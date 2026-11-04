# PTMagic 2.10 — Phase 1C implementation verification handoff

**Date:** 2026-11-04  
**Application:** `HojouFotytu/PTMagic`  
**Branch:** `phase1/market-data-foundation`  
**Last committed HEAD:** `64d063c1c9bc8886fb456cae97921780449f5cce` (verify HEAD before further edits)  
**Roadmap:** [Authoritative revised 2.10 roadmap](../roadmaps/revised-2.10-2026-11-04-markettrend-timeframe.txt), Section 5.5/5.6 and Phase1C checklist.  
**Status:** P1C-01 through P1C-07 **SOURCE IMPLEMENTED, NOT YET BUILD/TEST/TESTMODE VERIFIED**. Phase 1D must not be declared underway based on this alone.

## Implemented

- Per-asset ATRP with default Wilder period 14 over fully complete `MarketTrend.TrendMinutes` OHLC candles aggregated from normalized 5m data. First seed requires 15 complete trend bars; applies Wilder smoothing over older available contiguous history.
- Per-asset VolumeExpansion ratio using latest complete trend-sized quote volume divided by 20 preceding complete trend periods by default; no zero baseline.
- Global MedianATRP, VolatilityBreadth, MedianVolumeExpansion, VolumeExpansionBreadth, StrongVolumeExpansionBreadth with >=90% exact Phase 0 eligible population.
- Global VolumeConcentration (HHI*100 index), TopNVolumeShare, BTCVolumeShare, BTCETHVolumeShare over a *single latest complete trend period*, requiring 100% exact eligible quote-volume population and positive total. TopNVolumeCount defaults 10.
- All lookbacks and thresholds configurable per `MarketTrend`; each lookback N counts complete periods of the user's `MarketTrend.TrendMinutes`. The input source remains 5m. Invalid data remains unavailable with no shortcut/replacement.
- All metrics registered with scope; existing GlobalSetting/SMS/OffTrigger normalized resolver and tri-state trigger paths used. Monitor displays new global/asset metrics with %/x/index units; `MarketTrendAnalytics.json` exporter automatically includes snapshot features. No new exchange API calls.
- Separate correction: simple GlobalSetting AND/OR now evaluates ordered trigger results even with blank Tags (formerly dictionary collision).
- 13 synthetic Phase1COhlcv cases authored; previous 40 tests still need a fresh regression pass after these changes.

## Verification commands

```powershell
git pull --ff-only
dotnet build
dotnet run --project Tests/Phase1COhlcv/Phase1COhlcv.csproj
dotnet run --project Tests/Phase1MetricWarnings/Phase1MetricWarnings.csproj
dotnet run --project Tests/Phase1TriggerLogic/Phase1TriggerLogic.csproj
dotnet run --project Tests/Phase1AReadiness/Phase1AReadiness.csproj
```

Expected deterministic test counts if all pass: Phase1COhlcv **13**, metric warnings **7**, tri-state **29**, Phase1A **4**; **53 total**. These are *not claimed passes*. Compile failures and fixture discrepancies must be fixed before TestMode.

TestMode: enable representative per-asset/global features on 2h/4h/8h/24h trends with appropriate `StoreDataMaxHours`; ensure no incomplete-bar values, correct count/coverage, right metric units, exporter/Monitor entries, and proper GlobalSetting/SMS/OffTrigger behavior including unknown-in-OR. Inspect RAID SUMMARY for full grouped metric warnings. Verify unchanged legacy blank `Metrics` behavior.

**History sizing:** ATR(14) minimum 15 trend periods; VolumeExpansion(20) minimum 21 periods. For 4h these are 60h and 84h; for 8h 120h and 168h; for 24h 360h and 504h, plus margin for UTC period alignment. Retention never auto-expands; insufficient data must fail closed. Cold-start history may entail considerable Binance request load at high retention.

**Known exception:** Original Phase1B `Concentration` still ranks Top10 by fixed trailing 24h quote volume, separately tracked as `P1B-CONC-WINDOW`. Do not conflate it with new volume-based Phase1C concentration features.

After valid build, 53 test checks and satisfactory TestMode evidence, update STATUS to DONE, record a dated Phase1C closeout and write Phase1D-ready handoff. Do not reopen accepted Phase1A containment.

## 2026-11-04 — SMS summary list-aliasing follow-up

Application commit [`0e8ab70`](https://github.com/HojouFotytu/PTMagic/commit/0e8ab7056d32f16d1095a519ac4a1e87a29a4188) isolates the mutable per-market comment aggregation list from each persisted `TriggerSnapshot.MatchedTriggersContent`. Five new independent regression checks are in `Tests/Phase1SmsSummaryIsolation`. The prior TestMode run and Market Metrics page verified Phase 1C metrics and Monitor content. **New code has not been compiled or runtime-tested yet**. Verify `dotnet build`, `dotnet run --project Tests/Phase1SmsSummaryIsolation/Phase1SmsSummaryIsolation.csproj`, all four prior test harnesses, and a TestMode multi-SMS JSON export before final Phase1C closeout.
