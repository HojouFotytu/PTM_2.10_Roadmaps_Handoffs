# 2026-11-04 — Optional cross-raid historical snapshot reuse

**Task:** P1-PERF-SNAPSHOT  
**Scope:** Future performance optimization, not implementation.  
**Roadmap:** [PTMagic 2.10 revised roadmap](../roadmaps/revised-2.10-2026-11-04-markettrend-timeframe.txt), §12.7.

The current normalized data path creates fresh per-symbol snapshots that copy
and sort retained candles, extract closed candles and recheck gaps.
For unchanged historical data, future development should reuse immutable
historical snapshots across raids instead of repeating that work.

**Required safeguards:** invalidate/update cache when candle data changes
or retention trims it; recompute per-raid time-dependent closed-candle
and staleness state; preserve thread safety, normalized 5m ingestion,
configured MarketTrend analytical windows, data validity and existing
triggers. Benchmark CPU/GC/allocation and correctness at 72h and 144h
retention and actual market counts.

**Status:** OPTIONAL / PLANNED. No application-code modification or runtime
performance claim. Does not block current P1C-01 ATRP work.
