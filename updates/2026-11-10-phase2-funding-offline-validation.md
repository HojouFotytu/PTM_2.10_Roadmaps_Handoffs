# PTMagic 2.10 — Phase 2 funding offline validation evidence

**Review date:** November 10, 2026 (KST)  
**Exact tested application SHA:** `49f2aab66592b6e2922097ca5242b5a614090602`  
**Application branch:** `phase1/market-data-foundation`  
**Test environment:** Windows PowerShell; .NET SDK **10.0.403**  
**Evidence:** User-supplied complete output of `Tests/Phase2OpenInterestIncremental/Run-Phase2Validation.ps1` (232 lines).

## Outcome: PASS

**Full solution .NET build:** Core, PTMagic and Monitor net10.0 all succeeded; build completed in **11.0 seconds**.

**16 of 16 offline harnesses passed, containing 332 of 332 test case groups.**

| Harness | Passed |
|---|---:|
| `Phase2Funding` | 17 |
| `Phase2OpenInterest` | 18 |
| `Phase2OpenInterestIncremental` | 17 |
| `Phase1AReadiness` | 5 |
| `Phase1AnalyticsReliability` | 16 |
| `Phase1COhlcv` | 13 |
| `Phase1DCorrelation` | 21 |
| `Phase1MetricWarnings` | 18 |
| `Phase1SmsSummaryIsolation` | 5 |
| `Phase1TriggerLogic` | 29 |
| `NormalizedPriceTrendMigration` | 18 |
| `NormalizedWarmStartCache` | 8 |
| `TriggerConfigurationValidation` | 40 |
| `MonitorSettingsRoundTrip` | 28 |
| `ConfigurationLifecycle` | 66 |
| `DecisionHistory` | 13 |
| **Total** | **332** |

The new funding family passed **17/17**, and OI retained **35/35** (18 raw, 17 incremental). The remaining **280/280** cases passed in previously existing PTMagic regression harnesses. This is separate from the earlier OI-only 315/315 result at `5f51faaa`.

### Warnings and remaining acceptance

Two previously existing test projects produced eight nonfatal C# nullable warnings: `Phase1SmsSummaryIsolation` (CS8600, CS8602) and `NormalizedPriceTrendMigration` (CS8625×3, CS8629×2, CS8602). No compilation failure or test failure appeared.

The tested SHA is **one commit ahead of the preceding funding application checkpoint** `1b67fc2`; that additional commit modifies the Monitor Global Settings Log activation-trigger capture/display, associated models and the application changelog. The **solution including that source compiled** and the existing MonitorSettingsRoundTrip tests passed (28/28). The new Monitor display itself has **not** been independently browser-accepted by this console run.

The test runner explicitly reports that it makes **no live Binance/provider requests, no configured PTMagic raids, and no native PT API actions**. Accordingly, the result accepts funding/OI **deterministic source and regression correctness**, not exchange availability, production refresh/performance, GUI behavior or PT API acknowledgement.

Per D-045, ordinary Phase 2 development testing is required and this checkpoint satisfies the recorded offline build/regression gate. Only the previously identified remaining **Phase 1 configured integration** acceptance is deferred; do not describe new Phase 2 unit tests as deferred.

## Next work

Proceed to Phase 2 **global account and top-trader account/position long-short ratios**, maintaining distinct provider units, exact timestamps, MarketTrend-derived data requirements, bounded acquisition and offline fixture tests. Continue later with taker flow and Phase 2B aggregates. Live provider-specific acceptance remains an independent gate to document and complete when appropriate; it must not be falsely labeled PASS.

The test evidence and this documentation commit did not modify runtime configurations or any trading settings.
