# PTMagic 2.10 — Phase 2 open-interest deterministic validation

**Date:** November 10, 2026 (KST)  
**Exact tested application source:** `5f51faaa0db928cf33c52f6f93ca6f1b301735fb`  
**Application branch:** `HojouFotytu/PTMagic` / `phase1/market-data-foundation`  
**Environment:** Windows PowerShell, .NET SDK `10.0.403`  
**Source:** User-provided full console output of `Tests/Phase2OpenInterestIncremental/Run-Phase2Validation.ps1`.

## Result

**PASS — solution build and 15/15 harnesses; 315/315 reported deterministic test groups.** Build succeeded in **11.3 seconds**; Core, PTMagic, and Monitor compiled successfully for net10.0. The build is attributed only to the exact tested source above, not to any later documentation commits.

| Harness | Passed test groups |
|---|---:|
| Phase2OpenInterest (raw mapping) | 18 |
| Phase2OpenInterestIncremental (acquisition/cache/metrics) | 17 |
| Phase1AReadiness | 5 |
| Phase1AnalyticsReliability | 16 |
| Phase1COhlcv | 13 |
| Phase1DCorrelation | 21 |
| Phase1MetricWarnings | 18 |
| Phase1SmsSummaryIsolation | 5 |
| Phase1TriggerLogic | 29 |
| NormalizedPriceTrendMigration | 18 |
| NormalizedWarmStartCache | 8 |
| TriggerConfigurationValidation | 40 |
| MonitorSettingsRoundTrip | 28 |
| ConfigurationLifecycle | 66 |
| DecisionHistory | 13 |
| **Total** | **315** |

Two previously existing test projects printed nonfatal nullable-analysis warnings: two `CS8600/CS8602` in `Phase1SmsSummaryIsolation` and six `CS8625/CS8629/CS8602` in `NormalizedPriceTrendMigration`. No harness failed; no runtime compilation errors remained after `5f51faa` removed an invalid `await` from a synchronous test assertion.

## Acceptance boundary

- **Accepted at tested source:** solution compilation; both new Phase 2 OI offline harnesses; affected legacy deterministic regressions. The OI test coverage includes user-configured MarketTrend-derived history, longer-than-72h requirements, exact endpoints, independent native quantity/value semantics, budgeted and incremental acquisition, cache restart/corruption, scope isolation and unavailable-source handling.
- **Not established by these tests:** any live Binance OI endpoint behavior, provider history continuity or real rate-limit conditions; ordinary configured PTMagic raids using OI metrics; Monitor/browser rendering; native ProfitTrailer API acknowledgements.
- **Previously deferred separately:** the outstanding Phase 1 configured integration acceptance (specific runtime, PT/SOM, Monitor/browser, Spot/US and restart tests), per D-042 clarified by D-045. That deferral never applied to normal Phase 2 development testing.

## Consequence for the implementation queue

**Phase 2 open-interest deterministic acceptance is complete at `5f51faaa0db928cf33c52f6f93ca6f1b301735fb`.** Its live/provider-specific acceptance remains pending as a separate integration gate. Proceed with the next planned Phase 2 derivatives family: *funding-rate source acquisition and normalization* with its own source-specific requirements, exact timestamps, explicit metric selection, bounded requests, and fresh offline tests. The policy that all data history is derived from the user's enabled MarketTrends (and metric lookbacks) remains active. Do not reintroduce an independent fixed retention-hours setting.

No change to exchange-facing runtime, user analyzer configuration or trading state was made by recording this result.
