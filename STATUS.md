# PTMagic 2.10 — Current Development Status

**Updated:** November 9, 2026

**Application branch:** `phase1/market-data-foundation`

**Current source checkpoint:** `87b9eaa1c865e39d8fff6a657e1b332012be8c16`

**Current handoff:** [Stabilization, correlation, and validation](handoffs/2026-11-07-stabilization-correlation-validation.md)

This file describes the present state. Dated evidence stays in [updates](updates/README.md). The earlier append-heavy status is preserved in [history](history/2026-11-07-pre-reconciliation/STATUS.md). Accepted behavior is in [DECISIONS](DECISIONS.md); the complete plan is [roadmaps/CURRENT.md](roadmaps/CURRENT.md).

## November 9 — Uniform TestMode console styling

Application source `87b9eaa1c865e39d8fff6a657e1b332012be8c16` adds the same `Magenta` NLog `ColoredConsole` highlighting condition for every case-insensitive `TestMode` message in `PTMagic/nlog.config`, `Monitor/nlog.config` and the packaged default PTMagic `nlog.config`. INFO/WARN levels and file output are unchanged. Source/configuration inspection completed; user-local build and console rendering remain **not run**. Existing installed `nlog.config` requires deployment or copying the new config into the correct runtime folder.

## November 9 addition — warm-start normalized OHLCV

**Published and focused-build verified:** `925db7c153ee4d53cfe3b7bf736318e7a30bccf1` adds compressed, versioned, atomic per-exchange/symbol normalized candle checkpoints under `_data/NormalizedOhlcvCache`. The regular anchored refresh is still required to verify gaps, history capacity and freshness; invalid files are ignored and recovered through the exchange. Cache writes are throttled.

Eight test groups in `Tests/NormalizedWarmStartCache` passed **8/8** at `925db7c` on November 9. The same execution passed Phase1AnalyticsReliability **16/16** and Phase1COhlcv **13/13**, **37/37 focused checks**. Core/PTMagic/Monitor solution build passed in **18.3 seconds** using .NET SDK **10.0.403**. The authored inventory is **280** groups. The earlier **272 passing groups** remain evidence across `86c2ea3` and `d331fbd`; the new executable code at `925db7c` **passed its focused .NET build and 37/37 checks**. Configured two-startup runtime cache reuse remains unverified. The cache does not replace the separate legacy minute-tick data reconstruction. [Decision D-040](DECISIONS.md#d-040--targeted-persistent-ohlcv-warm-start-now).

## Publication status

The earlier settings/Monitor-help source was published at `a0b375c`. The current source checkpoint is `925db7c`. It adds [the cumulative effective-change record](CHANGELOG-2.10.md) with PR/merge guidance, completes the explicit startup SOM default in the development general-settings template, and clarifies the existing Monitor APPLICATION toggle with visible TestMode help. The packaged default already contained StartupSellOnlyMode=true. Engine code and test cases are unchanged. The two Telegram fixture corrections were executed successfully at `d331fbd`; build and harness evidence retain their actual execution revisions. No new .NET build or browser result is claimed for the documentation/template/static-view update.

The user's standing authorization covers publication of PTM 2.10 development changes to the application and documentation branches in [D-038](DECISIONS.md#d-038--standing-authorization-to-publish-ptm-210-development), without renewed conversational approval. Actual tool restrictions remain binding. The current handoff pins the published source for user-local verification; earlier passes remain attributed to the source actually tested.

## Present conclusion

The November 7 implementation addresses the assessed configuration lifecycle defects, adds startup global sell-only protection through ProfitTrailer's control API, repairs Monitor row preservation and missing-reference handling, strengthens normalized acquisition/decision freshness, reports history requirements, aligns Concentration ranking with its trend duration, implements Phase 1D BTC correlation, and adds bounded decision history.

The startup API design supersedes the earlier unpublished full-preset overlay. The guard request carries `enabled=true` and the configured API token; it does not carry a properties payload. Normal configuration delivery and API guard release are separate acknowledged actions. The current contract is [D-037](DECISIONS.md#d-037--direct-global-som-api-supersedes-the-startup-preset-overlay).

**Current evidence level: all 272 checks in twelve harnesses have passed across two recorded runs. Ten harnesses passed 193 checks at `86c2ea3`; ConfigurationLifecycle passed 66 and DecisionHistory passed 13 at `d331fbd`, where Core/PTMagic/Monitor also built successfully. Deterministic acceptance is complete; configured runtime, actual PT API, and browser acceptance remain open.** [Exact-source evidence](updates/2026-11-07-completed-harness-validation.md).

The source checkpoint identifies the implementation snapshot. Do not infer a new deployment from documentation or from a 2.10.0 version string.

### Latest reported build and completed continuation

The latest user-run build identifies source `d331fbd059041241069646c3bb82ac6549423a70` and .NET SDK 10.0.403. Core, PTMagic, and Monitor built successfully in 10.9 seconds. ConfigurationLifecycle passed all 66 checks, and DecisionHistory passed all 13. The continuation completed successfully.

The earlier run at `86c2ea3ff430b62e654f929a222935ec53ea8fa6` built the same application projects in 15.8 seconds and passed 193 checks across the first ten harnesses, including 40 TriggerConfigurationValidation and 28 MonitorSettingsRoundTrip checks. It stopped on the lifecycle fixture's CS0118 type/namespace collision. Explicitly qualifying the two Telegram constructors was the only executable change before the successful continuation; production source and test expectations were unchanged. The 272 total therefore combines evidence from these two revisions, rather than claiming a new full-suite run at `d331fbd`.

The earlier validation fixture failure at `78967a7` is now resolved by the 40/40 result, including both added sentinel boundary cases. That [earlier evidence](updates/2026-11-07-build-and-partial-harness-validation.md) remains historical. Nullable warnings in Phase1SmsSummaryIsolation and NormalizedPriceTrendMigration did not prevent their passes.

The user subsequently supplied another log using a configured runtime directory separate from the Git checkout. Its first raid loaded the default properties, completed, and reported a switch to a non-default setting; the next raid loaded only 13 PAIRS, 12 DCA, and 11 INDICATORS lines, then requested bare `symbol=USDT` with an empty MainMarket and failed. Neither raid contains the current code's unconditional `Source revision` or `Analysis main market` lines. Its stack locations also correspond to the older code layout. The process therefore executes pre-fix Core behavior; its exact source SHA and loaded DLL path are unknown. The runtime working directory and version 2.10.0 label do not identify the assembly used.

The log lacks the TestMode banner and reports `PT Config updated: Yes` after the first raid. It is not TestMode acceptance of the current implementation, and that reported update does not validate the new guard/acknowledgement logic. The next validation selects the freshly built DLL by absolute path while retaining the existing runtime working directory and TestMode configuration. This makes binary selection explicit without copying or overwriting private files. A permanent installed-launcher update must deploy a coherent application bundle, not Core.dll alone, and preserve settings, presets, data, and logs.

The main-market corrections preserve inherited preset assignments for null property groups, resolve and validate the exact `market` value before exchange I/O, and use the USDT price identity without a ticker request. Their lifecycle regressions now pass, including invalid-input rejection before exchange collection. Current normalization rejects an empty quote before the bare-USDT request seen in the log. The later explicit compiled-DLL launch reached preset validation, then stopped because the Default setting referenced a missing preset file. This occurs before guard enable or exchange loading. The user subsequently reported a long initial run underway and asked about SOM while TestMode was enabled. No completed result or exact running source was supplied for that run. Collect its `Source revision`, `Analysis main market` and completed-raid output; TestMode cannot establish native PT SOM activation. The current template/help changes do not require interrupting that run.

## Accepted pre-change evidence

| Evidence | Result and limit |
|---|---|
| User-local .NET 10 build | Passed at the November 5 baseline associated with `d0b0b87` |
| Six deterministic harnesses | 88 checks passed: readiness 5, Phase 1C 13, SMS summary isolation 5, trigger logic 29, normalized migration 18, metric warnings 18 |
| Binance Futures USDT TestMode | Nine raids reviewed; no PT writes in TestMode |
| Return availability | 250/250 global and 519/519 asset returns on the requested uncapped diagnostic trends; configured capped variants retained their distinct populations |
| Export/runtime consistency | 5,192 matching normalized per-asset PriceTrend values, zero differences; this compares two normalized outputs, not the old legacy calculation |
| OffTrigger | A positive BTC off branch ran, followed by same-raid reactivation while its activation condition remained true; lasting deactivation was not established |
| Fiat conversion | USDT identity case only; non-USDT historical quote conversion remains unverified |
| Source provenance | The source SHA was inferred from the preceding workflow; deployed logs printed 2.10.0, not the exact commit |

[Detailed nine-raid evidence](updates/2026-11-05-price-compatibility-nine-raid-testmode.md). The earlier pinned-time cold-start correction was separately [verified in Futures TestMode](updates/2026-11-05-pinned-boundary-fix-futures-verified.md). Its accepted result does not cover the new tight-retention request-window case.

## November 7 implementation and acceptance

The twelve harnesses now have passing execution evidence split between `86c2ea3` and `d331fbd`. The 66 lifecycle checks exercise production components with fake transports; the 13 history checks exercise production storage and capture paths with temporary fixtures. The table below separates that deterministic evidence from the remaining configured-environment acceptance.

| Area | Current source behavior | Acceptance still required |
|---|---|---|
| Final SMS removal | A nonempty-to-empty SMS transition is a configuration change; the clean-rebuilt-properties regression passes | Configured repeated-raid removal, actual acknowledgement, persistence, and failed-delivery retry |
| Desired / pending / confirmed delivery | Failed/partial delivery preserves acknowledgement and retries the same desired payload; deterministic cases pass | Actual PT transport acknowledgement/failure and configured restart recovery |
| Same-name reload / partial delivery | Current-definition reload and A→failed B→A replay cases pass with fake senders | Configured reload and multi-target recovery |
| Startup state | API enable precedes bootstrap; fresh conclusive normal acknowledgement precedes release; ordering/failure/retry cases pass with fake transports | Native per-target enable/release acknowledgement and configured startup recovery |
| Global SOM behavior and ownership | User clarified: global SOM blocks new buys and DCA buys while allowing sells; no prior-state readback/restoration is implemented | Confirm native behavior and explicit flag ownership in the configured PT environment; distinguish intended contract from observed execution |
| Guard checkpoint and tokens | Separate checkpoint, token alignment, base paths, redaction, restart state, and TestMode isolation pass in the lifecycle harness | Configured filesystem recovery and the actual PT targets/context paths |
| Startup opt-out | No new guard without an owned operation; pending PTM-owned recovery still resumes; both deterministic cases pass | Configured opt-out/restart behavior with known and unknown prior state |
| Monitor trigger editing | Rows preserve their MarketTrend/Metric/Tag identity and persisted precision; 28/28 round-trip checks passed at `86c2ea3` | Browser save/reload for multiple metrics on one trend |
| Reference validation | Broken MarketTrend references are rejected during configuration validation; defensive evaluation treats absent inputs as unavailable; all 40 validator checks, including sentinel boundaries, passed at `86c2ea3` | Verify actual startup/reload rejection |
| Main-market bootstrap | Exact parsing, null-group inheritance, fresh-summary bootstrap, invalid inputs, and exchange identity boundaries pass | Updated configured process identity, intended PAIRS market, and a successful USDT raid |
| SMS unavailable observations | Unknown activation, invalid age/time/volume, and AND/OR/negation cases pass in the deterministic harnesses | Configured repeated-raid selection, persistence, and output inspection |
| Pinned normalized acquisition | Network request windows and retained samples honor the raid's pinned analysis boundary | Tight retention while requests cross a five-minute close; next-raid advancement |
| Decision freshness | Stale raids, post-acknowledgement expiration, and volume-only configurations retain/defer protection in passing lifecycle cases | Configured slow bootstrap and decision-age behavior on real observations |
| History requirements | Per-metric reports distinguish complete history, current-raid slots, all-alignments retention, and configured capacity | Period/alignment calculations, dependencies, insufficient-store warnings, Monitor export |
| Return Concentration | Ranking volume uses TrendMinutes at the same normalized endpoint as the return; Top10-minus-remainder meaning and 100% coverage remain | Short/long trend windows, complete ranking population, min eleven markets, deterministic ranking |
| Phase 1D correlation | Exact synchronized simple-return Pearson vectors; N=30 default; asset plus global mean/median metrics; 21/21 harness checks passed at `86c2ea3` | Configured history, coverage, export/trigger/Monitor integration, and runtime acceptance |
| Decision history | All 13 checks pass: append/rotation/retention/quota, interrupted and oversized records, acknowledgement isolation, actual capture paths, and sensitive-data exclusion | Configured raid provenance, filesystem behavior, and integration with runtime summaries |

Detailed issue tracking: [configuration lifecycle and analytics reliability](issues/003-configuration-lifecycle-and-data-reliability.md). Implementation checkpoint: [November 7 update](updates/2026-11-07-stabilization-correlation-implementation.md).

## Execution queue

The completed deterministic inventory is **272 passing check groups across twelve projects**, with each result attributed to its actual source: 193 at `86c2ea3`, then 66 lifecycle and 13 history at `d331fbd`. Collect the reported ongoing run before requesting another launch. The current handoff retains the explicit built-DLL procedure and the complete twelve-project sequence for later work that requires them; the documentation/template/static-view update does not require repeating the completed harness checks.

Runtime acceptance remains open for:

- Restart of the updated configured instance, recorded Source revision, valid compiled PAIRS market, and a successful raid after the bootstrap corrections.
- Direct global SOM startup API behavior, explicit PTM flag ownership, and conclusive/fresh configuration delivery before release acknowledgement.
- Last-SMS removal that stays removed, including delivery failure followed by retry.
- Real PT acknowledgement and failed delivery; TestMode cannot establish either.
- Long-running raids exceeding the decision-age limit.
- Configured correlation and history requirements on retained real data.
- Binance Spot and Binance US migration/runtime behavior.
- Non-USDT Fiat conversion with synchronized quote/USDT history.
- Invalid TrendMinutes and missing MarketTrend reference rejection at actual startup/reload.
- Monitor trigger save/reload and old Market Analyzer rendering/history continuity.
- Existing non-default confirmed settings retained during an indeterminate raid.
- Decision-history provenance, bounded storage, and safe error records.

Some runtime scenarios require the user's configured exchange/PT installation. Source review and neutral deterministic fixtures do not replace those environments.

## Phase progress

| Phase | Current status |
|---|---|
| Phase 0 — architecture and eligibility | Established; later lifecycle contracts are now explicit |
| Phase 1A — normalized market-data foundation | Earlier baseline validated; new request-window/freshness extension pending |
| Phase 1B — return and relative-strength metrics | Earlier USDT Futures baseline validated; new Concentration window pending |
| Phase 1C — trend-duration OHLCV metrics | Implemented and earlier harness/runtime evidence recorded; extended history diagnostics pending |
| Unified PriceTrend migration | Implemented; Futures USDT evidence accepted with the stated non-USDT/Spot/US/browser gaps |
| Phase 1D — BTC correlation | 21/21 deterministic checks passed at `86c2ea3`; configured runtime acceptance pending |
| Minimal decision history | 13/13 deterministic checks passed at `d331fbd`; configured runtime integration remains; full Phase 6 stays planned |
| Phase 2 / 2B — derivatives ingestion and aggregates | Planned |
| Phase 3 — higher-order market state measurements | Planned |
| Phase 4 — selection, Monitor, and engine integration | Continues for every metric family |
| Phase 5 — liquidity, depth, and execution measurements | Planned |
| Phase 6 — complete native historical analysis | Planned beyond the initial decision audit |
| Dedicated performance work | Deferred until **all approved new metrics** are complete, including derivatives and liquidity |

## Scope and ordering decisions

Personal strategy development, preset tuning, long/short strategy tracks, and trading profitability are independent of PTMagic 2.10. They are excluded from this implementation backlog and its acceptance criteria.

The performance deferral is explicit. Startup reconstruction, broader snapshot caching, incremental indicator/vector work, debug-log optimization, and performance benchmarking must not be promoted ahead of remaining metrics. Correctness and bounded storage remain part of normal implementation.

The old 2.9 performance results and November 5 cold-start timings are historical evidence, not a current steady-state CPU measurement of 2.10. The old first raid took 14m28s, including about 11m59s of legacy reconstruction; that observation explains future work without changing its agreed ordering.

## Next action

Collect the user-reported long run and its source/main-market/completion evidence. If another run is needed, use the explicit-DLL procedure in the [current verification handoff](handoffs/2026-11-07-stabilization-correlation-validation.md) with the existing runtime configuration. Native SOM and normal PT delivery require separate live acceptance because TestMode sends neither. The Monitor control is General Settings → APPLICATION → Startup Global SOM, immediately below Test Mode. Continue the applicable runtime/PT/browser checks before the remaining metric families in [the current technical roadmap](roadmaps/CURRENT.md).

Earlier files that instructed a restart of Phase 1C, preservation of a separate legacy PriceTrend path, use of the removed selective-legacy harness, or optimization before correlation are historical and superseded.
