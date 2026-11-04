# PTMagic 2.10 — Unified normalized PriceTrend: Binance Futures TestMode evidence

Date: 2026-11-04
Exchange actually tested: Binance Futures (USDT)
Application branch: HojouFotytu/PTMagic / phase1/market-data-foundation
Application repository HEAD observed separately: 8ff8c87900aa6f56c8721444dd11f0885c99ac3d
Running binary identifies itself as PTMagic 2.10.0; uploaded runtime logs do NOT embed a source Git SHA, so the precise binary-commit relationship cannot be independently established.

## Submitted evidence

User uploaded three runtime JSON exports and a local Windows TestMode console log:
- LastRuntimeSummary(5).json
- MarketTrendAnalytics(5).json
- SingleMarketSettingSummary(5).json
- Pasted text(20261104-135145).txt

All files are user-provided runtime evidence, not a new CI build or local test harness report.

## Confirmed TestMode observations

- ProfitTrailer connectivity check succeeded; TestMode explicitly enabled and no PT configuration update sent.
- Three consecutive raids, first 2m06s (cold refresh), second 18s, third 2s; no ERROR/FATAL lines in supplied log.
- Initial normalized ingestion 756/756 futures markets, 872,424 candles, zero fetch failures. Steady-state second raid 2,268 candles, then third 87 candles across 29/756 markets (727 current/skipped).
- Analyzer classification: 519 COIN eligible of 756 USDT exchange markets; no EQUITY assets contributed normalized metrics.
- Eight configured MarketTrends evaluated. Seven exposed PriceTrend, with valid global 250/250 and asset 519/519 for unfiltered trends. FILTERED_1h had global BTC only (1/1) and per-asset BTC/ETH (2/2).
- DEFAULT_1h == IMPLICIT_1h global normalized PriceTrend, and all 519 matching per-asset PriceTrends were exactly equal.
- BLANK_2h == FULL_2h global normalized PriceTrend, and all 519 matching per-asset PriceTrends were exactly equal.
- All 3,116 exported asset PriceTrend entries over seven trends matched their corresponding LastRuntimeSummary.MarketSummary fields with zero numeric difference (six full trends at 519 each plus two filtered entries).
- GlobalSetting DIAG_Global_All15AndImplicit matched all 15 explicit FULL_2h global metric checks and three implicit PriceTrend checks. It switched during raid 1 and was retained without switching or reapplication on raids 2 and 3.
- 13 SMS snapshots persisted across BTC (7), ETH (5), SOL (1); 10 had new activation timestamps in raid 2, three were retained from raid 1. Every snapshot's MatchedTriggersContent contained its own setting prefix only: 0/13 cross-setting contamination.
- BTC diagnostic SMS activated for omitted-metric DEFAULT_1h, blank-metrics BLANK_2h, implicit dependency IMPLICIT_1h, filtered PriceTrend, 24h-volume-only, and true-OR-unavailable.
- The ETH SMS with unavailable OffTrigger was retained, consistent with fail-closed persistence. BTC RelativeTrigger exit and ETH implicit OffTrigger persistence were observed, but not a threshold-crossing deactivation.
- FULL_2h exposed all 15 global metrics; expected INVALID / INSUFFICIENT_8h metrics remained unavailable rather than zero.

## Seven recurring metric warnings: interpretation

1. FILTERED_1h / PriceTrend: no calculated value for a particular reference. The trend itself has valid global and BTC/ETH asset metrics. A reference to an outside-population market can explain the warning, but the exact calling trigger is not identified by these exports.
2. FULL_2h / ATRP: asset-scope metric invalid in GlobalSetting context. Correct rejection.
3. IMPLICIT_1h / PriceTrend: explicit reference rejected because the metric is not enabled in the MarketTrend metric list, even though blank-Metric triggers correctly request it implicitly. Diagnostic behavior should be cross-checked against test settings.
4–7. INSUFFICIENT_8h: ATRP (519/519 assets), MedianATRP (0/250), MedianVolumeExpansion (0/250), VolumeExpansion (519/519 assets) unavailable due missing 8h period history (11/15 or 11/21 complete periods); expected with 96h retention.

No source defect is established by these warnings. Do not silently mark them resolved; the FILTERED_1h warning source remains unattributed without the exact analyzer settings configuration.

## Acceptance

- Binance Futures normalized PriceTrend and backwards-compatible implicit trigger behavior: verified in user's deployed TestMode artifacts for the tested settings.
- Existing summary export fields and SMS description isolation: verified in supplied snapshots.
- Binance Spot and Binance US TestMode: NOT RUN in provided evidence.
- Monitor browser rendering: not directly inspected in this upload; JSON export compatibility verified only.
- TrendCurrency=Fiat numerical equivalence: not verified.
- Explicit OffTrigger threshold-crossing deactivation: not verified.
- A separate user-local dotnet build/test output was not supplied in this upload. Prior 70/70 GitHub CI results are historical and are not represented as new local tests.
- Outstanding end-to-end #4 stays PARTIAL (1/3 exchange environments tested).

## Development process (D-021)

Assistant handles source changes, code review, and regression test authoring/fixes. User runs local .NET builds, regressions and TestMode. Assistant analyzes user-provided logs. Do not enable automatic GitHub builds/tests unless explicitly requested.
