#!/usr/bin/env python3
"""Reproduce asset/global closed-candle path-efficiency profiles from a PTMagic _data ZIP.

Usage: python 2026-11-21-price-path-reproducer.py PTMagic-_data-INSTANCE.zip
Requires Python 3.10+ and numpy. Does NOT inspect future prices or trading results.
Timeframes are discovered from MarketTrendAnalytics.json; no hardcoded horizons.
This core path reproducer does not recalculate the separate ATRP cross-check.
"""
import gzip
import io
import json
import math
import re
import struct
import sys
import zipfile
from pathlib import Path
import numpy as np

CANDLE = struct.Struct("<qqddddddq")

def len7(f):
    n = shift = 0
    while True:
        b = f.read(1)
        if not b: raise ValueError("Truncated .NET string length")
        n |= (b[0] & 127) << shift
        if b[0] < 128: return n
        shift += 7

def text7(f):
    return f.read(len7(f)).decode("utf8")

def read_cache(data):
    f = io.BytesIO(gzip.decompress(data))
    magic, version = struct.unpack("<ii", f.read(8))
    if (magic, version) != (0x50544D43, 2):
        raise ValueError("Expected native v2 PTMagic normalized candle cache")
    exchange, symbol = text7(f), text7(f)
    ticks, count = struct.unpack("<qi", f.read(12))
    if ticks <= 0 or count <= 0: raise ValueError("Invalid interval/count")
    close_prices = {}
    for _ in range(count):
        candle = CANDLE.unpack(f.read(CANDLE.size))
        flag = f.read(1)
        if flag == b"\x01": f.read(8)
        elif flag != b"\x00": raise ValueError("Invalid taker field")
        close_prices[int(candle[1])] = float(candle[5])
    if struct.unpack("<i", f.read(4))[0] != 0x43414348 or f.read(1):
        raise ValueError("Invalid end marker")
    return symbol, ticks // 10000, close_prices

def evaluate(path):
    with zipfile.ZipFile(path) as archive:
        snap = json.loads(archive.read("_data/MarketTrendAnalytics.json"))
        decisions = sorted(n for n in archive.namelist()
                           if re.fullmatch(r"_data/DecisionHistory/[^/]+\.jsonl", n))
        if not decisions: raise ValueError("Missing first-raid DecisionHistory")
        first = json.loads(archive.read(decisions[0]).splitlines()[0])
        from datetime import datetime
        pinned_ms = round(datetime.fromisoformat(first["AnalysisAsOfUtc"]).timestamp() * 1000)
        filenames = [n for n in archive.namelist()
                     if re.fullmatch(r"_data/NormalizedOhlcvCache/[^/]+/\d+/[^/]+\.gz", n)]
        sources = [read_cache(archive.read(n)) for n in filenames]
    intervals = {x[1] for x in sources}
    if len(intervals) != 1: raise ValueError("Mixed source intervals")
    interval = intervals.pop()
    endpoint = (pinned_ms // interval) * interval - 1
    profiles = []
    for name, trend in sorted(snap["Trends"].items(), key=lambda x: x[1]["TrendMinutes"]):
        duration_ms = int(trend["TrendMinutes"]) * 60000
        if duration_ms <= 0 or duration_ms % interval:
            raise ValueError("Invalid configured source duration")
        n = duration_ms // interval
        if n < 2:
            profiles.append({"name": name, "valid": 0,
                             "reason": "Fewer than two path steps"})
            continue
        scores = []
        for symbol, _, points in sources:
            closes = [points.get(endpoint - (n - j) * interval) for j in range(n + 1)]
            if any(x is None or not math.isfinite(x) or x <= 0 for x in closes):
                continue
            d = np.diff(np.log(closes))
            distance = float(np.abs(d).sum())
            if distance <= 0: continue
            scores.append(min(1.0, max(0.0, abs(float(d.sum())) / distance)))
        if not scores:
            profiles.append({"name": name, "minutes": int(trend["TrendMinutes"]),
                             "valid": 0, "median": None})
            continue
        profiles.append({"name": name, "minutes": int(trend["TrendMinutes"]),
                         "valid": len(scores),
                         "median": float(np.median(scores)),
                         "p10": float(np.quantile(scores, 0.1)),
                         "p90": float(np.quantile(scores, 0.9))})
    return {"source": Path(path).name, "pinned_raid": first["AnalysisAsOfUtc"],
            "source_candle_milliseconds": interval, "markets": len(sources),
            "profile": profiles}

if __name__ == "__main__":
    if len(sys.argv) != 2: raise SystemExit("Usage: python price-path-reproducer.py _data.zip")
    print(json.dumps(evaluate(sys.argv[1]), indent=2))
