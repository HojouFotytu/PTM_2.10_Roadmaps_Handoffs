# 2026-11-04 — Selective legacy PriceTrend calculation refactor

**Application source:** HojouFotytu/PTMagic, branch `phase1/market-data-foundation`, HEAD [`1a6b9aa401fac74842e4d53ddbbfb2b2a4c5dc11`](https://github.com/HojouFotytu/PTMagic/commit/1a6b9aa401fac74842e4d53ddbbfb2b2a4c5dc11).  
**Task:** `P1-COMPAT-LEGACY-SELECTIVE`; decision D-020.  
**Status:** SOURCE IMPLEMENTED — BUILD, ALL TESTS, TESTMODE PENDING.

## Motivation

Prior Phase1C normalized `MarketTrend.Metrics` was opt-in, but `BaseAnalyzer.BuildMarketTrends` still fetched legacy snapshots and compared price changes for *every* MarketTrend, including ATRP/volume-only trends. The normalized runtime selected its asset/global populations from legacy `MarketTrendChange` lists, preventing simple removal of the old pass. SMS 24h-volume and summary fields also assumed at least one legacy market trend existed.

## Implementation

1. `LegacyMarketTrendPlanner`: computes separate legacy per-asset and global-mean requirement sets from configured MarketTrends, GlobalSetting triggers, SMS triggers and OffTriggers. Empty `Metrics`, non-Futures and CMC stay fully legacy. Implicit `Trigger.Metric`/ `OffTrigger.Metric` on a metrics-enabled trend forces only the legacy data actually needed. Volume-only, age and duration triggers do not force legacy returns.
2. `BaseAnalyzer`: optional required-name sets skip historical snapshot/legacy return passes and omit legacy global averages for explicitly metrics-only trends. No synthetic zero-valued averages are added when skipped.
3. `MarketTrendPopulationSelector` selects normalized per-trend global/asset symbols independently from legacy return records using frozen Phase0 eligibility, latest Exchange market snapshots, 24h volume ranking, MaxMarkets, AllowedMarkets/IgnoredMarkets and TrendThreshold. Configured threshold filtering may compute normalized returns internally but does not publish legacy PriceTrend.
4. `Core/Main/PTMagic.cs`: retains current market price/24h-volume snapshots for SMS volume checks, SMS activation reference price/volume and `LastRuntimeSummary.MarketSummary`. This removes assumptions that legacy trend dictionary has any keys. The old Market Analyzer page naturally shows blanks for trends not computed; eventual page merge is outside this patch.
5. `Tests/Phase1SelectiveLegacy`: 14 independent fixtures for compatibility, non-Futures/CMC, selective global vs asset, independent volume and age triggers, population filters and caps.

## Verification

```powershell
git pull --ff-only
dotnet build
dotnet run --project Tests/Phase1SelectiveLegacy/Phase1SelectiveLegacy.csproj
dotnet run --project Tests/Phase1SmsSummaryIsolation/Phase1SmsSummaryIsolation.csproj
dotnet run --project Tests/Phase1COhlcv/Phase1COhlcv.csproj
dotnet run --project Tests/Phase1MetricWarnings/Phase1MetricWarnings.csproj
dotnet run --project Tests/Phase1TriggerLogic/Phase1TriggerLogic.csproj
dotnet run --project Tests/Phase1AReadiness/Phase1AReadiness.csproj
```

Expected **14 new + 58 existing = 72** deterministic tests, but no current passes are claimed. Run a Binance Futures TestMode raid with metrics-only trends and at least one legacy-only or implicit-PriceTrend SMS trend: verify normalized 1h/2h/4h metric population counts, ATRP/volume values, inherited selection rules, legacy trigger activation, current SMS price/24h-volume values, and lack of unintended global reapplication or PT writes.

The earlier Phase1C closeout is still valid for the prior accepted build; this additional refactor is a **new unverified change** and must not be marked complete until fresh evidence.
