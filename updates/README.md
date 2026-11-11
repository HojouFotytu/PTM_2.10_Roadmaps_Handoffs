## Latest November 11 dashboard investigation

**[Dashboard refresh history, PBL rollback, and current Monitor state](2026-11-11-dashboard-refresh-history-and-current-state.md)**

The PBL/dashboard experiment was fully reverted to exact pre-change file blobs. The original DashboardTop jQuery `.load()` mechanism remains in place, but the user still reports stale PBL/Positions data. Git history identifies the November 2 callback-dependent polling rewrite and tooltip/color operations before request-flag reset as concrete code-level risks; runtime cause remains unconfirmed. The owner requires the proposed fix to be explained before source edits. The compact PBL count card is not implemented; zero again hides the full Possible Buys card.

## November 11 — Phase 2 derivative persistence offline validation PASS

**[Phase 2 derivative persistence: 378 checks passed at 86fa4c9](2026-11-11-phase2-derivative-persistence-offline-validation.md)**

The user ran the existing 17-harness PowerShell validation runner at exact application source `86fa4c9a306f7eb61742c26bbb1ae633bb775a2a`. The .NET 10.0.403 solution build passed in 10.3 seconds and all 17/17 harnesses passed: **378 checks total**. Funding and ratio complete restart, partial-range resume across restarts, and corrupt-cache replacement tests all passed. Eight nonfatal nullable warnings remain in two existing test projects. Configured two-startup runtime acceptance and live Binance/PT/Monitor checks remain pending.

# PTMagic 2.10 — Dated implementation and evidence updates

## Latest user-local verification

**[November 7 — Completed deterministic validation: 272 passing checks across two recorded runs](2026-11-07-completed-harness-validation.md)**

At exact source `d331fbd`, Core, PTMagic, and Monitor built successfully with SDK 10.0.403 in 10.9 seconds. ConfigurationLifecycle passed all 66 checks and DecisionHistory passed all 13. Combined with the earlier 193 passes in ten harnesses at `86c2ea3`, all 272 current checks now have passing results. Production code and assertions were unchanged between those two revisions; this is combined evidence, not a single twelve-project run. Configured runtime, actual PT API, and browser acceptance remain open.

The same record includes the subsequent runtime report: a process using the existing runtime working directory still executes older Core behavior and repeats the bare-USDT failure after a setting transition. Its actual running SHA and loaded DLL path are unknown. Explicitly selecting the freshly built DLL with the existing TestMode configuration is now the immediate next step; a checkout build alone does not establish which binary the installed launcher selects.

## Current implementation checkpoint

**[November 7 — Stabilization, correlation, and documentation reconciliation](2026-11-07-stabilization-correlation-implementation.md)**

Source implementation and deterministic execution are complete for the current twelve-harness inventory. Main-market/bootstrap, lifecycle, and decision-history checks now join the earlier validator, Monitor round-trip, analytics, and correlation passes. Subsequent application README updates record this evidence without changing executable code. Use the [current handoff](../handoffs/2026-11-07-stabilization-correlation-validation.md) for the next configured TestMode run and the retained full regression reference, and [current status](../STATUS.md) for the remaining acceptance boundaries. Documentation-only updates do not require repeating the successful harnesses.

The current checkpoint incorporates the user's direct global SOM API revision. Its fake-transport lifecycle checks pass; actual PT acknowledgement and native buy/DCA/sell behavior still need configured integration evidence. The earlier full-preset startup overlay is superseded by [D-037](../DECISIONS.md#d-037--direct-global-som-api-supersedes-the-startup-preset-overlay).

## Earlier November 7 verification

[The 193-check run at `86c2ea3`](2026-11-07-193-check-validation.md) preserves the successful build and ten harnesses, observed lifecycle compiler error, and source-reviewed matching history fixture error. The successful `d331fbd` continuation resolves both remaining harnesses without rewriting that prior record.

[Successful build and partial harness validation at `78967a7`](2026-11-07-build-and-partial-harness-validation.md) preserves the earlier build, 125 passes in eight completed harnesses, failed volume-cap fixture, and separate runtime bootstrap abort without an exact source SHA. The latest result resolves that fixture failure; it does not establish successful configured startup, SOM enforcement, or normal delivery.

## Last accepted pre-change runtime evidence

[November 5 — Nine-raid Futures USDT TestMode](2026-11-05-price-compatibility-nine-raid-testmode.md) records the latest pre-change runtime evidence associated with the 88-check baseline. Source provenance was inferred from the preceding workflow. TestMode sent no PT writes; non-USDT, Spot/US, sustained SMS removal, and specific browser/PT checks remain separately open.

## Historical November 5 records

These records preserve the state at their date. Later acceptance resolves earlier pending statements only within the tested scope.

- [PTMagic 2.10 — PriceTrend compatibility restoration handoff](2026-11-05-pricetrend-compatibility-restoration.md)
- [PTMagic 2.10 — PriceTrend compatibility live Binance Futures evidence](2026-11-05-price-compatibility-nine-raid-testmode.md)
- [PTMagic 2.10 — Pinned refresh time for normalized candles](2026-11-05-pinned-refresh-boundary-fix.md)
- [PTMagic 2.10 — Pinned candle boundary fix verified on Binance Futures](2026-11-05-pinned-boundary-fix-futures-verified.md)
- [PTMagic 2.10 — Option C warning live TestMode validation](2026-11-05-option-c-testmode-validation.md)

## Historical November 4 records

The earlier architectural stages, validation results, and optional optimization proposal remain historical. Current decisions supersede legacy-path and performance-order instructions.

- [PTMagic 2.10 — Local verbose metric warning TestMode verification](2026-11-04-verbose-warning-four-raid-testmode.md)
- [PTMagic 2.10 — Verbose normalized metric-warning diagnostics](2026-11-04-verbose-metric-warning-diagnostics.md)
- [PTMagic 2.10 — Unified normalized PriceTrend: Binance Futures TestMode evidence](2026-11-04-unified-pricetrend-futures-testmode.md)
- [2026-11-04 — D-017 build and deterministic test verification](2026-11-04-tristate-test-results.md)
- [2026-11-04 — Three-valued normalized trigger logic](2026-11-04-three-valued-trigger-logic.md)
- [2026-11-04 — Optional cross-raid historical snapshot reuse](2026-11-04-snapshot-reuse-optimization.md)
- [2026-11-04 — SMS summary list-isolation regression verification](2026-11-04-sms-summary-test-verification.md)
- [2026-11-04 — SMS summary list-sharing defect corrected in source](2026-11-04-sms-summary-alias-fix.md)
- [2026-11-04 — Deployed post-fix SMS TestMode reused historical snapshots](2026-11-04-sms-postfix-retained-snapshots.md)
- [2026-11-04 — Selective legacy PriceTrend calculation refactor](2026-11-04-selective-legacy-price-trend.md)
- [2026-11-04 — Compact RAID SUMMARY metric warnings](2026-11-04-raid-metric-warnings.md)
- [2026-11-04 — D-018 raid warning verification](2026-11-04-raid-metric-warnings-verification.md)
- [2026-11-04 — Phase 1C source implementation checkpoint](2026-11-04-phase1c-source-implementation.md)
- [2026-11-04 — Phase 1C Monitor metric content verified](2026-11-04-phase1c-monitor-verified.md)
- [2026-11-04 — Phase 1C live TestMode results](2026-11-04-phase1c-live-testmode-validation.md)
- [2026-11-04 — Phase 1C DONE: verified live SMS list isolation](2026-11-04-phase1c-final-closeout.md)
- [2026-11-04 — Phase 1C timeframe design correction](2026-11-04-phase-1c-timeframe-correction.md)
- [2026-11-04 — Phase 1A closeout and Phase 1C start gate](2026-11-04-phase-1a-closeout.md)
- [PTMagic 2.10 — Option C natural-language metric warnings](2026-11-04-option-c-natural-metric-warnings.md)
- [2026-11-04 — Tracker setup and authoritative version boundary](2026-11-04-initial-import.md)
- [PTMagic 2.10 — CoinMarketCap and legacy PriceTrend cleanup](2026-11-04-cmc-legacy-pricetrend-cleanup.md)
- [PTMagic 2.10 — Build/regression verification attempt](2026-11-04-build-regression-attempt.md)
- [PTMagic 2.10 — Release build and regression verification SUCCESS](2026-11-04-build-regression-70-passed.md)
- [2026-11-04 — Display all distinct RAID SUMMARY metric warnings](2026-11-04-all-metric-warnings.md)
- [2026-11-04 — D-018 all-warnings display verification](2026-11-04-all-metric-warnings-verified.md)

## Recordkeeping

Dated update files are historical snapshots. Add a later correction or acceptance record instead of rewriting a prior observation. Update README, STATUS, DECISIONS, and the sole current handoff when new evidence changes the present state.

A source commit and an authored test are not passing execution evidence. Report the actual source/binary identity, environment, check, and observed result. Personal strategy work remains outside this index.

[Update template](TEMPLATE.md) · [Pre-reconciliation index snapshot](../history/2026-11-07-pre-reconciliation/updates-README.md)
