# November 10, 2026 — SOM safety and Monitor metrics offline validation

**Verified application source:** `fb94373d8928b681e3ebe1f7209bd1439db42e72`  
**Application branch:** `phase1/market-data-foundation`  
**Environment:** Windows PowerShell, .NET SDK `10.0.403`  
**Scope:** deterministic offline development tests only, no live Binance, actual PT API or Monitor browser acceptance.

## User-executed evidence

Two independent full validation executions at the identical source SHA:

| Run | Solution build | Offline harnesses | Test groups | Warnings |
| --- | --- | --- | --- | --- |
| First | PASS (15.6s), Core/PTMagic/Monitor | 16/16 PASS | 337/337 PASS | Eight nonfatal pre-existing nullable reference warnings in two test projects |
| Second | PASS (10.3s), Core/PTMagic/Monitor | 16/16 PASS | 337/337 PASS | None displayed by second output (incremental compile) |

Both runs used the repository's checked-in `Tests/Phase2OpenInterestIncremental/Run-Phase2Validation.ps1` and recorded the exact source SHA.

### Validated harness inventory

| Harness | Passing groups |
| --- | ---: |
| Phase2Funding | 17 |
| Phase2OpenInterest | 18 |
| Phase2OpenInterestIncremental | 17 |
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
| ConfigurationLifecycle | 71 |
| DecisionHistory | 13 |
| **Total** | **337** |

### Specific newly accepted changes

- **SOM enable-only safety:** The ConfigurationLifecycle PASS set covers explicit global SOM disable rejection, never automatically calling `enabled=false` after delivery or on startup/restart/opt-out paths, checkpoint migration to manual review, uncertain enable/partial-target failure behavior, and TestMode no-command isolation.
- **Startup Monitor notice:** Source-level ticker regression assertions passed for the red `PT: SOM` warning during raids 1 and 2, disappearance from raid 3, and manual release messaging. The ticker does not read PT's authoritative live SOM state.
- **Global Settings Log:** The two new tests passed for capture of every applicable configured **global** market metric at activation, trigger-set membership highlighting regardless of FALSE/TRUE, unavailable values distinguished from numeric zero, and immutability after analytics changes.
- **Market Metrics:** The History Requirements **UI panel** was deleted without changing actual metric/history computations. Monitor solution compilation passed; no separate browser rendering test was performed.

### Warnings and limits

The first run logged eight compiler warnings in previously existing test fixtures:

- `Tests/Phase1SmsSummaryIsolation/Program.cs`: CS8600, CS8602.
- `Tests/NormalizedPriceTrendMigration/Program.cs`: CS8625 ×3, CS8629 ×2, CS8602.

The second full invocation produced no warnings in its output. Neither run reported a build or test failure. A clean rebuild may repeat the existing nullable warnings; they do not block acceptance.

**Not accepted by these runs:** live provider data availability, production Binance history collection, active PTMagic raids with live configurations, actual ProfitTrailer REST actions, Monitor page/browser rendering, and other previously deferred specific configured integration checks. No claim of live SOM readback or automatic release.

## Next work

Proceed to **Phase 2 Futures long/short ratio families**: distinguish global account ratio, top-trader account ratio, and top-trader position ratio. Preserve opt-in metrics, correct source mapping, bounded requests, history readiness, unavailable semantics, and new deterministic tests. Keep source changes on the existing `phase1/market-data-foundation` branch; no new branch or duplicate candidate path without asking.

The user does **not** need to repeat the already completed 337/337 offline suite for this accepted source as a prerequisite to starting the next development batch.

[Current roadmap](../roadmaps/CURRENT.md) · [Status](../STATUS.md) · [Active handoff](../handoffs/2026-11-10-som-enable-only.md).
