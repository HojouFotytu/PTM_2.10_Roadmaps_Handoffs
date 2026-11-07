# November 7, 2026 — Completed deterministic validation across twelve harnesses

**Application repository:** HojouFotytu/PTMagic

**Continuation source:** `d331fbd059041241069646c3bb82ac6549423a70`

**Earlier ten-harness source:** `86c2ea3ff430b62e654f929a222935ec53ea8fa6`

**Branch:** `phase1/market-data-foundation`

**Execution:** User-local PowerShell under D-021, .NET SDK 10.0.403

## Observed continuation

The user supplied the complete successful continuation output. The checkout fast-forwarded from `86c2ea3` to `d331fbd`, and the script confirmed the exact expected source. **Core, PTMagic, and Monitor built successfully in 10.9 seconds. ConfigurationLifecycle then passed all 66 checks and DecisionHistory passed all 13.** The fail-fast block reached its successful completion message.

The previous run at `86c2ea3` had already passed 193 checks in the first ten harnesses. The only executable changes before this continuation were the two fully qualified Telegram fixture constructors; production source and assertions did not change. Three accompanying README edits recorded the earlier evidence.

**All 272 current checks across twelve projects therefore have passing results across these two recorded revisions.** This is combined execution evidence, not a claim that all twelve projects ran at `d331fbd` in one sequence.

## Results and exact provenance

| Harness | Passing checks | Executed source |
|---|---:|---|
| Phase1AReadiness | 5 | `86c2ea3` |
| Phase1COhlcv | 13 | `86c2ea3` |
| Phase1SmsSummaryIsolation | 5 | `86c2ea3` |
| Phase1TriggerLogic | 29 | `86c2ea3` |
| NormalizedPriceTrendMigration | 18 | `86c2ea3` |
| Phase1MetricWarnings | 18 | `86c2ea3` |
| Phase1AnalyticsReliability | 16 | `86c2ea3` |
| Phase1DCorrelation | 21 | `86c2ea3` |
| TriggerConfigurationValidation | 40 | `86c2ea3` |
| MonitorSettingsRoundTrip | 28 | `86c2ea3` |
| ConfigurationLifecycle | 66 | `d331fbd` |
| DecisionHistory | 13 | `d331fbd` |
| **Total** | **272** | **Two recorded revisions** |

## What the continuation establishes

The 66 lifecycle checks passed for exact main-market parsing, preservation of non-USDT quotes, invalid/missing input rejection, null-group inheritance, fresh-summary bootstrap, guard retention on invalid bootstrap, and all three exchange adapters' identity and input boundaries. Exchange-boundary fixtures use already-canceled tokens; they did not collect live exchange data.

The same harness passed production-component cases for desired/pending/confirmed configuration state, failed and partial delivery, unchanged-payload suppression and retry, encoded SOM API requests and context paths, multi-target tokens and acknowledgements, rejection and timeout handling, startup enable/configuration/release ordering, freshness checks, restart/opt-out state, TestMode isolation, final SMS removal, same-name reload, and unavailable age/volume/off-trigger inputs. ProfitTrailer transport was injected/faked. These results verify the tested logic and HTTP request handling without establishing an actual PT server acknowledgement or trade restriction.

The 13 history checks passed for independently parseable appends, UTC-date and size rotation, retention and quota pruning, interrupted tails, oversized-record rejection, invalid bounds, metadata-only checkpoints, TestMode checkpoint isolation, actual raid capture with distinct RelativeTrigger inputs, failed-raid single-write history with credential exclusion, and disabled-history behavior. The bounded-file fixtures used temporary storage.

The earlier 40-check validator result and 28-check Monitor round-trip result remain tied to `86c2ea3`. The prior namespace compiler error and invalid finite-volume fixture are resolved by their subsequent successful executions. The [193-check report](2026-11-07-193-check-validation.md) and [earlier partial-validation report](2026-11-07-build-and-partial-harness-validation.md) remain unchanged as historical evidence.

## Subsequent configured-runtime report: runtime Core is still older

After the successful continuation, the user supplied another runtime log and reported the same error. Its working directory is the existing configured runtime folder, separate from the Git checkout used for the builds and harnesses. The loaded DLL path is not provided; working directory alone does not establish assembly location.

The first raid loaded the default properties, completed, and reported a switch to a non-default setting. The next raid loaded 13 PAIRS, 12 DCA, and 11 INDICATORS lines, then requested `ticker/24hr?symbol=USDT`, received Binance's invalid-symbol response, logged an empty main market, and aborted. Both raids omit the current code's unconditional `Source revision` and `Analysis main market` lines; their stack locations follow the older code layout. The executed Core code therefore predates the validated fixes. Its exact running SHA is unknown, and the version 2.10.0 label cannot identify it as `d331fbd` or the current documentation checkpoint.

Current main-market normalization rejects an empty quote before exchange I/O, while a valid USDT quote uses an identity price. The bare-USDT HTTP request is inconsistent with that corrected path. The first successful raid in the supplied log does not establish acceptance of the updated bootstrap implementation.

The supplied runtime log lacks the TestMode banner and reports `PT Config updated: Yes` after its first raid. That is the old runtime's reported behavior, not evidence that the new global SOM, confirmation, or release logic reached ProfitTrailer. No raw runtime log, private deployment path, credentials, or personal strategy preset is included in this public evidence record.

## Remaining acceptance and next action

The successful build and harness results remain valid for their recorded checkout sources. They do not establish which binary an existing launcher selects. The next step builds the pinned checkout and launches its absolute `PTMagic.dll` path with the existing runtime working directory and TestMode configuration, then verifies `Source revision`. This directly selects the updated application and its matching dependencies without copying or overwriting the existing private configuration/state. It does not claim that the installed launcher has been updated permanently.

Use the explicit-DLL TestMode procedure in the [current handoff](../handoffs/2026-11-07-stabilization-correlation-validation.md). Capture startup and two consecutive completed raids, confirming the intended `Analysis main market` in both, because the reported failure appeared on the raid after an initially successful setting transition. Provide the current runtime summaries/analytics with those logs. Before reusing the installed launcher, update its coherent application bundle while preserving private files; replacing only Core.dll can mix incompatible application versions. Actual PT API acknowledgement/native SOM enforcement and browser checks remain separate. Application README updates that record the passing tests do not change executable code or require another harness rerun.

The existing Phase 2 onward scope, performance deferral until all approved new metrics are complete, and exclusion of personal strategy work are unchanged.
