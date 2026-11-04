# PTMagic 2.10 — Phase 1D Correlation Development Handoff

**Date:** 2026-11-04  
**Application:** `HojouFotytu/PTMagic`  
**Working branch:** `phase1/market-data-foundation`  
**Last checked application HEAD:** `0e8ab7056d32f16d1095a519ac4a1e87a29a4188`  
**Documentation:** [Authoritative revised roadmap](../roadmaps/revised-2.10-2026-11-04-markettrend-timeframe.txt) · [STATUS](../STATUS.md) · [Phase1C final evidence](../updates/2026-11-04-phase1c-final-closeout.md).

## State on handoff

**Phase 1A** closed (readiness/coverage containment); **Phase 1B** completed; **Phase 1C CLOSED AND VERIFIED** (P1C-01–07); **Phase 1D NEXT, NOT STARTED**.

Phase1C proof: .NET 10 Core/PTMagic/Monitor build passed; **58/58 user-run deterministic tests** (SMS isolation 5, OHLCV 13, warnings 7, three-valued triggers 29, readiness 4). Binance Futures live TestMode confirmed metric calculation on 1h/2h/4h, insufficient 8h history fails closed at StoreDataMaxHours=96, exact populations, GlobalSettings and BTC/ETH/SOL SMS/OffTrigger routing, full metric warnings and no PT writes. Market Metrics content confirmed. The final 19:10–19:33 KST log and fresh JSON have **8 new SMS snapshots; 8/8 isolated, 0 foreign descriptions**, closing `P1C-SMS-SNAPSHOT-ALIAS`.

Current source files relevant to Phase1D:
- `Core/MarketAnalyzer/MarketData/MarketDataStore.cs`, `MarketDataSeriesSnapshot.cs`: normalized 5m candle storage and snapshots, closed-candle state, gap/stale diagnostics.
- `Core/MarketAnalyzer/MarketData/MarketTrendAnalyticsEngine.cs`: frozen exact per-trend eligible global/asset populations, existing return metrics and Phase1C integration, shared snapshot objects.
- `Core/MarketAnalyzer/MarketData/MarketTrendMetrics.cs`: canonical feature names, scope registration and opt-in parsing.
- `Core/MarketAnalyzer/MarketData/MarketMetricCoverage.cs`: 90% eligible coverage safeguards and metadata; do not weaken.
- `Core/MarketAnalyzer/MarketData/TrendPeriodMetricsCalculator.cs`: completed UTC-aligned trend-duration aggregation precedent; can reuse or consolidate its alignment logic without duplicating another historical store.
- `Core/MarketAnalyzer/MarketData/MarketTrendMetricTriggerResolver.cs`, `Core/Main/PTMagic.cs`: normalized GlobalSetting/SMS/OffTrigger lookup, tri-state expression interpretation.
- `Core/MarketAnalyzer/MarketData/MarketTrendAnalyticsMonitorExporter.cs`, `Monitor/Pages/MarketMetrics.cshtml.cs`, `.cshtml`: read-only export and Monitor display paths.
- `Tests/Phase1COhlcv`, `Tests/Phase1SmsSummaryIsolation`, `Tests/Phase1TriggerLogic`, `Tests/Phase1MetricWarnings`, `Tests/Phase1AReadiness`: established regression harness pattern.

## Required Phase 1D scope — synchronized return correlation

1. Implement synchronized *complete* return sequences using intervals from **each `MarketTrend.TrendMinutes`** (D-016). Normalized 5m OHLCV is **source resolution only**, not permission to hardcode 5m/15m correlation metrics. Do not calculate correlation between raw price levels.
2. Define and document up front: simple vs log return (choose and test), configurable rolling sample count N and N+1 price endpoints, UTC-aligned closed trend-bar boundaries, correlation minimum sample size, zero-variance treatment, source-data gaps, missing BTC comparison candles, stale data, insufficient StoreDataMaxHours and behavior on market listing dates.
3. Per-asset `CorrelationToBTC`: Pearson coefficient of synchronized return vectors with range [-1, +1]. Align BTC and asset vectors by the **same exact trend-period endpoint timestamps**, not by index on independently sparse arrays; count only explicitly accepted points. Do not fill missing returns with 0, forward fill, shift windows or use incompatible market windows.
4. Global `MedianCorrelationToBTC` and `MeanCorrelationToBTC` with the exact eligible `MarketTrend` universe denominator and Phase1A 90% coverage gate; 100% remains required only for special metrics already designated that way.
5. Establish non-duplicative source snapshot sharing within a raid, avoid avoidable per-symbol copying/allocations, and bound computation at the actually required rolling period length. The existing optional **cross-raid unchanged historical snapshot reuse** is a separate benchmarked performance follow-up, not required to deliver Phase1D.
6. Add canonical opt-in names/scopes/configuration, GlobalSetting and SMS/OffTrigger normalized routing with missing values retaining D-017 three-valued semantics, Monitor/export columns and descriptive tooltip units (correlation is a *unitless coefficient*, never a percent).
7. Add deterministic fixtures covering perfect positive (+1), negative (-1), non-correlated cases with controlled expected values, BTC self-correlation (when sufficient variance), constant/zero variance, missing/unequal endpoints, stale history, too-short retention, mismatched period alignment, exactly-at-minimum and just-below-coverage denominators, and unchanged legacy metric behavior. Validate 5m, 1h, 2h, 4h etc using the same D-016 rule, not new hardcoded intervals.
8. Inspect runtime performance across ~750 normalized market sources and ~250 eligible global population; compare initial/steady raids; verify no extra Binance HTTP calls solely for correlation (source candles already ingested).
9. Build/tests on user .NET10 installation, then TestMode live metrics, GlobalSetting/SMS/OffTrigger, export, and Monitor inspection. Do not mark Phase1D DONE until accepted verification.

## Scope decisions still to be settled within Phase1D

- Rolling N and whether N is configurable per MarketTrend.
- Log versus simple return (Pearson on return sequences; never raw close correlation).
- Requirement that **all N return timestamps** be present vs explicit pairwise overlap policy (if any missing samples are allowed, minimum overlap and common endpoint must be documented and tested, and gaps cannot silently change comparison windows).
- Whether `AveragePairwiseCorrelation` is worth O(M^2 * N) work in first release; **default recommendation is defer**, as per the roadmap.
- Whether average/median market correlation should include BTC itself; pick the exact denominator deliberately and document it.
- Underlying `Concentration` 24h volume rank correction (`P1B-CONC-WINDOW`) remains separate, not mixed into Phase1D.

## Never regress

- No AI layer or redundant external market-data endpoints.
- Source 5m normalization, exact eligible population, only completed period endpoints.
- No zero substitution for unavailable, no fabricated readiness; >=90% global coverage, previously documented 100% exceptions.
- D-017 strong Kleene trigger semantics, unsupported OffTriggerConnection compatibility, and no PT writes in TestMode.
- No five-line RAID SUMMARY truncation.
- SMS snapshot alias fix and fresh-persistence behavior; `RefreshOffTriggers=false` preserves existing snapshots by design.
- No reopen of closed Phase1A containment work without new evidence.

## Test commands to preserve existing acceptance

```powershell
git status --short
git pull --ff-only
dotnet build
dotnet run --project Tests/Phase1SmsSummaryIsolation/Phase1SmsSummaryIsolation.csproj
dotnet run --project Tests/Phase1COhlcv/Phase1COhlcv.csproj
dotnet run --project Tests/Phase1MetricWarnings/Phase1MetricWarnings.csproj
dotnet run --project Tests/Phase1TriggerLogic/Phase1TriggerLogic.csproj
dotnet run --project Tests/Phase1AReadiness/Phase1AReadiness.csproj
```

**Previously verified baseline:** 58/58 tests; future changes need a fresh rerun. Record application HEAD and new numerical/acceptance evidence in the documentation repository after Phase1D work.

**Next action:** inspect current branch HEAD and the listed source types, write the Phase1D correlation calculation/coverage contract, then implement using opt-in metric registration and full synthetic tests.
