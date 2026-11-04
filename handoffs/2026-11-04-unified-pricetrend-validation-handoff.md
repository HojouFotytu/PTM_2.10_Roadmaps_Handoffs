# PTMagic 2.10 — Unified PriceTrend validation handoff after Binance Futures TestMode

**Date:** 2026-11-04
**Application repository:** HojouFotytu/PTMagic
**Working branch:** phase1/market-data-foundation
**Checked application HEAD:** 8ff8c87900aa6f56c8721444dd11f0885c99ac3d (runtime binary only reports 2.10.0)
**Scope:** Post-Phase1C unified normalized PriceTrend migration; remaining end-to-end verification prior to Phase 1D

## Current validated status

- 70/70 deterministic tests and Release build passed earlier in GitHub Actions run 41836826883; this precedes D-021 and is not a new local test report.
- User-provided Binance Futures deployed TestMode from 2026-11-04 22:47–22:51 KST: three consecutive raids, no ERROR/FATAL, no PT updates. Latest eight normalized trends present and 519/519 eligible COIN assets with valid 1h/2h returns.
- Legacy omitted/blank MarketTrend.Metrics -> normalized PriceTrend; missing trigger Metric -> normalized PriceTrend and legacy relative/absolute relationships; explicit metrics continue to work.
- Global Setting DIAG_Global_All15AndImplicit matched all 15 explicit and three implicit triggers; remained active without switch/reapply in raids 2 and 3.
- 13 SMS entries across BTC/ETH/SOL, with 0 cross-setting descriptions; active settings agree between SMS JSON and LastRuntimeSummary.
- Independent comparison: all 3,116 per-asset PriceTrend values in LastRuntimeSummary match MarketTrendAnalytics exactly. DEFAULT_1h/IMPLICIT_1h (519 assets) and BLANK_2h/FULL_2h (519 assets) are identical, as intended.
- Expected unavailable INSUFFICIENT_8h ATRP/volume metrics fail closed.
- A recurring FILTERED_1h / PriceTrend warning is not attributable to its specific referencing trigger using supplied exports; only BTC/ETH have per-asset filtered values. Other diagnostic warnings involve invalid scope/explicit enablement. Verify diagnostic config before labeling as defect.

## Pending validation before Phase 1D

1. User runs equivalent TestMode on Binance Spot and Binance US; supplies console log and MarketTrendAnalytics, LastRuntimeSummary, SMS summaries.
2. Verify Monitor browser rendering and old Market Analyzer values/column alignment on the migrated architecture; JSON exports only were checked here.
3. Verify legacy TrendCurrency=Fiat behavior if compatibility is required; numerical parity not established.
4. Exercise at least one positive SMS OffTrigger crossing its threshold, including RelativeTrigger compared against activation price. Current evidence shows persistence, not positive deactivation.
5. Reconcile the FILTERED_1h warning with the exact diagnostic settings; ensure excluded symbols fail closed without misleading diagnostics.
6. Don't introduce Phase 1D feature work until remaining acceptance decisions are explicitly resolved.

## Workflow contract D-021 (mandatory)

Assistant implements source changes, reviews code, authors regression tests and fixes failures. User compiles/runs local tests and TestMode. Review user-provided output together. GitHub used for commits and roadmap/handoffs, not new automated builds unless specifically requested. Existing workflow is still present and should be disabled separately if desired.

## References

- Detailed evidence: ../updates/2026-11-04-unified-pricetrend-futures-testmode.md
- Project status: ../STATUS.md
- Prior 70/70 CI evidence: ../updates/2026-11-04-build-regression-70-passed.md
- D-021 ownership: ../DECISIONS.md
- Prior Phase1D readiness handoff: 2026-11-04-phase1d-correlation-ready.md
