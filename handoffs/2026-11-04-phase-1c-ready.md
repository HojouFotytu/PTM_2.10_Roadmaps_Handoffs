# PTMagic 2.10 — New Chat Development Handoff: Begin Phase 1C

**Date:** 2026-11-04
**Code repository:** [HojouFotytu/PTMagic](https://github.com/HojouFotytu/PTMagic)
**Working branch:** `phase1/market-data-foundation`
**Last checked code HEAD:** `89324bc5c8c5ea19ceb543b6ab5130899f2675dc` (merge commit). **Recheck HEAD before any edits.**
**Roadmaps/handoffs repository:** [HojouFotytu/PTM_2.10_Roadmaps_Handoffs](https://github.com/HojouFotytu/PTM_2.10_Roadmaps_Handoffs), branch `main`.
**Authoritative roadmap:** [revised PTMagic 2.10 roadmap](../roadmaps/revised-2.10-2026-11-04.txt)
**Current task tracker:** [STATUS.md](../STATUS.md), [decisions](../DECISIONS.md), [Phase 1A issue closeout](../issues/001-cold-start-readiness.md).

## Immediate next-chat request

**Continue PTMagic 2.10 development from Phase 1C-01: implement per-asset `ATRP5m`, then Phase 1C-02 global `MedianATRP5m`.** Begin with current code inspection and an exact calculation/design/test plan, then make small, reviewable implementation commits. Do not reopen Phase 1A as a blocker without new evidence.

## Product and architecture boundary

PTMagic **2.9 was completed and released** (modernization/CPU/network/Monitor fixes). This *entire* Phase 0–6 deterministic market-analysis expansion is **PTMagic 2.10**, even though the TestMode binary logged `Version 2.9.1`. Use .NET 10. No external AI layer.

Keep existing legacy market trend calculation and ProfitTrailer settings behavior. Normalized 5m Binance Futures USDT perpetual OHLCV is stored separately via `MarketDataService` / `MarketDataStore`; source candles include H/L/C and quote volume, valid/closed timestamps and staleness. Apply actual Phase 0-resolved trend-specific eligible symbols. Do not independently define another universe, add raw Binance endpoints just for ATRP, add duplicate storage or implement a separate analytics subsystem.

## Phase 1A and Phase 1B status

**Phase 1A: DONE — ACCEPTED CORRECTNESS CONTAINMENT** (no longer blocks Phase 1C). Normalized first raid may be incomplete after a long cold start; the *consequence* is contained by 90% cross-sectional readiness and fail-closed normalized triggers, and natural scheduled incremental refresh restores readiness. The original candle-boundary ingestion mechanism is *plausible but unproven*, not eliminated.

Eight Phase 1B metrics already implemented:
- Global: `PriceTrend` (arithmetic mean normalized return), `MedianPriceTrend`, `MeanMedianSpread`, `Breadth` (positive-return share), `Dispersion`, `Concentration` (top-ten **return** advantage in percentage points among 24h quote-volume-ranked markets).
- Per asset: `RelativeStrengthMarket`, `RelativeStrengthBTC`.

**Coverage policy (committed):** `MarketMetricCoverage` requires at least `ceil(0.90 × eligibleGlobalSymbols)` valid aligned returns, and an eligible count > 0. `Concentration` retains **100%** eligible complete-volume ranking. Missing/invalid/stale data are unavailable, never zero. Each `FeatureValueSnapshot` carries `Value`, `SampleCount`, `EligibleSampleCount` where applicable, `CoveragePercent`, `CalculatedAtUtc`, `SourceDataTimestampUtc`, `IsValid`, `IsStale`, and `InvalidReason`. Trend/Monitor snapshots include expected closed candle endpoint and categorized missing/invalid counts.

**Settings behavior:** Explicit `MarketTrend.Metrics` opts in to normalized metrics, and explicit `Trigger.Metric` / `OffTrigger.Metric` selects them. Omitted `Metric` preserves legacy processing. Unavailable normalized metrics cannot activate dependent GlobalSettings/SMS (including negated custom conditions). If no fully evaluable setting matches and normalized inputs are unavailable, retain active GlobalSetting rather than falling back automatically to `Default`; independent valid settings remain eligible. There is **no trading halt** and no forced new Binance data requests. Same-setting reapplication is allowed.

## Code commits

| Commit | Change |
|---|---|
| [`3a2ba02`](https://github.com/HojouFotytu/PTMagic/commit/3a2ba0227246ea4bcad91205273575ae04fa4f8e) | 90% cross-sectional readiness; 100% Concentration; diagnostic metadata/Monitor export |
| [`c038a11`](https://github.com/HojouFotytu/PTMagic/commit/c038a11baff881285317f07f393084624b6bd3ca) | Indeterminate GlobalSetting hold and invalid SMS negation suppression |
| [`e002801`](https://github.com/HojouFotytu/PTMagic/commit/e002801555ffb98e8169e1943aa4a13b05956b52) | Four deterministic Phase1AReadiness tests |
| [`11d6e28`](https://github.com/HojouFotytu/PTMagic/commit/11d6e286b0ed6474d730eb2eba1b6ecb0158a26d) | Log summary differentiates GlobalSetting switched vs reapplied |
| `89324bc5c8c5ea19ceb543b6ab5130899f2675dc` | Source branch HEAD at handoff; includes preceding commits |

## Actual tests and live diagnostic evidence

User-run `dotnet build`: **Core/ PTMagic / Monitor net10.0 succeeded**. User-run `dotnet run --project Tests/Phase1AReadiness/Phase1AReadiness.csproj`: **4/4 passed**.

November 4 Binance Futures TestMode cold-start and subsequent raids:
- First raid ~13:30 KST: 756/756 normalized series reported refreshed, 654,696 candles, zero failures. Global 4h valid returns **32/250 (12.8%)** with 218 `MissingEndpoint`, asset metrics **0/1434**. 90% gate rejected global metrics; dependent diagnostic GlobalSettings skipped and active `Default` held.
- Second raid ~13:31 KST: 705/756 series refreshed, 2,115 incremental candles, zero failures. Global 4h **249/249 (100%)**; asset returns **717/717**, asset metric values **1434/1434**. No invalid reasons.
- Third raid ~13:32 KST: zero kline requests across 756 cached series; same fully valid analytics.
- After flood protection expired, `DIAG_Global_AllMetrics` actually activated ~13:33 KST, remained stable. BTC/ETH diagnostic normalized SMS and SOL legacy SMS also worked.
- Every five-minute boundary, normal incremental refresh ~2,268 candles (756×3 overlap); many intervening raids required zero requests. No automatic pause/forced catch-up. TestMode **did not send PT settings**.

**Non-blocking follow-up tests:** non-default active GlobalSetting retention when a later below-90% condition occurs; runtime verification of `11d6e28` switched/reapplied labels (logs collected before patch); additional 90–99% and sparse/stale/boundary fault injection under Phase 1E. Tested binary still reports 2.9.1; correct that in 2.10 release/version preparation, not in this task.

## Phase 1C scope and first implementation steps

**P1C-01: per-symbol `ATRP5m`.** Use the existing normalized 5m closed OHLCV series, never the still-forming candle. Confirm the mathematical contract before coding:

1. Proposed standard True Range per closed bar: `TR = max(high-low, abs(high - previousClose), abs(low - previousClose))`.
2. Proposed first ATR: simple average of first 14 *defined* TRs (requiring at least 15 closes if previous close required for all 14), then Wilder's recurrence `ATR_t = (ATR_(t-1) * 13 + TR_t) / 14`. Establish whether a longer back-history changes the value, whether use a fixed tail or all retained 72h candles, and what seed convention is intended; this has not yet been formally accepted.
3. Proposed percentage: `ATRP5m = 100 × ATR(14) / latest valid closed candle close`; reject zero/invalid denominator, non-finite values, missing/unaligned endpoint, stale data, insufficient consecutive warm-up bars.
4. `MarketTrend.TrendMinutes` is the legacy/normalized **return horizon** (e.g. 4h); `ATRP5m`'s source interval must remain **5 minutes**, independent of TrendMinutes. Do not calculate 4h ATR just because the metric appears in a 4h trend.
5. Decide whether ATR period is initially a hard-coded consistent 14 or configured as `MarketAnalyzer.ATRPeriod` and how period changes are reflected in metric validity; do not silently invent a setting.

**P1C-02: `MedianATRP5m`.** Calculate across the same exact Phase 0-resolved **global** universe for the trend. Validate each per-market ATRP first; use the established cross-sectional coverage threshold of **90%** of eligible population. Report valid numerator, eligible denominator, endpoint, and reasons; ensure even/odd medians are correct. Do not calculate the median from the SMS asset universe or all exchange-listed symbols.

**Then:** P1C-03 volatility breadth (threshold required); P1C-04 recent quote-volume expansion over comparable closed windows; P1C-05 volume-expansion breadth; P1C-06 quote-volume share concentration **distinct from existing `Concentration`**; P1C-07 metric registration, Monitor, triggers and tests.

## Source files to inspect first

- `Core/MarketAnalyzer/MarketData/MarketCandle.cs`, `MarketDataSeriesSnapshot.cs`, `MarketDataStore.cs`, `MarketDataService.cs`.
- `Core/MarketAnalyzer/MarketData/MarketTrendAnalyticsEngine.cs`, `MarketTrendMetrics.cs`, `MarketMetricCoverage.cs`.
- `Core/MarketAnalyzer/MarketData/BinanceFuturesAnalyticsRuntime.cs`, `MarketTrendMetricTriggerResolver.cs`, `AnalysisSnapshots.cs`, `MarketTrendAnalyticsMonitorExporter.cs`, `MarketTrendAnalyticsMonitorSnapshot.cs`.
- `Tests/Phase1AReadiness` as an example for a dependency-light regression harness.
- `Core/Main/PTMagic.cs` only as needed for explicit metric routing. Avoid unrelated changes to this large file.

## Acceptance checks and workflow

1. Fetch current source HEAD (do not trust handoff SHA as permanently current) and roadmap/status/decisions; inspect relevant code. State precise plan and mathematical assumptions.
2. Implement a pure, deterministic ATRP calculator with small tests using independently known 5m OHLC sequences. Cover Wilder seed/warm-up, stable/rising/falling data, non-finite values, exact missing endpoint, gaps, stale candles and last-closed denominator.
3. Register the exact metric name/scope and expose per-asset outputs in existing runtime/Monitor; preserve legacy `Metric` omitted semantics and fail closed for invalid new data.
4. Implement `MedianATRP5m` only after per-asset ATRP verification; test odd/even medians, missing assets, 90% threshold, exact universe.
5. Verify `dotnet build`, existing `Tests/Phase1AReadiness`, new tests, and first/normal/idle TestMode raids. A source commit or build alone is not runtime validation.
6. Commit application code to `phase1/market-data-foundation` only. Record commits, test evidence, decisions and any new handoff in this separate documentation repository.
7. No extra Binance APIs, duplicated data stores, external AI layer, automatic trading suspension, or modifications to completed PTMagic 2.9.

**New chat opening instruction:** “Begin PTMagic 2.10 Phase 1C. Use the latest Phase 1C-ready handoff and authoritative roadmap, verify both repository HEADs, inspect the current metric/market-data code, and start P1C-01 ATRP5m with explicit math/validity definitions and deterministic tests.”
