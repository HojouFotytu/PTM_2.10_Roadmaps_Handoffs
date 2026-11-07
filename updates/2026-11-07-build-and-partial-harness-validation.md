# November 7, 2026 — Successful build, partial harness results, and a separate runtime failure

**Application repository:** HojouFotytu/PTMagic

**Validated source:** `78967a7703ab9f57fece40d488fc538b1caf393b`

**Execution:** User-local PowerShell verification under D-021

## Result and scope

The user supplied exact-source validation output for the Razor correction. **Core, PTMagic, and Monitor built successfully with .NET SDK 10.0.403 in 9.6 seconds.** This confirms that the Monitor compilation blocker was resolved at the source above; Monitor browser save/reload behavior still needs separate verification.

The first eight harnesses completed successfully with **125 passing checks**. The ninth harness, TriggerConfigurationValidation, printed 23 PASS results and then failed its 24th case. The fail-fast sequence stopped, so the remaining three harnesses did not run. The full regression set is not accepted.

## Recorded harness results

The expected counts below describe the validated source, whose authored inventory was 260 check groups across twelve projects. They are not a claim that all 260 passed.

| Project | Expected groups at this source | Observed result |
|---|---:|---|
| Phase1AReadiness | 5 | 5/5 passed |
| Phase1COhlcv | 13 | 13/13 passed |
| Phase1SmsSummaryIsolation | 5 | 5/5 passed |
| Phase1TriggerLogic | 29 | 29/29 passed |
| NormalizedPriceTrendMigration | 18 | 18/18 passed |
| Phase1MetricWarnings | 18 | 18/18 passed |
| Phase1AnalyticsReliability | 16 | 16/16 passed |
| Phase1DCorrelation | 21 | 21/21 passed |
| TriggerConfigurationValidation | 38 | 23 PASS results, then failure at case 24 |
| MonitorSettingsRoundTrip | 28 | Not run; fail-fast sequence stopped |
| ConfigurationLifecycle | 56 | Not run; fail-fast sequence stopped |
| DecisionHistory | 13 | Not run; fail-fast sequence stopped |

The failing case is **“timed and volume off-triggers need no trend.”** Validation rejected OffTrigger #2 for a missing MarketTrend with an empty name. The 23 earlier PASS results are partial output from a failed harness, separate from the 125 checks in the eight completed harnesses.

Nullable warnings appeared in Phase1SmsSummaryIsolation and NormalizedPriceTrendMigration. Both harnesses passed; those warnings were not the terminating failure.

## Separate runtime excerpt without an exact source SHA

The application excerpt reports version **2.10.0**, without a source SHA. It shows a Binance Futures 24-hour ticker request with `symbol=USDT`, followed by a blank `MainMarket` and an aborted raid. This records a runtime failure, but it cannot be assigned to the exact source validated above.

The reported PTMagic stack locations, 897 and 1308, match the earlier `d0b0b87` baseline, and the excerpt lacks the current startup `Source revision` line. This suggests that an older binary was still running. That is an inference from the trace and missing provenance, not identification of the deployed commit.

Configured startup and raid acceptance remain open. The excerpt does not establish successful global SOM enforcement, normal configuration delivery, or guard release.

## Follow-up source review and corrections

The failing validation fixture used `Constants.Max24hVolume - 1`, with `Constants.Max24hVolume` equal to `double.MaxValue`. That subtraction rounds back to the same unbounded sentinel, so production validation correctly required a trend reference. The fixture now uses a finite cap of 1,000. Two added checks distinguish the adjacent representable value below the sentinel from the exact sentinel. Production validation is unchanged; the revised TriggerConfigurationValidation inventory is 40 authored checks awaiting execution.

The bootstrap corrections preserve inherited default-file assignments when a setting's property group is null, read the exact `market` property, normalize its asset code, and reject missing or malformed values before exchange I/O. They add a log identifying the resolved main market and selected setting. Direct adapter inputs are validated before network access, and USDT price conversion uses the identity value 1 without a ticker request. No silent USDT fallback is introduced.

Ten added lifecycle groups cover these bootstrap, inheritance, identity, and invalid-input boundaries, bringing ConfigurationLifecycle to 66 authored groups. Together with the two validator additions, the next source has **272 authored groups across the same twelve projects**. These added cases are unexecuted; the 260-group table above remains the inventory for the source actually tested.

These follow-up corrections are published at the source pinned in the [current handoff](../handoffs/2026-11-07-stabilization-correlation-validation.md). Their complete build and harness run remain required, along with the separate configured runtime checks. Restart the updated configured instance, capture its `Source revision` line, and verify a valid `market` assignment in its compiled PAIRS settings; for the user's USDT setup, that assignment is `market = USDT`.

The November 5 build, 88-check baseline, and nine Futures USDT TestMode raids remain historical evidence for their recorded scope. This newer build and partial regression result do not turn unexecuted lifecycle, Monitor, or decision-history harnesses into passes.
