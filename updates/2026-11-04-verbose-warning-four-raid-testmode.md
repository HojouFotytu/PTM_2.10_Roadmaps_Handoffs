# PTMagic 2.10 — Local verbose metric warning TestMode verification

Date: 2026-11-04
Source branch: HojouFotytu/PTMagic / phase1/market-data-foundation
Source HEAD inspected: efa7b5ff1a99606395c1b1b9636c828600a55353
Uploaded runtime version: 2.10.0 (binary does not embed an exact Git SHA)

## Uploaded evidence

- Pasted text(20261104-142438).txt: four consecutive user-run Binance Futures raids, 23:19–23:24 Korea time.
- MarketTrendAnalytics(6).json: timestamp 2026-11-04T14:22:14.8165153+00:00 (second raid).
- LastRuntimeSummary(6).json: LastRuntime 2026-11-04T14:22:06.0850927Z (second raid, not final raid).
- SingleMarketSettingSummary(6).json: 13 SMS entries; 10 newly activated at 14:22:15Z and three retained from 13:49:11Z.

## Runtime outcomes

| Raid | Approximate time / duration | Metric groups | Candle ingestion | Price-return availability |
|---|---|---|---|---|
| 1 | 23:19–23:21 / 2m 0s | 31 | 756/756 fetched, 872,424 candles, 0 failed; Binance rate limiter paused requests | 142/250 global; 296/519 asset; 223 missing closed endpoints |
| 2 | 23:22 / 10s | 7 | 373/756 refreshed, 1,119 candles; 383 skipped | 250/250 global; 519/519 asset |
| 3 | 23:23 / 1s | 7 | All 756 series current; no kline requests | Full coverage |
| 4 | 23:24 / 1s | 7 | All 756 series current; no kline requests | Full coverage |

No ERROR/FATAL messages. TestMode reported no ProfitTrailer configuration updates.

## What seven stable warning groups mean

1. FILTERED_1h / PriceTrend: `DIAG_SMS_SOL_FilteredOut`, `SOLUSDT`, activation trigger #1, Absolute, explicit PriceTrend. SOL excluded by `IgnoredMarkets="SOL"` despite being in AllowedMarkets. Expected fail-closed behavior, and detailed caller identification is now confirmed.
2. FULL_2h / ATRP: `DIAG_Global_RejectAssetScope` references an asset-only metric in a GlobalSetting. Expected invalid scope.
3. IMPLICIT_1h / PriceTrend: `DIAG_SMS_BTC_ExplicitDisabledPriceTrend` requests explicit PriceTrend although the configured explicit metrics list omits it; omitted Metric trigger references still receive implicit PriceTrend. Expected invalid explicit reference.
4. INSUFFICIENT_8h / ATRP: 519/519 unavailable, only 11/15 complete 8h periods for ATRP(14), with SMS activation/OffTrigger call examples.
5. INSUFFICIENT_8h / MedianATRP: 0/250, expected insufficient market coverage.
6. INSUFFICIENT_8h / MedianVolumeExpansion: 0/250, expected insufficient market coverage.
7. INSUFFICIENT_8h / VolumeExpansion: 519/519 unavailable, 11/21 complete 8h volume periods for VolumeExpansion(20).

Grouped counts, caller names/market/tags/relations, failure reasons and analytics populations are present; no per-pair warning flood occurred in steady-state raids.

## Cross-export verification (second raid)

- Eight MarketTrends.
- For all non-intentionally-insufficient PriceTrend trends, 250/250 global and 519/519 asset returns valid (except FILTERED_1h, correctly 1/1 global and 2/2 asset).
- DEFAULT_1h = IMPLICIT_1h for global PriceTrend and all 519 per-asset values.
- BLANK_2h = FULL_2h for global PriceTrend and all 519 per-asset values.
- All 3,116 valid exported asset PriceTrend values match LastRuntimeSummary per-market trend fields exactly (zero differences).
- Thirteen SMS records, seven BTC/five ETH/one SOL; zero foreign matched-trigger messages.

GlobalSetting was Default in raid 2 due flood protection; switched to DIAG_Global_All15AndImplicit in raid 3; remained unchanged and was not reapplied in raid 4.

## Additional issue to investigate: candle-boundary consistency during cold refresh

First raid started at 14:19:06 UTC; all-market historical refresh ended at 14:21:04 UTC, crossing the 14:20 UTC five-minute candle close. Only 142 of 250 global and 296 of 519 asset returns could see the now-expected exact endpoint 14:19:59.999. Some early series ended at 14:14:59.999; 223 assets failed exact-endpoint resolution. Despite 0 fetch failures, the GlobalSetting remained indeterminate during that raid.

Code review found MarketDataService.RefreshAsync captures `refreshStartedUtc` before its asynchronous fetches, but BinanceFuturesAnalyticsRuntime.EvaluateConfiguredMarketTrends uses a new `DateTimeOffset.UtcNow` after the entire refresh to evaluate the common expected endpoint. Consequently a refresh spanning a five-minute close can mix different latest closed-candle endpoints across assets and fail coverage.

**Classification:** credible timing bug/hypothesis supported by code and runtime chronology. Need implement a consistent refresh/evaluation as-of boundary or targeted endpoint reconciliation and test with a controlled cross-boundary fetch. Do NOT mark fixed on the strength of second-raid recovery alone.

## Outstanding acceptance

- This upload does not include local `dotnet build` or `Tests/Phase1MetricWarnings` output; target 75/75 remains not independently validated.
- Futures runtime diagnostics passed; Binance Spot and Binance US remain untested in this upload.
- Monitor browser rendering, positive threshold-crossing SMS OffTrigger deactivation and TrendCurrency=Fiat parity remain unverified.
- Do not start Phase 1D until the outstanding acceptance decisions are resolved.

## Ownership (D-021)

Assistant changes code/reviews failures and authors tests; user runs builds, regression harnesses and TestMode locally. GitHub is for commits and documentation, no automatic builds without explicit request.
