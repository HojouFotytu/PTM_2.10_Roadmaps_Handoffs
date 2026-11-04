# 2026-11-04 — D-018 raid warning verification

**Application repository:** HojouFotytu/PTMagic  
**Branch:** `phase1/market-data-foundation`  
**Application HEAD:** `34c30aa08918252d2976d6fabd7dddb1589acfd9`  
**Scope:** D-018 compact RAID SUMMARY metric warnings; D-017 and Phase1A regression checks.

## User-executed results

- `git pull --ff-only`: fast-forward `c66b9f3..34c30aa`.
- `dotnet build`: succeeded in **15.2 seconds**; Core, PTMagic and Monitor built on .NET 10.
- `dotnet run --project Tests/Phase1MetricWarnings/Phase1MetricWarnings.csproj`: **7 passed**.
- `dotnet run --project Tests/Phase1TriggerLogic/Phase1TriggerLogic.csproj`: **29 passed**.
- `dotnet run --project Tests/Phase1AReadiness/Phase1AReadiness.csproj`: **4 passed**.
- **Total: 40/40 deterministic tests passed.**

## Evidence boundary

These results verify compilation and deterministic checks, not actual RAID SUMMARY presentation in a running Binance Futures TestMode raid. Confirm the compact warning section under missing/stale/coverage issues and indeterminate GlobalSetting retention in a live TestMode raid before calling D-018 runtime-verified. No additional source changes were made during this documentation update. Phase 1C P1C-01 dynamic `ATRP`, then P1C-02 `MedianATRP`, remain next, with `MarketTrend.TrendMinutes` governing every calculated metric timeframe.
