# PTMagic 2.10 — Newly Listed Market History Reporting Handoff
**Date:** November 19, 2026 · **Scope:** PTMagic source reporting and verification, not a new metric · **Status:** Source committed; build and live TestMode acceptance pending.

## Problem and requested behavior

The November 19 LONG and SHORT data/log archives contained repeated WARN groups from six newly listed Binance Futures contracts: SOXXUSDT, IGVUSDT, ARTYUSDT, IBITUSDT, CCJUSDT and ETNUSDT. Their earliest contiguous five-minute candles began on November 18, 2026 between 09:30 and 09:55 UTC. The metrics with insufficient pre-listing windows remained UNAVAILABLE (correct) but the raid summary grouped the same underlying market-age limitation repeatedly by metric/trend.

**Owner requirement:** one informational notice per newly listed market, not multiple "Metric Warnings", when required historical observations cannot yet exist. Preserve actual failures and all trading safety.

## Application changes in existing branch

**Repository:** [HojouFotytu/PTMagic](https://github.com/HojouFotytu/PTMagic), existing `phase1/market-data-foundation` branch. No branch or strategy-settings modification.

- `Core/MarketAnalyzer/BinanceFuturesMarketUniverse.cs`: retain Binance's existing `exchangeInfo.onboardDate` as nullable UTC Unix milliseconds in the same persistent market metadata; older cache entries without this field remain valid but cannot justify suppressing warnings.
- `Core/MarketAnalyzer/MarketData/NewMarketHistoryDiagnostics.cs`: new reporting-only classifier. For an unavailable asset metric, require verified onboard time, a fresh and contiguous normalized source series beginning no later than one source interval after onboarding, an actual current expected endpoint, a recognized history-shortage reason, and a metric-specific required earliest source observation predating onboarding. Classifies price reference, dependent relative strength (with valid benchmark), ATRP, volume expansion, synchronized correlation and complete-period taker ratio/imbalance shortages. A missing/invalid listing date, stale source, gaps after onboarding, old truncated cache, invalid taker numbers or other reason are not reclassified. Reuses source snapshots only for invalid assets across trends.
- `Core/MarketAnalyzer/MarketData/RaidMetricWarnings.cs`: remove only verified pre-listing asset shortages from WARN grouping, including all matching SMS callers beyond the bounded five-example display list; mixed/unverified/global callers stay WARN. Emit `+ New markets with insufficient history: N` on each affected raid and one individual INFO detail per newly affected/changed market, e.g. `SOXXUSDT is too new (listed 2026-11-18 09:30 UTC); excluded from N metric results requiring pre-listing history. Other valid metrics remain active.` Do not repeat unchanged market detail every raid. One transition line when no current exclusions remain.
- `Core/Main/PTMagic.cs`: integrate classification into the existing end-of-raid summary only for Binance Futures, with no calculation, trigger or configuration-delivery changes.
- `Core/MarketAnalyzer/MarketData/MarketTrendHistoryRequirements.cs`: correct the descriptive Phase 3 global observed-cohort coverage text to the already-implemented ≥90% rule; **no new calculation behavior**.
- `Tests/Phase1MetricWarnings/Program.cs`: add two focused test groups (21 calls total including prior NO_TRADES group) for a complete source-backed new listing, overlapping metric families, >5 SMS callers, missing metadata, postlisting gap, cache truncation, invalid numeric values, global decision warnings, nonrepeated notices and recovery. `Tests/Phase1MetricWarnings/README.md` and application change log updated.

## Guaranteed safety boundaries

**Metric values and availability remain untouched.** New listing means the affected metric/timeframe result is still UNAVAILABLE, not fabricated zero; all other metrics continue to operate. The symbol remains in the original eligible market population; neither cohort membership nor the existing global 90%/100% coverage semantics change. A GlobalSetting or SMS decision that is truly indeterminate stays fail-closed and its decision failure remains a genuine WARN. NO_TRADES remains separate DEBUG handling.

Only the presentation/severity of **proved pre-listing history shortages** changes. No added Binance requests; listing date comes from an existing metadata response. No new metric registry entry, threshold, PT property, SOM behavior, live order, or independent LONG/SHORT strategy change.

## Verification boundary and next test

Source commits are published on the existing application branch. The working environment for the assistant has no .NET SDK, so **no compilation or executed 21/21 test PASS is claimed**; source-level delimiter checks are not compiler evidence. Local command:

```powershell
git pull --ff-only
dotnet build .\PTMagic.sln
dotnet run --project .\Tests\Phase1MetricWarnings
```

Then compare new-source isolated LONG and SHORT TestMode raids and export/log snapshots. Verify the number of markets and source timestamps, exact INFO lines, remaining real Metric Warnings, the same metric values/coverage/unavailable status, and unchanged GlobalSetting/SMS selection. If the native onboarding date is missing or inconsistent, the condition must remain a normal Metric Warning until verified; do not substitute the first retained candle as the exchange's listing date. The November 19 archive is **pre-change** evidence only.

**Related:** [current need-driven metric reassessment](2026-11-19-ptm-210-metric-reassessment.md), [older Dev 10→11 source evidence](2026-11-17-ptm-210-dev10-to-dev11.md), [application release changelog](https://github.com/HojouFotytu/PTMagic/blob/phase1/market-data-foundation/CHANGELOG-2.10.md). This work is an accuracy-of-diagnostics correction, **not an additional metric-development phase**.
