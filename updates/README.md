## November 12 — D-053 OI and positioning withdrawal (new scope decision)

The current owner-approved roadmap removes `OpenInterestChange`, `OpenInterestValueChange`, `GlobalLongShortAccountRatio`, their planned cross-market aggregates and OI/positioning-based higher-order conditions. The approved product target is 24 metrics, with funding, future taker-flow/aggregates and liquidity retained. **Application source is not yet changed:** `d101b5a03e01f8f76acf8cc9a6bde7214ff34aa2` remains the user-tested 18/18-harness pre-removal baseline. [Decision](../DECISIONS.md#d-053--remove-binance-futures-open-interest-and-longshort-positioning-metrics-from-ptmagic-210) · [Current roadmap](../roadmaps/CURRENT.md). Older updates remain chronological evidence only.

## November 12 — Binance public global-account ratio boundary fix (validation pending)

**[Live startTime overlap diagnosed; narrow ratio service correction published](2026-11-12-global-account-ratio-boundary-fix.md)**

Live PowerShell data identified a valid extra aligned 5m observation exactly one millisecond before the requested start; strict ratio service validation had rejected it, explaining zero valid histories in the November 12 raids. Application source `6f6da51` ignores only this known overlap and includes focused pagination/cache regressions. **Local .NET build/test and configured recheck are pending**; earlier 386 offline checks at `5a21a48` remain historical evidence.

## November 11 — Adaptive derivative acquisition offline validation PASS

**[D-051 adaptive acquisition: 18/18 harnesses, 386 checks PASS](2026-11-11-derivative-adaptive-acquisition-implementation.md)**

At source `5a21a482711c8026b50fce10c55b3fb76f4075c3`, the user ran .NET SDK 10.0.403: Core/PTMagic/Monitor solution build PASS in 13.9s, **18/18 offline harnesses and 386 checks PASS**, including all nine adaptive checks for Binance quotas, response-weight headers, cooldowns, fairness, deadlines and acquisition beyond 60 pages. Eight pre-existing nonfatal nullable warnings remain. Configured Unicode-market raid, two-startup persistence and live PT/Binance/Monitor acceptance remain pending.

## November 11 — Single-source ratio and adaptive derivative acquisition decisions

**[D-051/D-052: public global-account ratio only; application-managed adaptive acquisition](2026-11-11-single-source-ratio-adaptive-acquisition.md)**

The approved PTMagic ratio scope retains only `GlobalLongShortAccountRatio`; both top-trader metrics and their API-key-only path are removed entirely. The three user-configurable per-raid request-budget properties are to be removed and replaced by application-managed adaptive acquisition using shared Binance rate-limit state, endpoint weights, response headers and 429/418 cooldowns. Internal pagination, fairness, incremental coverage, persistence and UNAVAILABLE safeguards remain. This is a design decision, not completed implementation. PTMagic application development remains strictly separate from ProfitTrailer strategy-settings development. No application source, configuration or strategy settings were changed in this documentation update.

## Latest November 11 Monitor resolution

**[DashboardTop refresh restored and runtime-confirmed](2026-11-11-dashboard-refresh-resolution.md)**

The user reports that the top dashboard now refreshes properly. The one-file fix guards the `cleanupOrphanedTooltips()` call in `Monitor/Pages/Index.cshtml` when a browser may have an older cached `custom.js`. The user's local solution build passed after pulling the fix (15.6 seconds across Core, PTMagic and Monitor). The original jQuery `.load()` path and five-second refresh remain unchanged. No PBL endpoint/cache or ticker refresh changes were reintroduced.

## Historical November 11 dashboard investigation

**[Dashboard refresh history and pre-fix state](2026-11-11-dashboard-refresh-history-and-current-state.md)**

This record preserves the earlier open-investigation state and PBL rollback history. Its unresolved-refresh statements describe the pre-fix checkpoint and are superseded by the resolution record above.

## November 11 — Unicode Binance Futures symbol validation PASS

**[Unicode Binance Futures symbols: 384 checks passed at f108cd1](2026-11-11-unicode-futures-symbol-validation.md)**

The user reported five eligible COIN perpetual symbols containing Chinese characters. The shared derivative symbol normalizer was ASCII-only and aborted OI service preparation. Unicode-aware letter/digit validation now accepts these exchange-provided names while retaining rejection of whitespace, query separators and unsupported punctuation. The user ran the existing 17-harness suite at exact source `f108cd1ab39c44103bed91d1899f90f86a830eb4`: .NET 10.0.403 solution build PASS in 16.7 seconds; **17/17 harnesses and 384 checks PASS**. OI, funding and ratio service/cache handling is covered offline. Live Binance endpoint acceptance and a configured raid using the five symbols remain pending.

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


## November 11 — Top-trader ratio removal validated

**[Single public global-account ratio; 377 offline checks passed](2026-11-11-top-trader-ratio-removal-validation.md)**

At application source `1a1f1804237288433ed046b30fb7d9b780a32066`, both top-trader metrics and all API-key handling were removed. The .NET 10.0.403 solution build passed in 18.2 seconds; 17/17 offline harnesses and 377 checks passed. Adaptive acquisition and configured runtime acceptance remain pending.
