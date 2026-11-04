# P1A-READY — Cold-start cross-sectional completeness

**State:** CLOSED — ACCEPTED CORRECTNESS CONTAINMENT (no longer blocks Phase 1C)
**Date:** 2026-11-04
**Application branch:** `HojouFotytu/PTMagic:phase1/market-data-foundation`
**Last code HEAD inspected:** `89324bc5c8c5ea19ceb543b6ab5130899f2675dc`

## Original observation

A long cold start reported 756/756 successful normalized fetches but only 259/1,434 valid 4h asset metric values. The second raid recovered validity, and a later idle raid required no kline requests. A bootstrap spanning multiple 5m boundaries is a plausible explanation, but **the exact ingestion root cause is not proven**.

## Accepted containment

- `3a2ba0227246ea4bcad91205273575ae04fa4f8e`: normalized global market-wide metrics require at least **90%** of the exact Phase 0-selected eligible universe, rounding required count up. Empty universes are invalid. `Concentration` requires **100%** of the ranked eligible population with complete 24h quote-volume windows.
- Coverage fields (`SampleCount`, `EligibleSampleCount`, `CoveragePercent`) and expected close-time/invalid-reason diagnostics are exposed to runtime and Monitor snapshots. Missing data are not interpreted as zeros.
- `c038a11baff881285317f07f393084624b6bd3ca`: unavailable normalized triggers cannot activate GlobalSettings or negated SMS conditions. If selection is indeterminate and no fully evaluable GlobalSetting matches, retain the current active setting. Independent valid and legacy triggers can still operate.
- `e002801555ffb98e8169e1943aa4a13b05956b52`: four deterministic Phase1AReadiness regression tests.
- `11d6e286b0ed6474d730eb2eba1b6ecb0158a26d`: logging-only separation of GlobalSetting *switched* vs *reapplied*. Runtime log evidence predates this patch.

No forced second raid, extra API requests, normalized ingestion rewrite, trading suspension, or legacy-path change.

## Verification

User ran `dotnet build`: Core, PTMagic and Monitor built successfully on .NET 10. `dotnet run --project Tests/Phase1AReadiness/Phase1AReadiness.csproj`: **4/4 passed**.

| TestMode raid, KST | Normalized refresh | 4h global valid returns | 4h asset metrics | Outcome |
|---|---|---|---|---|
| ~13:30 first raid | 756/756 markets, 654,696 candles | 32/250 (12.8%) | 0/1434 | Invalid metrics rejected; Default retained |
| ~13:31 cleanup | 705/756 markets, 2,115 candles | 249/249 (100%) | 1434/1434 | Recovered |
| ~13:32 idle | 0 kline requests | 249/249 (100%) | 1434/1434 | Current |
| ~13:33 normal selection | 0 kline requests | 249/249 (100%) | 1434/1434 | Switched to DIAG_Global_AllMetrics after flood protection |
| ~13:35 5m boundary | 756 markets, 2,268 candles | 249/249 (100%) | 1434/1434 | Incremental update |

The first raid recorded `MissingEndpoint=218` for 4h global returns. Actual PT settings were not sent because TestMode was enabled.

## Deferred, non-blocking verification

- [ ] Test **non-default** GlobalSetting retention across a later below-90% coverage episode. Only `Default` retention was exercised in available logs.
- [ ] Runtime-check `Global setting switched` and `Global setting reapplied` wording from commit `11d6e28`.
- [ ] Extend fixtures for stale/partial/sparse/missing intermediate candles and 90–99% coverage; prove bootstrap-endpoint root cause only if future operational symptoms justify further investigation.
- [ ] Align application version labeling (the tested binary reports 2.9.1; development target is 2.10) during release preparation.

## Exit decision

**Phase 1A is DONE by verified containment.** An incomplete first raid is acceptable when it fails closed, preserves valid independent behavior and repairs on the normally scheduled next raid. Move to Phase 1C. This closure does **not** claim the exact original ingest timing mechanism was eliminated.
