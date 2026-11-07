# PTMagic 2.10 — Current Development Status

**Updated:** November 7, 2026

**Application branch:** `phase1/market-data-foundation`

**Current source checkpoint:** `d331fbd059041241069646c3bb82ac6549423a70`

**Current handoff:** [Stabilization, correlation, and validation](handoffs/2026-11-07-stabilization-correlation-validation.md)

This file describes the present state. Dated evidence stays in [updates](updates/README.md). The earlier append-heavy status is preserved in [history](history/2026-11-07-pre-reconciliation/STATUS.md). Accepted behavior is in [DECISIONS](DECISIONS.md); the complete plan is [roadmaps/CURRENT.md](roadmaps/CURRENT.md).

## Publication status

The follow-up correction is published on `phase1/market-data-foundation` at the source checkpoint above. It fully qualifies the Telegram settings type in the ConfigurationLifecycle and DecisionHistory fixtures; production behavior and the authored case inventory are unchanged.

The user's standing authorization covers publication of PTM 2.10 development changes to the application and documentation branches in [D-038](DECISIONS.md#d-038--standing-authorization-to-publish-ptm-210-development), without renewed conversational approval. Actual tool restrictions remain binding. The current handoff pins the published source for user-local verification; earlier passes remain attributed to the source actually tested.

## Present conclusion

The November 7 implementation addresses the assessed configuration lifecycle defects, adds startup global sell-only protection through ProfitTrailer's control API, repairs Monitor row preservation and missing-reference handling, strengthens normalized acquisition/decision freshness, reports history requirements, aligns Concentration ranking with its trend duration, implements Phase 1D BTC correlation, and adds bounded decision history.

The startup API design supersedes the earlier unpublished full-preset overlay. The guard request carries `enabled=true` and the configured API token; it does not carry a properties payload. Normal configuration delivery and API guard release are separate acknowledged actions. The current contract is [D-037](DECISIONS.md#d-037--direct-global-som-api-supersedes-the-startup-preset-overlay).

**Current evidence level: a successful Core/PTMagic/Monitor build and ten completed harnesses with 193 passing checks at `86c2ea3`. ConfigurationLifecycle failed compilation before any cases executed; DecisionHistory did not run. Full regression and configured runtime acceptance remain pending.** [Exact-source evidence](updates/2026-11-07-193-check-validation.md).

The source checkpoint identifies the implementation snapshot. Do not infer a new deployment from documentation or from a 2.10.0 version string.

### Latest reported build and source correction

The latest user-run build identifies source `86c2ea3ff430b62e654f929a222935ec53ea8fa6` and .NET SDK 10.0.403. Core, PTMagic, and Monitor built successfully in 15.8 seconds. The first ten harnesses passed 193 checks, including all 40 TriggerConfigurationValidation cases and all 28 MonitorSettingsRoundTrip cases. The Razor compilation correction remains confirmed.

ConfigurationLifecycle failed to compile at Program.cs line 686 with CS0118: `Telegram` is a namespace but is used like a type. The fixture constructor introduced an unqualified type name that collided with the Telegram namespace. Source review found the same reference in DecisionHistory Program.cs line 198, which the fail-fast run had not reached. Both constructors now use `Core.Main.DataObjects.PTMagicData.Telegram`; no production source or test expectations change. The lifecycle harness executed zero cases, and DecisionHistory did not run. The solution contains only Core, PTMagic, and Monitor, so its successful build did not compile these separate harnesses.

The earlier validation fixture failure at `78967a7` is now resolved by the 40/40 result, including both added sentinel boundary cases. That [earlier evidence](updates/2026-11-07-build-and-partial-harness-validation.md) remains historical. Nullable warnings in Phase1SmsSummaryIsolation and NormalizedPriceTrendMigration did not prevent their passes.

A separate runtime excerpt shows a Binance Futures ticker request with `symbol=USDT`, a blank MainMarket, and an aborted raid. Its stack locations match the earlier `d0b0b87` baseline and it lacks the current `Source revision` line, suggesting an older running binary. This is an inference; the excerpt does not establish an exact runtime SHA.

The main-market corrections at `86c2ea3` preserve inherited preset assignments for null property groups, resolve and validate the exact `market` value before exchange I/O, and use the USDT price identity without a ticker request. They add an explicit main-market log. Their production source has built, but the lifecycle cases have not executed. The corrected harness and a restarted, updated configured instance still require verification; capture the runtime `Source revision` and confirm the compiled PAIRS market.

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

The build and ten completed harnesses have execution evidence at `86c2ea3`. The table below lists source behavior and remaining acceptance; the lifecycle and history harnesses and configured runtime checks are still open. Any follow-up source correction needs its own recorded verification.

| Area | Current source behavior | Acceptance still required |
|---|---|---|
| Final SMS removal | A nonempty-to-empty SMS transition is a configuration change that must reach PT | Repeated-raid removal, acknowledged delivery, persistence, and failed-delivery retry |
| Desired / pending / confirmed delivery | Only successful delivery advances confirmed state; unchanged desired settings still retry after failure | API and file-path failures, restart/checkpoint behavior, same desired payload retry |
| Same-name reload / partial delivery | Compile current definitions even when a setting name is unchanged; a partial multi-target failure still requires replay when returning to an old payload | Current-definition reload and A→failed B→A repair across targets |
| Startup state | `StartupSellOnlyMode=true` assigns global SOM control to PTM: API enable before slow bootstrap, then API disable after fresh conclusive configuration acknowledgement; no startup properties submission | Per-target enable/release acknowledgement, enable failure/retry, stale or indeterminate raids, configuration-before-release ordering, release failure/retry, TestMode isolation |
| Global SOM behavior and ownership | User clarified: global SOM blocks new buys and DCA buys while allowing sells; no prior-state readback/restoration is implemented | Confirm native behavior and explicit flag ownership in the configured PT environment; distinguish intended contract from observed execution |
| Guard checkpoint and tokens | Guard metadata uses `_data/StartupSellOnlyModeState.json`; additional-target API tokens may be supplied through ProfitTrailerServerAPITokenXtra, otherwise the primary token is shared | Restart/pending-release recovery, base-path preservation, target/token alignment, redaction and no live checkpoint writes in TestMode |
| Startup opt-out | `StartupSellOnlyMode=false` prevents a new API guard; recorded pending PTM-owned guard work still resumes. Indeterminate startup retains known confirmed configuration or defers unknown state | New opt-out versus pending recovery, restart with known/unknown configuration, no forced DEFAULT publication |
| Monitor trigger editing | Rows preserve their MarketTrend/Metric/Tag identity and persisted precision; 28/28 round-trip checks passed at `86c2ea3` | Browser save/reload for multiple metrics on one trend |
| Reference validation | Broken MarketTrend references are rejected during configuration validation; defensive evaluation treats absent inputs as unavailable; all 40 validator checks, including sentinel boundaries, passed at `86c2ea3` | Verify actual startup/reload rejection |
| Main-market bootstrap | Null property groups inherit default-file assignments; the exact market value is normalized and validated before exchange I/O; USDT uses an identity price of 1 | Lifecycle regressions, missing/malformed market rejection, updated configured process identity, and a successful USDT raid |
| SMS unavailable observations | Unknown activation retains an existing ordinary SMS; final unavailable SMS expressions keep initial selection indeterminate; invalid age/time/volume observations remain unavailable | Missing/future timestamps, nonfinite/negative volume, held SMS, conclusive masked expressions |
| Pinned normalized acquisition | Network request windows and retained samples honor the raid's pinned analysis boundary | Tight retention while requests cross a five-minute close; next-raid advancement |
| Decision freshness | `MaxAnalysisAgeSeconds=300` compares decision time with the pinned analysis time; missing/future/expired pins are unavailable | Boundary ages and slow bootstrap; legitimate long-duration bars remain usable |
| History requirements | Per-metric reports distinguish complete history, current-raid slots, all-alignments retention, and configured capacity | Period/alignment calculations, dependencies, insufficient-store warnings, Monitor export |
| Return Concentration | Ranking volume uses TrendMinutes at the same normalized endpoint as the return; Top10-minus-remainder meaning and 100% coverage remain | Short/long trend windows, complete ranking population, min eleven markets, deterministic ranking |
| Phase 1D correlation | Exact synchronized simple-return Pearson vectors; N=30 default; asset plus global mean/median metrics; 21/21 harness checks passed at `86c2ea3` | Configured history, coverage, export/trigger/Monitor integration, and runtime acceptance |
| Decision history | Bounded JSONL records with source/config hashes, evaluated inputs, selection/guard/delivery outcome | Retention, rotation, quotas, error paths, sensitive-data omission, TestMode distinction |

Detailed issue tracking: [configuration lifecycle and analytics reliability](issues/003-configuration-lifecycle-and-data-reliability.md). Implementation checkpoint: [November 7 update](updates/2026-11-07-stabilization-correlation-implementation.md).

## Execution queue

The current handoff supplies a focused continuation: pull the corrected source, verify its identity, build the solution, then run ConfigurationLifecycle and DecisionHistory. It retains the complete twelve-project sequence for a full rerun when required. The inventory is **272 authored check groups**: 193 passed across ten harnesses at `86c2ea3`; the 66 lifecycle groups did not execute because of the compiler error, and the 13 history groups did not run. The fixture qualification corrections require user-local verification under D-021. Record the actual source SHA, .NET version, build output, and per-project results; do not roll the expected 79 remaining checks into a passing total or relabel the earlier 193 passes as a run of the corrected source.

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
| Minimal decision history | Implemented; new execution acceptance pending; full Phase 6 remains planned |
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

Run the [current verification handoff](handoffs/2026-11-07-stabilization-correlation-validation.md) from the PTMagic application repository. Review the output, fix any failures, and record acceptance by scenario and source SHA. After current correctness acceptance, continue the remaining metric families in [the current technical roadmap](roadmaps/CURRENT.md).

Earlier files that instructed a restart of Phase 1C, preservation of a separate legacy PriceTrend path, use of the removed selective-legacy harness, or optimization before correlation are historical and superseded.
