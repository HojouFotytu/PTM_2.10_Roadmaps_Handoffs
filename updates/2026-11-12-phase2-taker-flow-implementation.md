# PTMagic 2.10 — Phase 2 taker-flow implementation checkpoint

**Date:** 2026-11-12 KST  
**Application repository:** `HojouFotytu/PTMagic` / existing `phase1/market-data-foundation`  
**Published source revision:** [`361c729ff8e64f40b2e0a507c557297161fbbc1e`](https://github.com/HojouFotytu/PTMagic/commit/361c729ff8e64f40b2e0a507c557297161fbbc1e)  
**Status:** **Implemented in source and inspected. A .NET build and new focused tests are pending user-local execution.** This is **not** a verified runtime-acceptance claim.

## Implemented metric contract

Two new **asset-only** opt-in metrics join the 24 retained D-053 metrics; the current catalogue contains **26 names** (17 globally evaluable, nine asset-only).

- `TakerBuyRatio = sum(TakerBuyQuoteVolume) / sum(QuoteVolume)`, range **0–1**.
- `TakerImbalance = 2 × TakerBuyRatio − 1`, range **−1 to +1**.

Both use the **same** latest completely closed UTC-aligned `MarketTrend.TrendMinutes` period, assembled from source-verified normalized 5m candles. This is a **ratio of summed quote volumes**, not an arithmetic mean of individual candle ratios. The metrics are not independent input sources and should not be treated as independent evidence in composite analytics. Units are **dimensionless**. Neutral values are 0.5 (ratio) and 0 (imbalance). Valid extreme observations are permitted; incomplete or invalid source is UNAVAILABLE, never a fabricated zero.

Binance USDⓈ-M `/fapi/v1/klines` provides total quote volume at array index 7 and taker-buy **quote** volume at index 10; index 9 is taker-buy *base* volume and is not substituted. Existing kline requests now carry this optional data without a new provider endpoint or dedicated request-budget subsystem. Existing Binance Spot/US dispatch still uses the shared kline parser; unsupported/missing source fields remain unavailable.

## Source integration

- `Core/MarketAnalyzer/MarketData/BinanceKlineClient.cs`: parse index 10, validate finite nonnegative values not exceeding total quote volume, and keep invalid/missing taker fields null without poisoning otherwise valid OHLCV.
- `MarketCandle.cs`, `MarketDataStore.cs`: nullable taker-buy quote volume plus source-volume integrity checks.
- **New file in existing source directory** `TakerFlowFeatureEngine.cs`: exact closed-period aggregation with contiguous-candle checks, pinned UTC boundaries, finite total quote volume, ratio-of-sums, and feature validity/diagnostic metadata. Binary search over existing sorted closed candles avoids per-symbol full-history dictionary allocation.
- `MarketDataService.cs` and `BinanceFuturesAnalyticsRuntime.cs`: request repair history **only when enabled taker metric trends require it**. The normal one-source OHLCV refresh, frozen universe, pinned as-of, and base rate limiting remain unchanged.
- `MarketDataWarmStartCache.cs`: write binary **v2** with nullable taker values, **read both v1 and v2**. v1 records remain valid OHLCV but are not falsely treated as taker-complete. On selected trends, targeted recent-period taker backfill coexists with preserved cached OHLCV history; successfully verified new coverage saves immediately even inside the existing save throttle. No bulk deletion/repopulation of the user's original cache directories.
- `MarketTrendMetrics.cs`, `MarketTrendAnalyticsEngine.cs`, `MarketTrendHistoryRequirements.cs`, `MarketTrendMetricTriggerResolver.cs`: 26-name catalogue, correct asset scope, standard per-trend retention requirements, existing SMS/Monitor/export path, dimensionless units.
- `Monitor/Pages/MarketAnalyzer.cshtml.cs`: explicit titles/tooltips, four-decimal asset display, and green/red around 0.5 (ratio) or zero (imbalance). No change to DashboardTop polling, startup SOM, or existing global metric formatting.
- `Tests/Settings/settings.analyzer.json` and `README.md`: **existing** test configuration updated in place to version 2.1.0, with 26 metrics across the same M30/H1/H24 MarketTrends and the same two SMS groups; no new strategy repository, folder tree or production presets.

## Regression additions, authored but not yet executed

Existing harnesses (not new directories): `Tests/Phase1COhlcv` adds exact weighted ratio, integration, zero-volume, legacy missing-data and Binance index-10 parser checks; `Tests/NormalizedWarmStartCache` adds realistic legacy-v1 restoration, selectively requested taker history, immediate v2 persistence despite the save throttle, and restart reuse; `Tests/Phase2AdaptiveAcquisition` now expects **26** registered metrics (17 global-capable, nine asset-only).

A further targeted guard prevents repeat full-history requests when the configured OHLCV retention is too short to hold the required taker period; that metric remains unavailable until the retention constraint is resolved. The existing warm-start harness includes a direct regression for this condition. The newly authored focused tests total **15 Phase1COhlcv groups, 10 NormalizedWarmStartCache groups, and 8 Phase2AdaptiveAcquisition groups** (33 expected; **not yet executed**).

The D-053 user-run build and **36/36** focused tests at `e31635a1` and four configured TestMode raids are previous-feature evidence only; they do **not** validate this new revision. A .NET SDK is unavailable to the assistant's execution environment. No compile or test PASS is claimed for `361c729ff8e64f40b2e0a507c557297161fbbc1e`.

## Exact next verification

From the existing application repository root on the user's Windows host:

```powershell
git switch phase1/market-data-foundation
if ($LASTEXITCODE -ne 0) { throw "Branch switch failed" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Git pull failed" }
git rev-parse HEAD
dotnet build .\PTMagic.sln
if ($LASTEXITCODE -ne 0) { throw "Solution build failed" }
foreach ($project in @(
  "Tests/Phase1COhlcv/Phase1COhlcv.csproj",
  "Tests/NormalizedWarmStartCache/NormalizedWarmStartCache.csproj",
  "Tests/Phase2AdaptiveAcquisition/Phase2AdaptiveAcquisition.csproj"
)) {
  dotnet run --project $project
  if ($LASTEXITCODE -ne 0) { throw "Focused test failed: $project" }
}
```

After the **new** source passes, use the existing 26-metric TestMode analyzer to evaluate real source coverage, taker ratio/imbalance validity and initial cache upgrade versus subsequent raids, with PT writes still disabled. Do not invent runtime acceptance until those results exist. Defer unrelated full replay/large synthetic cycles.

**Separation:** This is PTMagic software only. No modifications to ProfitTrailer personal LONG/SHORT analyzer, settings, PAIRS, DCA, INDICATORS, or separate strategy repositories.

[Prior D-053 acceptance](2026-11-12-d053-configured-testmode-validation.md) · [Source design review](2026-11-12-phase2-taker-flow-source-review.md) · [Current technical roadmap](../roadmaps/CURRENT.md)
