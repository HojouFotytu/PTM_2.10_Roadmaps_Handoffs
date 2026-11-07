# November 7, 2026 — Stabilization, correlation, and current-roadmap reconciliation

**Application repository:** HojouFotytu/PTMagic

**Branch:** `phase1/market-data-foundation`

**Application source checkpoint:** `86c2ea3ff430b62e654f929a222935ec53ea8fa6`

**Documentation baseline before reconciliation:** `a074fea56f33033c1a99db78df12099ea230a88a`

## Evidence level

Source changes and regression cases were authored and reviewed. The user's subsequent exact-source run at `78967a7` built Core, PTMagic, and Monitor successfully, then completed eight harnesses with 125 passing checks before TriggerConfigurationValidation failed at case 24. The last three harnesses did not run. [The dated validation record](2026-11-07-build-and-partial-harness-validation.md) separates these results from the unpinned runtime excerpt showing a bootstrap abort. Full regression and configured runtime acceptance remain open under D-021.

The accepted pre-change baseline is the November 5 build and 88 checks associated with d0b0b87, followed by nine Futures USDT TestMode raids. The exact deployed SHA was inferred from the workflow; the logs printed application version 2.10.0. Those results remain valid for their recorded scope and do not validate the new source.

## Reported Monitor build failure and correction

The user reported a .NET 10 build in which Core succeeded and Monitor failed with **27 Razor compile errors across nine row-render expressions** in `Monitor/Pages/_get/SettingsGlobalSettings.cshtml` and `Monitor/Pages/_get/SettingsSingleMarketSettings.cshtml`. The submitted log did not include an exact source SHA, so the report does not establish acceptance of a specific revision.

The correction encloses each server-side expression as `@(Html.Raw(...))`. This ends Razor's C# expression before the following JavaScript `.map(...)` and `.join(...)` chain, preserving the serialized row data and client-side rendering behavior. The user subsequently confirmed the compilation correction at `78967a7`: Core, PTMagic, and Monitor built successfully with SDK 10.0.403 in 9.6 seconds. Browser behavior and the complete regression sequence still require acceptance through the [current handoff](../handoffs/2026-11-07-stabilization-correlation-validation.md).

No harness cases were added for the delimiter correction. Its validated source contained **260 authored check groups across 12 projects**. The eight completed harnesses passed 125 checks; another 23 PASS results preceded the failure in the ninth harness. This is partial execution, not a 260-check pass.

## Follow-up fixture and main-market corrections

The reported validator failure was caused by a fixture that subtracted 1 from the double.MaxValue sentinel and therefore retained the same value. The fixture now uses a finite volume cap of 1,000; two added cases test the adjacent representable value and exact sentinel. Production validation remains unchanged.

The bootstrap corrections retain default-file assignments for null property groups, resolve the exact market property, normalize and validate its asset code before exchange I/O, and return the USDT identity price without a ticker request. A new log records the resolved main market and selected setting. The separate runtime excerpt likely came from an older running binary, inferred from baseline stack locations and the missing Source revision line; it does not identify an exact runtime SHA.

The revised inventory is **272 authored check groups across twelve projects**, including 40 validator and 66 lifecycle groups. The twelve added groups have not been executed. The corrections are published at the source checkpoint above. A complete build/harness rerun and a restarted configured instance with its Source revision and compiled market verified remain required. The [dated evidence record](2026-11-07-build-and-partial-harness-validation.md) retains the earlier validated source and counts; [publication status](../STATUS.md#publication-status) records the current source and standing authorization.

## User-directed scope

The user authorized corrections to configuration delivery and SMS lifecycle, Monitor preservation, reference validation, startup handling, acquisition/freshness, history requirements, Concentration semantics, documentation, and verification gaps. The requested continuation includes Phase 1D correlation and a minimal native decision audit.

Before publication, the user rejected the first startup implementation because its full-preset overlay could replace existing live overrides. The accepted replacement is the supplied `POST /api/v2/globalSellOnlyMode` control endpoint with `token` and `enabled` query parameters. The user clarified that native global SOM stops new buys and DCA buys while allowing sells. [D-037](../DECISIONS.md#d-037--direct-global-som-api-supersedes-the-startup-preset-overlay) records this supersession and explicit flag ownership.

The user explicitly moved performance work until after **all approved new metrics** are complete. This includes derivatives and liquidity families, not just Phase 1D. Personal strategy development is an independent project and excluded from PTMagic 2.10 deliverables and release criteria.

## Implementation contracts

| Area | Current contract |
|---|---|
| Last SMS removal | Removal of the final active SMS produces a deliverable configuration change |
| Delivery | Desired, pending, and confirmed states are distinct; failure does not advance confirmation; identical desired configuration is retried |
| Restart/checkpoint | `_data/ConfigurationDeliveryState.json` contains confirmed identity and hash, not the raw PT payload; TestMode does not write it |
| Initial protection | `StartupSellOnlyMode=true` calls the global SOM API with enabled=true before lengthy exchange bootstrap; no PAIRS/DCA/INDICATORS payload is sent for the guard |
| Guard release | Fresh conclusive analysis and normal configuration acknowledgement must precede the separate enabled=false API request; release failure retains normal acknowledgement and pending release |
| Flag ownership | PTM owns the global flag for this enabled startup option; no prior-state readback/restoration is implemented, including when the flag was already true |
| Guard metadata/tokens | `_data/StartupSellOnlyModeState.json` is separate from configuration confirmation; additional tokens use ProfitTrailerServerAPITokenXtra, whose empty default shares the primary token |
| Startup opt-out | No new guard is acquired, but matching pending PTM-owned recovery still completes; indeterminate analysis retains known configuration or defers unknown state without forcing DEFAULT |
| Monitor | Multiple metrics/tags on one trend and supported precision survive the edit/save pipeline |
| Missing references | Configuration validation rejects broken MarketTrend references; defensive evaluation retains unavailable semantics |
| Acquisition and age | Requests preserve the pinned analysis window; `MaxAnalysisAgeSeconds=300` applies to the age of that pin at decision time |
| History requirements | Per-metric reports expose complete-history minimums, current-raid stored slots/retention, all-alignments guidance, configured capacity, and warnings |
| Concentration | Top10 mean return minus remaining-market mean return, in percentage points; rank on the same TrendMinutes trailing volume window; 100% coverage and minimum eleven markets |
| Correlation | CorrelationToBTC, MeanCorrelationToBTC, MedianCorrelationToBTC; Pearson(simple returns), exact synchronized complete endpoints/source observations, N=30 default and 3–1000 range |
| Audit trail | Bounded redacted JSONL at `_data/DecisionHistory/`, enabled by default, 30 days, 256 MiB total, 16 MiB segments |

Correlation missing-data and zero-variance cases are unavailable. Mean/median use 90% coverage of the exact selected global population, including BTC only when selected. No shortened overlap vector or forward fill is allowed.

A metric's legitimate last complete four-hour/daily bar must not be rejected merely because its close is older than the decision-age setting. That setting measures delay since the raid's pinned analysis time.

At a 24-hour trend duration, the default conservative all-alignments history guidance is 384 hours for ATR(14), 528 hours for VolumeExpansion(20), and 744 hours for Correlation(30). The report distinguishes those values from complete-period mathematical lower bounds. Insufficient retention warns and leaves dependent values unavailable; it does not silently resize storage.

## Regression and runtime work

New projects cover correlation, analytics reliability, configuration lifecycle, Monitor settings round trips, and decision history. The existing six projects remain part of the required regression set. Exact project paths and current expected case counts are in the [verification handoff](../handoffs/2026-11-07-stabilization-correlation-validation.md).

The recorded execution is limited to the successful build, eight completed harnesses, and partial output from the failed ninth harness. Environment-specific checks remain necessary for acknowledged PT updates, failed sends, global SOM enable/configuration/release ordering and native enforcement, lasting last-SMS removal, Monitor browser preservation, Spot/US behavior, and non-USDT conversion. The user's endpoint and native-behavior clarification do not establish that the new client/lifecycle has been run successfully.

## Documentation reconciliation

- Prepared a standalone [current technical roadmap](../roadmaps/CURRENT.md) retaining all future derivative, aggregate, state, liquidity, integration, and historical-analysis phases.
- Replaced stale current README, status, decision register, concise roadmap, and navigation with one consistent current contract.
- Explicitly superseded the separate legacy PriceTrend path, CMC/selective-legacy intermediate architecture, removed test-project instructions, old “Phase 1C next” guidance, and performance-before-correlation ordering.
- Preserved earlier mutable documents under [history](../history/README.md).
- Left dated roadmap, handoff, issue, and update files intact as historical evidence.
- Added [issue 003](../issues/003-configuration-lifecycle-and-data-reliability.md) and the [November 7 handoff](../handoffs/2026-11-07-stabilization-correlation-validation.md).

The new status distinguishes intended behavior, source implementation, written tests, actual execution, configured TestMode evidence, and real delivery/browser acceptance. A version label or dated document no longer implies a newer deployed source.

## Next action

Run the complete fail-fast local verification sequence in the current handoff, provide output with the actual commit, then resolve any failing case before recording acceptance. Continue the remaining metric families after current correctness acceptance. Keep the dedicated performance program behind the all-new-metrics completion gate.
