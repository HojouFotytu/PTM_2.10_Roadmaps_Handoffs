# PTMagic 2.10 — Binance Global Account Ratio boundary correction

**Date:** November 12, 2026 (KST)  
**Application:** `HojouFotytu/PTMagic`, existing `phase1/market-data-foundation` branch  
**Implementation:** [`6f6da519b783ee51b20df3c7dfd5cf91b004e630`](https://github.com/HojouFotytu/PTMagic/commit/6f6da519b783ee51b20df3c7dfd5cf91b004e630)  
**Status:** GitHub published and verified; local .NET solution build, focused tests and configured runtime acceptance **pending**.

## Evidence and diagnosis

The user executed a direct public Binance Futures 5m `globalLongShortAccountRatio` query for BTCUSDT. Request boundaries were `startTime=1794408900001`, `endTime=1794412500000`. The response returned **13 observations**, including `timestamp=1794408900000` exactly one millisecond before the requested start, and **zero unaligned timestamps**. The first row included `longShortRatio=2.7538`, `longAccount=0.7336`, `shortAccount=0.2664`. This establishes the provider's inclusive five-minute boundary behavior; it is legitimate data for the *preceding* bucket and must not be counted in the current exclusive interval.

The existing service demanded that every returned row be at or after the exclusive `from` timestamp, throwing `InvalidOperationException` before accepting any row. In the November 12 runtime log, all attempted global-account ratio requests failed with this exception type while OI and funding acquired histories. The provider overlap therefore explains the consistent ratio failure.

## Narrow implementation

- `Core/MarketAnalyzer/MarketData/FuturesLongShortRatioDataService.cs`: when `from % 300000 == 1`, ignore exactly `timestamp == from - 1` after validating the row's identity and five-minute alignment; reject other early or late rows as before. Do not cache the extra row.
- Preserve `returned.Count` rather than accepted-row count in the `PageSize=500` exhaustion decision, so a complete provider page containing an overlap still requires another page if coverage is incomplete.
- `Tests/Phase2LongShortRatios/Program.cs`: focused cases for actual 13-row/12-valid response, persistent cache exclusion, unrelated earlier-row rejection and 500-row page/restart pagination behavior.
- `Tests/Phase2LongShortRatios/README.md`: describe the confirmed boundary case and strict acceptance semantics.

No changes to other acquisition families, Binance rate-limit rules, settings, SOM, PT APIs or LONG/SHORT strategies. The diagnostic analyzer's separate market-population mismatch was not modified.

## Acceptance boundary and next action

The previous validated application source was `5a21a482711c8026b50fce10c55b3fb76f4075c3`: .NET 10.0.403 solution build PASS in 13.9 seconds, 18/18 offline harnesses and 386 checks PASS, with eight nonfatal nullable warnings in two existing test projects. Those results **do not validate** commit `6f6da519b783ee51b20df3c7dfd5cf91b004e630`.

Run from the existing PTMagic repository checkout:

```powershell
$ErrorActionPreference = "Stop"
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Git pull failed" }
git log -1 --format="%H"
& ".\Tests\Phase2OpenInterestIncremental\Run-Phase2Validation.ps1"
if ($LASTEXITCODE -ne 0) { throw "Validation failed" }
```

After successful local validation, repeat the configured Binance TestMode raid and confirm real global-account ratio samples no longer fail solely because of the one-millisecond provider overlap. Then compare persistent caches, provider requests and calculated values across two **actual process startups**. Neither configured acceptance gate has yet passed.
