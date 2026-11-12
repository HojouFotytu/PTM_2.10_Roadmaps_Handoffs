# PTMagic 2.10 — Current Decision Register

**Phase 2 Taker Flow implementation — November 12:** application source [`f7d802facfabb4611098d695d88a269d60daa278`](https://github.com/HojouFotytu/PTMagic/commit/f7d802facfabb4611098d695d88a269d60daa278) now contains **26 registered metrics** (17 globally evaluable, nine asset-only), including `TakerBuyRatio` and `TakerImbalance`. The existing kline reader retains index-10 taker-buy **quote** volume, an opt-in exact-period feature engine calculates both metrics, legacy OHLCV cache **v1** remains readable, and cache **v2** persists source-verified taker fields with targeted repair of old cache windows. The existing diagnostic TestMode analyzer was extended in place; Monitor labels/colors and focused tests were updated. **Published and source-inspected; .NET build, new focused test execution and configured taker-flow raid are PENDING.** The earlier D-053 PASS cannot be reattributed to this feature. [Implementation and verification handoff](updates/2026-11-12-phase2-taker-flow-implementation.md).

**2026-11-12 D-053 configured verification — PASS:** user-run `.NET 10` solution build **PASS (12.9s)** at application source `e31635a1e67347918ca1bbf94d0fb64809b1cea0`; **Phase2Funding 28/28** and **Phase2AdaptiveAcquisition 8/8** (**36/36 focused offline checks**). The user-supplied log and `_data` archive show **four completed TestMode raids**, 519 COIN markets, **519/519 funding history coverage**, **4,169/4,169 available trigger inputs** per decision, **zero completed-raid metric warnings**, successful bulk-only funding acquisition (6/1/1/1 pages; no failures) and fresh determinate decisions. Obsolete OI/ratio warnings preceded the corrected analyzer reload. **D-053 source, focused checks and configured TestMode acceptance are complete**; non-TestMode PT delivery, startup SOM enforcement and Monitor browser acceptance remain unverified. **Next development: Phase 2 taker-flow assessment and implementation; do not repeat retired OI/ratio validation.** [Full D-053 configured evidence](updates/2026-11-12-d053-configured-testmode-validation.md).

**D-053 implementation and removal-audit checkpoint — November 12, 2026:** PTMagic source [`892a5f1f4729a3fccd3cb477ba6ad22fbbe0918d`](https://github.com/HojouFotytu/PTMagic/commit/892a5f1f4729a3fccd3cb477ba6ad22fbbe0918d) contains the completed removal of `OpenInterestChange`, `OpenInterestValueChange` and `GlobalLongShortAccountRatio`, including their acquisition/services/active caches/registry/Monitor integrations. The source audit compared the **22-metric pre-introduction baseline** [`66629347`](https://github.com/HojouFotytu/PTMagic/commit/66629347f0dc9c7b68ea9f1c3f5bf536f3d7c427), **27-metric pre-removal** `d101b5a0` and current **24-metric** code: all 22 original metric identities and scopes survive; `FundingRate` and `FundingSum` also survive. A real shared Unicode symbol-validator dependency was temporarily broken by deleting OI, then repaired by [`02820822`](https://github.com/HojouFotytu/PTMagic/commit/02820822b9bb) and [`d7847c46`](https://github.com/HojouFotytu/PTMagic/commit/d7847c46190b). No further major/critical removal-related defect was established by source inspection; **current-revision local build, 15-harness test execution and configured runtime acceptance remain unverified**. The earlier 18-harness PASS at `d101b5a0` is strictly **pre-removal evidence**. [Full read-only audit](updates/2026-11-12-d053-removal-code-audit.md) (links relative to repository root). **This checkpoint supersedes all contradictory claims below that removal is pending, that retired OI/positioning is active, or that its tests/feature work remain required. Dated implementation evidence is retained as history.** No rollback and no strategy-settings work.


**Current scope (November 12, 2026): D-053 supersedes the open-interest and long/short positioning feature scope.** The approved future application contains **24 metrics (17 global-capable and 7 asset-only)** after source cleanup; `FundingRate`/`FundingSum`, kline-based taker flow, and funding/taker market-wide aggregates remain. The current D-053 code has removed all three withdrawn metrics; local post-removal execution has not been verified. Earlier OI/ratio entries below are retained for decision history, **not authorization for future development**.

**Reconciled:** November 11, 2026

**Current inspected application branch head:** `27da292158687bc0bf1aa3b990d06f53237b42d9`; last fully offline-accepted source `fb94373d8928b681e3ebe1f7209bd1439db42e72` (337/337; later Monitor changes/rollback not covered by that suite)

**Scope:** PTMagic 2.10 application development. Personal trading-strategy work is independent.

This register governs current intent. “Accepted” identifies a design or user decision, not successful execution. [STATUS.md](STATUS.md) records implementation and evidence separately. The previous register is preserved in [history](history/2026-11-07-pre-reconciliation/DECISIONS.md); dated implementation records remain unchanged.

## November 10 — SOM and Monitor validation accepted (latest evidence)

**Exact verified application source:** `fb94373d8928b681e3ebe1f7209bd1439db42e72`. The user ran the existing full validation script twice: .NET SDK 10.0.403 solution builds **PASS** in 15.6s and 10.3s; **all 16 offline harnesses and 337/337 test groups PASS in both runs**. This includes 71 ConfigurationLifecycle checks (SOM enable-only, startup manual-release notice, new metric snapshots), 28 Monitor settings roundtrip checks and 13 DecisionHistory checks. The first build reported eight nonfatal pre-existing nullable test-source warnings; the second reported no warnings, consistent with incremental compilation. No live exchange, PT API or browser acceptance is claimed.

The Market Metrics History Requirements **UI panel** is removed; its diagnostic calculations remain active. Global Settings Log captures all available **market-wide** metrics across configured trends at entry creation and highlights a metric in white when referenced by any selected-setting trigger (even if FALSE/UNAVAILABLE); other metrics are gray. Existing history must not be fabricated from later snapshots. The red startup `PT: SOM` notice lasts only the first two raids; PTMagic never automatically requests global SOM OFF and the user releases it manually. **Do not rerun this completed offline suite as a prerequisite for new Phase 2 work.** Current Phase 2 ratio scope and application-owned request scheduling are governed by D-051; configured runtime and Monitor browser verification remain separately open.

**Evidence:** [November 10 — 337-group offline validation](updates/2026-11-10-som-monitor-offline-validation.md).

## NEXT CHAT — verify SOM safety changes

Application source `891f709010c867259a6cde3df8e9c82781091b7f` (existing `phase1/market-data-foundation` branch) contains enable-only startup SOM, manual ProfitTrailer release, legacy release-checkpoint migration, and the red `PT: SOM` ticker plus raid-summary warnings on startup raids 1–2. **The source has NOT yet passed its new local .NET build or regression suite.** Last verified source `49f2aab66592b6e2922097ca5242b5a614090602` passed **332/332** before these changes.

**Historical next action (superseded; D-053 removal implemented):** remove `OpenInterestChange`, `OpenInterestValueChange`, and `GlobalLongShortAccountRatio` and their source-only OI/positioning acquisition, cache, registry, configuration and Monitor paths from PTMagic. Preserve funding, existing 17 global metrics, valid asset metrics, normalized OHLCV, startup SOM, and the existing eligibility filter. Update applicable existing tests/diagnostics. Then resume funding/taker-flow work and funding/taker Phase 2B aggregates. Source removal is **complete** at `892a5f1f`; post-removal runtime acceptance remains unverified; no strategy-settings development is in scope.

[Complete active new-chat handoff](handoffs/2026-11-10-som-enable-only.md). Only specified unfinished Phase 1 *configured integration* tests were deferred; normal source builds and regressions remain mandatory.

## Existing decisions and their present disposition

| ID | Current disposition |
|---|---|
| D-001 | **Active.** The market-analysis expansion belongs to PTMagic 2.10. The completed 2.9 modernization is separate historical work. |
| D-002 | **Superseded by D-023.** The original parallel legacy/normalized PriceTrend architecture was replaced. Remaining legacy snapshot/reconstruction code is an operational dependency to audit later, not authority to restore a legacy calculator. |
| D-003 | **Active, clarified by D-024.** Metrics use explicitly selected per-trend populations and record eligible versus valid samples. Global and asset populations can differ by the documented MaxMarkets contract. |
| D-004 | **Superseded by D-023.** Omitted trigger Metric now resolves normalized PriceTrend. |
| D-005 | **Active.** Missing, invalid, nonfinite, stale, or insufficient measurements are unavailable. Numeric zero is a valid value, never a missing-data substitute. |
| D-006 | **Active, window amended by D-031.** Concentration means Top10 return advantage in percentage points. Volume distribution has separate names. |
| D-007 | **Active.** Phase 4 is metric-trigger integration; Phase 5 is liquidity/depth/stress. |
| D-008 | **Historical prerequisite fulfilled.** Phase 1A readiness was contained and later a specific boundary defect was repaired. The performance follow-ups now follow D-032. |
| D-009 | **Active.** Preserve dated historical roadmaps, handoffs, and evidence. Snapshot materially replaced current documents and keep one current authority. |
| D-010 | **Active.** General cross-sectional readiness requires a nonempty eligible population and at least ceil(0.90 × eligible count) valid markets. Missing markets stay in the denominator. |
| D-011 | **Active, window amended by D-031.** Return Concentration requires the complete eligible ranking population, with valid returns and complete volume inputs. Volume-share families retain their documented 100% requirements. |
| D-012 | **Historical containment policy, refined by D-029.** Scheduled refresh recovery remains valid; pinning now prevents requesting a newer analytical endpoint during a long raid. Do not treat the original boundary diagnosis as still wholly unknown. |
| D-013 | **Active for continuous operation; startup extended by D-025.** When selection is indeterminate and no conclusively matching independent setting exists, retain the confirmed state rather than interpret unavailable as evidence for DEFAULT. |
| D-014 | **Active for ordinary warm operation; startup amended by D-025.** A transient incomplete warm raid does not itself mandate a new SOM transition. Same-setting reapplication is permitted when needed. Logs distinguish selection, application, reapplication, acknowledgement, and simulation. |
| D-015 | **Historical acceptance retained.** Phase 1A was closed as DONE—CONTAINED. The later Futures boundary-fix acceptance strengthens that record without rewriting it. |
| D-016 | **Active.** Analytical duration comes from MarketTrend.TrendMinutes, with explicit endpoint contracts per metric. Five-minute OHLCV is source resolution. Lookback N counts trend-sized periods. |
| D-017 | **Active, caller validation strengthened by D-028.** GlobalSetting, SMS activation, and SMS OffTrigger logic use true/false/unavailable. A conclusively true expression can match despite an unused unavailable branch. |
| D-018 | **Active.** Display all distinct grouped metric warnings in the raid summary. Group duplicates; do not reintroduce the superseded five-group truncation. |
| D-019 | **Active.** Phase 1C uses complete UTC trend-sized periods. Defaults: ATRPeriod=14, VolumeExpansionLookback=20, ATRPBreadthThreshold=0.5%, VolumeExpansionBreadthThreshold=1.0x, StrongVolumeExpansionThreshold=1.5x, TopNVolumeCount=10. Medians/breadth use 90% coverage; volume HHI/shares require their complete eligible volume population. |
| D-020 | **Superseded by D-023/D-024.** The selective legacy PriceTrend optimization was an intermediate architecture. Its removed test project and CMC/legacy behavior are not current requirements. |
| D-021 | **Active.** Assistant owns source review, implementation, regression authorship, and fixes. User owns local .NET builds, harness execution, and configured runtime checks. Automatic GitHub Actions/remote execution is opt-in. |
| D-022 | **Active.** Every verification handoff supplies complete fail-fast PowerShell, git pull, exact source SHA, dotnet build, exact current harness paths, and runtime acceptance instructions. |

## D-023 — Unified normalized PriceTrend and supported exchange scope

**Decision origin:** November 4, 2026 user instruction; consolidated November 7.

All supported Exchange MarketTrends use the normalized engine. Supported application exchanges are Binance Futures, Binance Spot, and Binance US. CoinMarketCap and the obsolete Bittrex/Poloniex paths are removed.

- Omitted or blank MarketTrend.Metrics enables normalized PriceTrend.
- A nonempty Metrics value explicitly selects published metrics.
- An omitted Trigger.Metric or OffTrigger.Metric requires normalized PriceTrend through the dependency mechanism.
- An explicitly named metric must be enabled on its referenced trend.
- A calculation may use internal dependencies without publishing them as selected outputs.
- Exchange TrendMinutes must be positive and exactly representable by the five-minute source.
- Runtime support in source does not establish identical acceptance on all exchanges or quote currencies.

[Original migration record](updates/2026-11-04-cmc-legacy-pricetrend-cleanup.md).

## D-024 — PriceTrend compatibility semantics

**Decision origin:** November 5, 2026; consolidated November 7.

- Global arithmetic PriceTrend uses the configured global population, including MaxMarkets.
- SMS Relative PriceTrend uses a separately computed uncapped asset-population reference.
- TrendThreshold filters the arithmetic PriceTrend means only. It does not suppress per-asset observations or remove markets from breadth, median, dispersion, MeanMedianSpread, volume, or concentration calculations.
- RelativeStrengthMarket retains its own documented market-median comparison; it is not the SMS Relative reference.
- Fiat PriceTrend combines synchronized asset/quote and quote/USDT return factors on the same exchange. USD/USDT use the existing identity convention. Missing conversion inputs remain unavailable.
- USDT identity-case tests do not establish non-USDT conversion acceptance.

[Compatibility restoration](updates/2026-11-05-pricetrend-compatibility-restoration.md) · [Recorded Futures validation](updates/2026-11-05-price-compatibility-nine-raid-testmode.md).

## D-025 — Startup SOM goal and release condition

**SUPERSEDED where this section describes automatic release.** D-047 now forbids global SOM OFF requests; this older text is historical only.

**User instruction:** November 7, 2026, assessment item 2D.

Application.StartupSellOnlyMode defaults to true. The startup goal is to establish sell-only protection before lengthy exchange bootstrap and retain it until a fresh raid reaches a conclusive decision under D-017 and PT acknowledges the resulting normal configuration.

The user subsequently rejected the initial unpublished implementation that submitted a full preset with pair SOM properties forced to true. [D-037](#d-037--direct-global-som-api-supersedes-the-startup-preset-overlay) replaces that mechanism with the direct global SOM API. No startup shadow preset or startup PAIRS/DCA/INDICATORS submission is part of the current design.

- Initial guard failure is not reported as successful protection. The raid stops before slow bootstrap and retries at the next interval.
- An indeterminate, stale, or failed raid cannot authorize releasing the guard.
- A failed normal-configuration delivery leaves pending work explicit; it does not authorize global SOM disablement.
- Normal configuration acknowledgement is a prerequisite for release, not evidence that the separate release API call succeeded.
- TestMode records simulation and sends no state-changing guard or configuration requests.
- StartupSellOnlyMode=false prevents acquiring a new API guard. Previously recorded pending PTM-owned guard work is still reconciled. Indeterminate or stale startup still cannot force DEFAULT as a fabricated prior state; retain a known confirmed state or defer publication while prior state is unknown.
- The guard uses PT's global SOM control. As clarified by the user, it stops new buys and DCA buys while allowing sells. It does not rewrite pair SOM properties, DCA, indicators, or sell settings.

This amends the startup portion of D-013/D-014. It does not add automatic SOM transitions to every incomplete warm raid.

## D-026 — Desired, pending, and confirmed delivery state

**User instruction:** November 7, assessment item 2B.

Configuration selection is distinct from confirmed application. PT delivery returns an explicit result. Failed or incomplete transfer remains pending and is retried even when the selected configuration has not changed.

Recompile from the current setting definition and preset contents even when the setting name is unchanged. A partial multi-target failure requires replay to every target; returning to an earlier confirmed payload does not clear that pending uncertainty.

Only acknowledged non-TestMode application advances the confirmed configuration checkpoint, stored in `_data/ConfigurationDeliveryState.json`. The checkpoint records configuration identity and payload hash, not raw properties, credentials, or license values. TestMode does not overwrite this checkpoint.

Logs and summaries must not claim that PT was updated solely because a configuration was compiled or a call returned after swallowing an error. Do not clear pending delivery state during ordinary raid cleanup.

## D-027 — SMS removal is a configuration transition

**User instruction:** November 7, assessment item 2A.

A transition from an applied nonempty SMS set to an empty set must generate the clean global configuration and require delivery, even if the GlobalSetting remains unchanged. Comparing only already-clean in-memory property lists cannot establish whether PT still has previous SMS overrides.

The remembered SMS set must follow the correct lifecycle, including empty transitions and failed delivery. Repeating an acknowledged unchanged configuration should not cause unnecessary retransmission.

## D-028 — Trigger identity, references, and editor preservation

**User instruction:** November 7, assessment items 2C/2E.

- Distinct triggers on the same MarketTrend retain separate identities, Metric, Tag, thresholds, relations, and other fields through Monitor load/save.
- A no-edit save must preserve configuration meaning, including full numeric precision.
- Global, SMS activation, and SMS OffTrigger references are validated consistently; missing or ambiguous reference identity must not silently become false or disappear from an AND expression.
- Custom expressions require the declared, unambiguous tags they use. AND/OR connections retain their supported untagged form.
- Runtime data availability still uses D-017. Intentional unavailable-metric diagnostics must remain distinguishable from structurally invalid references.
- No validation change may turn NOT unavailable into true or discard an unavailable condition from AND.

The current structural validator rejects missing MarketTrend references; blank or duplicate case-insensitive trend/setting names; duplicate nonblank tags; undeclared tags or malformed custom Boolean expressions; unsupported OffTriggerConnection values outside AND/OR; and invalid active metric parameter ranges. Unknown, disabled, or wrong-scope metric references remain accepted diagnostic configurations whose values are unavailable with warnings. This preserves the deliberate diagnostic fixtures used in prior validation.

The Monitor applies edits to detached ordered rows by original row index and verifies a SHA256 revision token before saving. New rows receive unique identities. Interleaved metric, age, volume, and time rows, omitted fields, inactive fields, native property values, and invariant numeric precision must survive the round trip.

The Monitor is part of the supported configuration lifecycle, not merely a viewer.

Unavailable SMS activation or OffTrigger expressions keep initial selection indeterminate; an already active ordinary SMS is retained when its activation becomes unavailable. Missing/sentinel/future age or activation-time observations and nonfinite/negative volume are unavailable rather than fabricated false or zero values. Conclusive three-valued expressions retain the normal AND/OR masking rules.

## D-029 — Pinned acquisition and bounded decision age

**User instruction:** November 7, assessment item 3.

Use one pinned UTC analysis boundary for normalized acquisition and evaluation. Per-symbol network requests must preserve the complete historical window required at that boundary, including tight retention when the fetch spans a new candle close.

Application.MaxAnalysisAgeSeconds defaults to 300 and accepts 1–86400 seconds. Decision freshness compares actual decision time with the pinned raid time. A missing, future, or expired pin prevents new normal configuration decisions from being published and keeps the startup guard where applicable.

Every normal configuration requires a completed raid analysis and a fresh runtime pin, including configurations whose conditions use only volume, age, or time. Omitting analytical trends does not bypass freshness or startup-release requirements.

This is separate from a metric's legitimate latest completed four-hour/daily endpoint. Do not apply a universal five-minute source-age rule to every analytical duration.

The previous boundary-fix acceptance remains valid for its tested case; the November 7 extension requires fresh validation.

## D-030 — Explicit history requirements

**User instruction:** November 7, assessment item 5.

Each enabled metric and internal dependency reports the history it requires. Retention is configured explicitly; the application does not silently increase StoreDataMaxHours or calculate shortened metrics.

Required complete-period lower bounds include:

- PriceTrend: two exact closes separated by TrendMinutes.
- ATR(P): P+1 complete trend bars, default 15 bars.
- VolumeExpansion(N): current complete bar plus N preceding complete bars, default 21.
- Correlation(N): N synchronized returns from N+1 trend-duration endpoints, with complete required source observations.
- Return Concentration ranking: the configured TrendMinutes volume window under D-031.

The exported HistoryRequirements report distinguishes minimum complete-source history, current-raid required stored slots (including the forming source candle and partial UTC trend period), the current-raid minimum StoreDataMaxHours, and conservative retention sufficient at every UTC alignment. It also reports configured capacity and insufficiency warnings. Capacity follows the production store's ceiling(hours / source interval) + 2 rule.

At a 24-hour trend duration with the default parameters, conservative StoreDataMaxHours guidance is 384 hours for ATR(14), 528 hours for VolumeExpansion(20), and 744 hours for Correlation(30). These are different from the complete-period lower bounds above. Do not describe 360 hours of complete ATR periods as sufficient at every point in a UTC day.

Insufficient configured history produces an explicit requirement warning and unavailable dependent values; it does not itself reject the entire configuration or silently resize retention. Unrelated valid metrics remain usable.

## D-031 — Return Concentration ranking window

**User instruction:** November 7, assessment item 5; resolves P1B-CONC-WINDOW in source.

Concentration keeps its established Top10 return-advantage meaning and percentage-point units. Rank the eligible population by complete quote volume over MarketTrend.TrendMinutes ending at the same normalized five-minute endpoint as the relevant return, replacing the fixed trailing 24-hour ranking window.

Keep the 100% eligible ranking/return coverage requirement. The calculation remains the mean return of the ten highest-volume eligible markets minus the mean return of the remaining eligible markets, requiring at least eleven markets. This is a deliberate semantic correction for non-24-hour trends and requires numerical/runtime revalidation; it is not covered by the prior 88-check baseline.

## D-032 — Performance work after all new metrics

**User instruction:** November 7, assessment item 4.

Defer the dedicated performance program until completion of **all approved new metric additions**, including derivatives ingestion/aggregation, higher-order measurements, and liquidity/depth families.

Deferred work includes legacy cold-start reconstruction optimization, shared or cross-raid snapshot caching, broader stateful incremental calculation, logging-volume optimization, allocation/GC work, and comparative CPU/network benchmarking.

Correctness, bounded storage, clear diagnostics, and respecting endpoint limits remain necessary during metric implementation. This does not authorize reopening a performance project before the agreed gate.

D-032 supersedes earlier Phase 1D handoff requirements to establish snapshot reuse as part of correlation, earlier optional-performance priority wording, and the November 7 assessment's suggested early optimization sequence.

## D-033 — Phase 1D correlation contract

**Authorized:** November 7, assessment item 8. Implementation choices below are part of the approved work. All 21 correlation harness checks passed at `86c2ea3`; configured runtime acceptance remains pending.

- Asset metric: CorrelationToBTC.
- Global metrics: MeanCorrelationToBTC and MedianCorrelationToBTC.
- Statistic: Pearson correlation of simple returns, coefficient in [-1,+1], unitless.
- MarketTrend.CorrelationLookback defaults to 30, valid range 3–1000.
- Use N returns and N+1 exact UTC-aligned complete TrendMinutes close endpoints.
- Require all observations in the declared vector; no zero fill, forward fill, shifted index matching, or reduced-overlap substitute.
- Missing source history, timestamp mismatch, nonfinite values, or zero variance produce unavailable values.
- BTC self-correlation is +1 only when its full vector is valid with nonzero variance.
- Global aggregates use the exact selected global population and 90% coverage. BTC is included only if it belongs to that selected population; no hidden denominator adjustment.
- Reuse normalized inputs; no new exchange endpoint solely for correlation.
- Full pairwise correlation remains an optional later feature requiring a separate value/cost decision.

## D-034 — Minimal native decision history

**Authorized:** November 7, assessment item 8.

Application defaults:

| Property | Default |
|---|---:|
| DecisionHistoryEnabled | true |
| DecisionHistoryRetentionDays | 30 |
| DecisionHistoryMaxMegabytes | 256 |

Retention accepts 1–3650 days; the quota accepts 16–102400 MiB. Oversized individual records are rejected rather than violating the segment bound.

Append JSONL records under `_data/DecisionHistory/YYYY-MM-DD-NNNNNN.jsonl`, rotating at 16 MiB and pruning complete oldest files by age and total quota.

Records identify the source/version, configuration and desired/confirmed payload hashes, analysis/decision times, evaluated metric inputs and validity, selection/SMS state, startup guard, and delivery outcome. Failed/pre-bootstrap raids record safe status/error categories when configuration and history services are ready.

Do not persist license values, tokens, raw general settings, raw PT payloads, or raw exception strings that may contain secrets. This is a bounded audit trail, not the complete Phase 6 backtest system or a persistent normalized candle cache.

All 13 decision-history harness checks passed at `d331fbd`, including bounded files, acknowledgement isolation, and production capture paths. Configured runtime integration remains separate from this deterministic evidence.

## D-035 — Application scope is independent of personal strategy development

**User instruction:** November 7, assessment item 7.

Personal strategy design, strategy repositories, long/short preset development, and strategy profitability are not PTMagic 2.10 deliverables, acceptance gates, or documentation dependencies. Use application-owned neutral fixtures to verify the engine.

Native analysis history and optional later interfaces to outcome data remain application capabilities; they do not absorb a personal trading-strategy project into this roadmap.

## D-036 — Acceptance and provenance

**Consolidated:** November 7.

Distinguish:

1. Source implemented.
2. Source inspected.
3. Deterministic tests authored.
4. Build/tests actually executed.
5. Configured TestMode behavior observed.
6. Actual PT acknowledgement/application observed.
7. Monitor/browser behavior observed.

A previous successful run does not validate later source. TestMode deliberately suppresses PT writes, so it cannot establish actual guard or configuration delivery. Record exact source/binary identity where available and label inferred provenance explicitly.

The accepted pre-change runtime baseline remains the November 5 build, 88 checks, and nine Futures USDT TestMode raids associated with d0b0b87. The November 7 deterministic inventory is now complete across two recorded revisions: ten harnesses passed 193 checks at `86c2ea3`, and the two-harness continuation passed 66 lifecycle plus 13 history checks at `d331fbd`. Only the fixture type qualifications and README evidence changed between those runs; production code and assertions were unchanged. Record the combined 272 passes with both source identities, not as a single twelve-project run at `d331fbd`. Subsequent documentation-only evidence updates do not require repeating those checks. Configured runtime, actual PT acknowledgement, and browser acceptance remain open.

## D-037 — Direct global SOM API supersedes the startup preset overlay

**SUPERSEDED in its ownership/automatic-release details by D-047.** Keep the original API transport and no-shadow-preset principle, but all references below to automatic `enabled=false`, ownership of the user's SOM flag and release retries are obsolete.

**User instruction:** November 7, 2026, after inspection of the initial startup implementation.

Use the ProfitTrailer control endpoint supplied in the user's Swagger excerpt:

```text
POST /api/v2/globalSellOnlyMode
query: token=<configured API token>&enabled=true|false
```

The initial unpublished full-preset overlay was rejected because it could reapply local preset changes and remove existing SMS/manual overrides before analysis. Startup protection now sends the global SOM control request without any PAIRS, DCA, or INDICATORS payload. The endpoint is resolved beneath each configured PT Monitor base URL, including any path prefix. Private instance addresses and real tokens do not belong in repository examples or logs.

The user clarified the native endpoint's behavior: global SOM stops new buys and DCA buys while allowing sells. The startup request therefore protects both kinds of buying without uploading a configuration preset.

Before slow market-data bootstrap, establish global SOM with `enabled=true` on every configured PT target and record its outcome separately from the configuration-delivery checkpoint. After a fresh conclusive raid, deliver the fully computed normal global/SMS configuration while protection remains enabled. Only then request `enabled=false`; that release requires its own acknowledgement and retry state.

`StartupSellOnlyMode=true` explicitly assigns control of the global SOM flag to PTMagic for this startup cycle. The verified input contract is a setter; the implementation does not read or restore an unknown prior global flag. Even if global SOM was already enabled before startup, PTMagic requests `enabled=false` after the release prerequisites are satisfied. Do not describe this as preserving an independently managed global SOM state.

Use `Application.ProfitTrailerServerAPIToken` for the primary PT target. `Application.ProfitTrailerServerAPITokenXtra` supplies comma-separated tokens aligned with the additional configured PT Monitor URLs. Its default empty value explicitly reuses the primary token for those additional targets. The base URL's path prefix must be retained.

Persist guard metadata separately in `_data/StartupSellOnlyModeState.json`; it contains no token, license, or raw properties. Guard enable acknowledgement must not mark a preset as applied. A successful normal configuration upload alone must never be recorded as successful global SOM release. Enable failure prevents slow bootstrap; release failure preserves the acknowledged normal configuration and leaves guard release pending for a fresh conclusive retry.

Persist the pending intent before sending enabled=true. If that intent cannot be recorded, defer the command and bootstrap rather than leave an unrecorded owned guard. If saving metadata fails after a command acknowledgement, retain the actual acknowledgement and report the I/O error; the earlier pending intent supports conservative recovery.

Acknowledgement is the command response; it is not a subsequent readback of PT's live global flag. Partial target failure or timeout leaves remote state uncertain. Reassert the owned guard before the next load and retry eligible release after fresh conclusive analysis; never present one target's acknowledgement as complete multi-target success.

Summary and decision history expose StartupSellOnlyModeActive, StartupSellOnlyModePending, and StartupSellOnlyModeStatus separately from ConfigurationDeliveryStatus. The Monitor's general settings page exposes the startup global SOM option and additional-target API tokens. The active flag alone must not hide pending or unconfirmed delivery.

TestMode makes no SOM API calls and writes neither live acknowledgement checkpoint. Disabling the startup option prevents a new guard; it does not automatically clear an untracked existing global SOM flag. A matching checkpoint with pending PTM-owned release still resumes recovery, even after opt-out, so the earlier owned guard is not stranded. Neither the user-supplied endpoint contract nor source implementation is evidence that the new code has passed native PT acceptance; record that separately under D-021/D-036.

This decision replaces the transport and payload design originally drafted for D-025. The conclusive/fresh/acknowledged normal-configuration prerequisite remains active. Dedicated performance ordering and independent strategy scope are unchanged.

## D-038 — Standing authorization to publish PTM 2.10 development

**User instruction:** November 7, 2026. The user explicitly approved publication and instructed the assistant to stop asking again.

The assistant is authorized to commit and publish PTM 2.10 application development changes and their roadmap, handoff, and evidence updates to these destinations:

| Repository | Branch |
|---|---|
| HojouFotytu/PTMagic | `phase1/market-data-foundation` |
| HojouFotytu/PTM_2.10_Roadmaps_Handoffs | `main` |

This authorization persists across subsequent development work in the agreed PTM 2.10 scope. Continue publication to these branches without renewed conversational approval. Actual tool-level restrictions still apply; if a tool blocks an action, report the specific restriction without treating the user's existing authorization as missing or asking for the same consent again.

This decision covers application and documentation development. It does not extend to the user's independent personal strategy work or authorize live ProfitTrailer/API/trading actions. D-021 and D-022 remain active: the user runs local builds, harnesses, and configured runtime checks, and handoffs retain exact source pins and verification commands. Publication does not establish execution acceptance.

## D-039 — Cumulative effective-change record for PRs and merges

**User instruction:** November 7, 2026. Create a record from the beginning of 2.10 through the current implementation, including only changes that remain in effect.

Maintain [CHANGELOG-2.10.md](CHANGELOG-2.10.md) in this repository and an identical application-repository copy that is included in 2.10 code merges. Update the applicable sections whenever a PR changes behavior, metrics, settings, compatibility, diagnostics or validation, and reference those sections in PR, merge and release descriptions. Synchronize both copies as part of the same development handoff.

The record describes the cumulative resulting release, beginning with the normalized foundation on November 2, rather than a sequence of interim implementations. Consolidate or remove an entry when it is replaced or reversed. Keep planned work in the roadmap, chronological provenance in dated records/source control, and personal strategy development outside application scope. Retain exact tested-source identities and acceptance limits when describing validation.

The initial record includes the native startup global SOM setting, both supplied general-settings templates and the Monitor General Settings APPLICATION toggle. The packaged template already declared the true default; the development template now declares it explicitly too. Monitor already has on/off persistence; visible help now states that TestMode leaves the remote SOM flag unchanged.

## D-040 — Targeted persistent OHLCV warm start now

**User instruction:** November 9, 2026, following repeated short-restart full downloads.

Implement a persistent cache now for **normalized five-minute OHLCV candles**. Save validated complete candle histories locally, reload the cache on startup, and use the existing pinned refresh and coverage gates to fetch only missing/overlapping candles or repair incomplete history.

Keep exchange identity isolation, bounded history, strict validation, fail-open corrupt/missing-cache behavior, atomic file replacement, and cache-write throttling. Cache content must never establish a metric as available without passing the existing completeness, source-timestamp, freshness and population checks. Cache I/O failure must not change ProfitTrailer delivery or SOM acknowledgement.

This **specific warm-start optimization** is an accepted exception to D-032. The dedicated wider performance program (legacy reconstruction redesign, cross-raid vector reuse, allocation profiling, etc.) is still deferred until all approved metrics are complete.

Published implementation source: `925db7c153ee4d53cfe3b7bf736318e7a30bccf1`. Eight focused tests **passed** at `925db7c` on November 9; the .NET solution build and two existing relevant harnesses passed in the same 37/37-check run; configured cold/restart acceptance is **pending** under D-021. Existing 272 passed checks from prior commits remain valid only for their executed revisions. Cache does not yet eliminate legacy tick reconstruction or first-seen-date acquisition.

## D-041 — Uniform TestMode console color

**User instruction:** November 9, 2026.

All TestMode-related PTMagic and Monitor console lines should use the same purple/magenta color as the startup `TESTMODE ENABLED` warning. Use NLog `ColoredConsole` message-based highlighting (case-insensitive), not a changed log level. Preserve INFO/WARN meaning, normal unrelated colors and uncolored file logs. Keep the application, Monitor and packaged default logging configs aligned.

Application source `87b9eaa1c865e39d8fff6a657e1b332012be8c16` implements the shared rule. Source inspection is complete; user-local .NET build and live Windows console rendering are not yet verified. A source update alone cannot replace a running instance's already-installed `nlog.config`.

## D-047 — Startup global SOM is enable-only; manual PT release

**Owner directive:** November 10, 2026.

PTMagic may enable ProfitTrailer's native global SOM on a new disruptive startup when configured, but **must never turn it OFF automatically**. The user manually releases SOM from ProfitTrailer when ready; the software does not assume ownership of an already enabled SOM or of manual changes made later. Automatic release after normal setting acknowledgement is withdrawn. The global SOM API adapter must reject any `enabled=false` request to prevent accidental old-call-site releases. Enabling global SOM must not alter PAIRS, DCA or INDICATORS settings. Failed or unconfirmed enable commands must not be silently treated as safe startup protection.

Legacy v1 checkpoints containing a pending automatic release must not trigger an off request. Migrate to v2 enable-intent/acknowledgement/manual-review metadata and preserve explicit pending uncertainty. TestMode never calls the PT global SOM API.

**Owner UI directive:** On first and second startup raids, issue a prominent warning in the RAID SUMMARY explaining that PTMagic requested SOM ON and the user must turn it off manually when ready. Show a **red `PT: SOM`** indicator alongside the global setting, SMS and PT health top Monitor tickers for those same first two raids, with an `(i)` tooltip. The ticker disappears after raid 2, but does not represent the actual PT global flag or remove the user's obligation to review it. Keep additional manual-review details available in the Status Summary.

This decision supersedes the automatic-release paragraphs of **D-025 and D-037**; their separately acknowledged normal configuration delivery and startup enable/freshness safeguards remain valid. New implementation published at `891f709010c867259a6cde3df8e9c82781091b7f`, with local build/regression acceptance still pending.

## D-046 — Binance USD-M funding metrics use settled events and dynamic history

**Date:** November 10, 2026. Opt-in `FundingRate` and `FundingSum` are per-asset percentage-point metrics of **Regular** historical funding settlements (native decimal ×100). Preserve Special and unknown types separately; never treat an unknown type as a regular zero. The full user-specified MarketTrend window must be source-verified, not replaced with an assumed 8-hour funding period. `FundingRate` is the latest regular settlement in that window, unavailable if none. `FundingSum` is the arithmetic sum of regular settlements, valid zero only for fully verified empty regular history. No annualization or future estimated rates.

Use the historical Binance USD-M `fundingRate` endpoint with pinned time, limited pages, fair request budgeting, and incomplete/failed history remaining unavailable. Funding history derives exclusively from configured funding-enabled MarketTrends, not an independent fixed retention setting. The request budget (default 60 pages/raid) is a separate operational throttle. Futures-only; no queries on Spot/US. Provider's `fundingIntervalHours` changes and interval metadata require distinct handling from raw settlement history.

Source published at `6430bab1afa262fadd4ae31199c11084508b28c7`; **new funding build and deterministic test results pending** under D-045. Earlier OI 315/315 tests remain verified only at their actual tested revision.

## D-045 — Development tests are not deferred

**Owner clarification:** November 10, 2026.

D-042 deferred only the remaining Phase 1 configured integration checks explicitly discussed before proceeding to Phase 2. This never deferred normal Phase 2 builds, new-feature unit/scenario tests, affected regression harnesses, or fixing and re-running failed tests. Every new code batch requires execution evidence tied to the actual source SHA before it can be reported as validated. Authored but unexecuted tests do not count as PASS.

The remaining Phase 1 real PT API, Monitor/browser, selected cross-exchange and restart tests stay pending for a future integration/release gate. They are not a reason to skip ordinary Phase 2 verification. Use the fail-fast PowerShell runner documented in the current Phase 2 handoff.

## D-044 — Open-interest history derives from configured MarketTrends

**HISTORICAL — superseded entirely for future scope by D-053 (November 12).** This records prior implemented behavior, not an active requirement.

**Owner instruction:** November 10, 2026.

Remove the independent OI retention-hours setting and any fixed application history horizon. All OI data requirements must follow the user's explicit OI-enabled MarketTrends, just as the existing normalized metric families use their own TrendMinutes and lookbacks. Retain enough source observations for the longest required OI duration, with the exact reference and overlap. Recompute the requirement on configuration changes. The exchange's supported historical availability is an external limitation to report as unavailable, never justification for silently truncating a user's chosen trend. The OI request budget is a separate operational throttle, not a retention setting. Fixed-size corruption protections do not dictate metric history. Published at `0ae76f4c7886397a06ad346b42a375f6aa06be00`; native build/tests remain unexecuted.

## D-043 — Opt-in bounded Binance Futures open-interest metrics

**HISTORICAL — superseded entirely for future scope by D-053 (November 12).** The OI metrics and acquisition are withdrawn.

**Implementation record:** November 10, 2026.

Historical Binance USD-M open interest is sourced separately from normalized OHLCV, without any implied requests in PriceTrend-only settings. Add explicit per-asset `OpenInterestChange` and `OpenInterestValueChange` metrics (both percent changes from exact 5m provider endpoints), preserving native quantity and reported value independently. Missing, inconsistent, stale or insufficient source remains unavailable; no conversion or interpolation. Limit network requests and source retention separately from `StoreDataMaxHours`. The first batch adds a bounded serialized collector, compressed persistent cache, and existing metric/trigger/export integration. These are implemented, **not yet compiled or acceptance-tested**. Owner-deferral of testing under D-042 remains active.

## D-042 — Start Phase 2 and defer remaining Phase 1 testing

**Owner instruction:** November 10, 2026.

Continue PTMagic 2.10 **application** development from Phase 2 futures raw observations without waiting for further Phase 1 runtime, native PT API, Monitor/browser or two-startup cache testing. These are explicitly deferred, not passed or waived; retain their evidence and release-acceptance obligations. Do not request repeat tests of previously reviewed captures. Continue source implementation and clearly label authored versus executed tests.

Phase 2 concerns data acquisition, normalization, calculations, registry/trigger/Monitor integration and diagnostics **inside PTMagic**. Personal LONG/SHORT strategy settings and PT property trios are outside scope.

Published first source slice: `314214b1a20bcddd1643b8fa8df032db5463b04d` (open-interest raw models and opt-in client); offline 18-case harness **not run**. Resume later acceptance only when the user explicitly reopens testing or release readiness requires it.

## Remaining open design decisions

- Phase 2 endpoint availability, supported exchange/contract scope, units, history limits, cadence, and retention must be verified against current official API documentation before implementation.
- Derivatives weighting and aggregation coverage are defined per metric family, not inherited blindly from raw notional size.
- Higher-order state formulas and any component weights require explicit transparent contracts.
- Liquidity sampling, book freshness, notional sizes, and depth aggregation remain planned.
- Full Phase 6 history schema/query engine and independent chronological validation remain planned.
- Pairwise correlation has not been approved for first-release implementation.

The previously open Phase 1C formula choices were resolved by its implemented and accepted contract; do not reopen them as if ATRP and volume expansion had not been developed.


## D-048 — Preserve the existing DashboardTop refresh mechanism; refresh only required card data

**Owner direction:** November 11, 2026.

The dashboard needs current **Possible Buys (PBL)** and **Positions** data. Preserve the existing DashboardTop jQuery `.load()` request and its callback. The authorized refresh correction is **scheduling-only in `Monitor/Pages/Index.cshtml`**; do not replace the request mechanism, add endpoints/count caches, change PBL/Positions retrieval or calculations, modify DashboardTop rendering, or alter the separate ticker tooltip-preservation code, DashboardBottom, tooltip behavior or profit coloring. Do not reintroduce the experimental `PossibleBuysCount` endpoint, asynchronous count cache, or custom AJAX replacement.

Before any source edit, explain the exact proposed scheduling change, affected files, and scope, then wait for the owner's review. No refresh fix is yet approved or implemented. The current dashboard/PBL source files are restored to exact baseline `438acbe` blobs. The top refresh defect remains open. November 2 callback-driven polling changes (`ec19a5e`, `26ce2d8`) are a code-level investigation lead, not a runtime-confirmed root cause. See [November 11 dashboard refresh history and current state](updates/2026-11-11-dashboard-refresh-history-and-current-state.md).


## D-049 — Binance Futures long/short ratio metric contract

**HISTORICAL — superseded first by D-051 and now fully excluded by D-053.**

**Historical owner direction:** November 11, 2026. **Superseded on November 11 by D-051.** The three-source/top-trader design and optional API-key requirement below are preserved as historical rationale, not current scope.

Implement three separate, opt-in, asset-scoped Binance USD-M Futures metrics: `GlobalLongShortAccountRatio`, `TopTraderLongShortAccountRatio`, and `TopTraderLongShortPositionRatio`. Global account participation, top-trader account counts and top-trader position-size participation are distinct and must not be conflated. No exchange-wide aggregates are introduced in this batch.

Use native five-minute observations over each configured MarketTrend's exact `TrendMinutes` window. Preserve provider `longShortRatio`, `longAccount` and `shortAccount` independently. Calculate the window metric by converting each provider ratio to its implied long-side share `r/(1+r)`, averaging those shares, then converting the mean back to a ratio. Neutral is 1.0. Require every expected five-minute observation; never interpolate, use a nearest timestamp, fill zero or silently shorten the window.

The two top-trader endpoints require an optional Binance API key with read-only market-data access; no API secret or signed request is required. Do not echo the key in Monitor or log it. Missing credentials leave only the top-trader metrics unavailable; the global account source remains usable.

All three sources share a bounded per-raid request budget (default 60; zero disables; maximum 80), fair source/symbol scheduling and at most two pages per source/symbol per raid. Provider history is limited to the latest 30 days and 500 rows per request. Disk persistence for ratios and funding was subsequently added under D-050; service-level restart and configured two-startup acceptance remain pending.

Implementation is published on the existing `phase1/market-data-foundation` branch. The .NET 10 solution build and all 17 offline harnesses passed at `875b4feb71104fbc609bd07dc3120405218d325f`. Live Binance/API-key acceptance, end-to-end service restart acceptance and Monitor browser verification remain pending.


## D-050 — Persist Futures funding and long/short ratio histories

**Partially superseded by D-053:** settled-funding persistence remains approved; OI and ratio persistence become historical and are no longer active feature requirements.

**Implementation direction:** November 11, 2026.

Funding and the retained Binance USD-M Futures global-account long/short ratio data source use disk persistence, consistent with the existing OI and normalized OHLCV warm-start approach. The original all-three-source wording is superseded by D-051. The active runtime paths are:

- OI: `_data/DerivativesOpenInterestCache` (existing).
- Funding: `_data/DerivativesFundingCache`.
- Ratios: `_data/DerivativesLongShortRatioCache`, partitioned by source and symbol.

The funding and ratio caches store versioned compressed raw observations and verified provider-query coverage intervals. Coverage records mean a bounded provider query was exhausted; they are not synthetic observations and do not imply missing periods are zero. Cache writes use a temporary file and atomic replacement. Restore validates schema/version, symbol/source identity, timestamps, values and defensive size/count limits. Corrupt cache files are discarded fail-open so normal bounded incremental acquisition can repair the history.

Funding cache ordering permits distinct `Regular` and `Special` rate types at the same settlement timestamp while rejecting duplicate same-type observations. Ratio caches keep the three endpoint sources separate for each symbol.

**Verification:** the user executed a .NET 10.0.403 solution build (17.4s) and all 17 offline harnesses successfully at `875b4feb71104fbc609bd07dc3120405218d325f`. Direct cache save/restore, source isolation and corruption recovery tests passed. This does **not** yet prove end-to-end restoration through newly constructed data-service instances or configured two-startup request reduction. Those service-level tests and runtime acceptance remain required before persistence is considered fully accepted.


## D-051 — Public global-account ratio only; application-managed derivative acquisition

**Partially superseded by D-053:** the retained global-account ratio is now withdrawn; provider-safe admission, cooldowns and application-owned scheduling remain applicable to retained funding and future data families.

**Owner direction:** November 11, 2026.

Retain only the public, asset-scoped Binance USD-M Futures metric `GlobalLongShortAccountRatio`. Remove `TopTraderLongShortAccountRatio` and `TopTraderLongShortPositionRatio` from the approved PTMagic 2.10 metric scope entirely. Do not retain them as disabled, optional, or credential-gated alternatives. Their account-count and position-size distinctions are no longer part of the active metric design.

The top-trader-only API-key dependency and authentication path are unnecessary for the retained ratio scope. No additional Binance API key should be required for the global-account ratio.

The three per-raid request-budget properties `OpenInterestMaxRequestsPerRaid`, `FundingMaxRequestsPerRaid`, and `LongShortRatioMaxRequestsPerRaid` are not user-facing controls. PTMagic must manage derivative acquisition internally and dynamically using the shared Binance rate-limit state, endpoint request weights, response headers and exchange cooldowns. Do not replace them with other arbitrary user-configurable static limits. The exact internal scheduler implementation and its validation remain future application work; this decision does not claim that adaptive scheduling is already implemented.

Retain internal safeguards needed for correctness and service stability: endpoint pagination limits, bounded per-symbol page progress, fair scheduling, incremental coverage, persistent caches, cancellation, retry/cooldown handling, and UNAVAILABLE semantics for missing data. These are application-owned mechanics, not user strategy settings.

This decision supersedes D-049's three-source ratio contract and static shared ratio request budget. Existing source/offline evidence remains historical evidence for the implementation at its tested revision; it does not validate the revised single-source/adaptive-scheduling design.

## D-052 — Strict separation of PTMagic application and ProfitTrailer strategy-settings development

**Owner direction:** November 11, 2026.

PTMagic 2.10 application development and ProfitTrailer LONG/SHORT strategy-settings development are independent workstreams with no implicit crossover. PTMagic code, API, data-acquisition, analytics, Monitor and PTMagic project documentation work must not trigger changes to the separate strategy-settings repositories or artifacts.

Do not modify LONG/SHORT strategy analyzers, GlobalSettings/SMS designs, PAIRS/DCA/INDICATORS property files, strategy settings repositories, or related settings-development documents during PTMagic work unless the user explicitly requests that separate work. Likewise, strategy-settings decisions do not authorize PTMagic source or configuration changes.

For this PTMagic request, the authorized action is limited to the PTM 2.10 roadmap/handoff documentation. No application source, PTMagic configuration/settings files, or ProfitTrailer strategy-settings files are changed by this documentation update.


## D-053 — Remove Binance Futures open-interest and long/short positioning metrics from PTMagic 2.10

**Owner direction:** November 12, 2026. **Implemented and source-audited at `892a5f1f`; post-removal build/runtime acceptance pending.**

Remove all three presently implemented asset-specific metrics:
- `OpenInterestChange`
- `OpenInterestValueChange`
- `GlobalLongShortAccountRatio`

Remove the OI and positioning-only endpoint clients, service models, acquisition and scheduling work, caches as active dependencies, metric registry entries, exported/Monitor calculations, trigger paths, and obsolete configuration controls/diagnostics when performing application cleanup. Do not merely disable the metrics or preserve a hidden legacy calculation path. Do not fabricate values for references to withdrawn names. Existing user data/cache files must not be silently deleted by this documentation decision. Update tests and the existing diagnostic test configuration when source removal is performed.

**Reason:** USD-M OI and global-account-ratio sources are symbol-specific. PTMagic's current conservative shared historical-data allowance is 800 requests per rolling five-minute window. The November 12 live raids showed exactly 800 combined OI/ratio requests, with 519 assets per family and rotating incomplete coverage. This makes a 90% current-window market-wide requirement unattainable for both families together under that acquisition model (at least 936 current requests for 519 assets if each family requires one per symbol). Do not presume the provider has independent quotas or relax the safety allowance as a workaround. The owner elects scope removal rather than an acquisition redesign for these metrics.

**Retain:** all 17 existing globally evaluable metrics; `RelativeStrengthMarket`, `RelativeStrengthBTC`, `ATRP`, `VolumeExpansion`, `CorrelationToBTC`, `FundingRate`, and `FundingSum` as the seven remaining asset-only metrics. The approved target registry is **24 metrics** (17 global-capable, including global/asset `PriceTrend`, and 7 asset-only). Funding's separate bulk acquisition, cache, exact settlement semantics and source-aware availability remain. Continue planned `TakerBuyRatio` and `TakerImbalance`, preferably deriving their inputs from existing Binance kline taker-buy fields if validated, then Phase 2B funding and taker-flow market aggregates.

**Withdraw from future roadmap:** OI median/expansion/contraction/extreme breadth; long/short account/position median, concentration and breadth; leverage expansion; OI/positioning-based long and short crowding; OI-based deleveraging; OI-dependent branches of flow confirmation/divergence and composite market stress. Flow confirmation/divergence may continue on price, volume and taker-flow evidence. Funding extremes, volatility, spread, book depth and liquidity stress remain eligible independent measurements, but funding alone must not be labeled as verified trader crowding.

**Implementation and evidence boundary:** On November 12 the user built and passed all 18 current offline harnesses at application source `d101b5a03e01f8f76acf8cc9a6bde7214ff34aa2` (80 ConfigurationLifecycle checks, eight pre-existing nullable warnings). That binary still contains the three withdrawn metrics. This is a **new roadmap decision**, not proof the removal is implemented, built, tested or live-accepted. Keep earlier commits and dated test evidence immutable as historical facts.

**Preserve:** the separate LONG/SHORT strategy-settings boundary (D-052), SOM enable-only safety (D-047), explicit underlying-type eligibility, frozen metric populations and strict UNAVAILABLE semantics. Only the PTMagic software/documentation workstream is authorized by this decision.


## D-054 — Opt-in kline-derived taker-flow metrics and legacy-cache compatibility

**Accepted and source-implemented:** November 12, 2026. **Post-implementation .NET build and runtime acceptance pending.**

Add `TakerBuyRatio` (summed taker-buy quote volume / summed total quote volume; 0–1) and `TakerImbalance` (twice that ratio minus one; −1 to +1) as **asset-only** metrics evaluated on the latest complete UTC-aligned `MarketTrend.TrendMinutes` period. Source is Binance kline index 10, not index 9; reuse the existing normalized 5m OHLCV feed, frozen populations and standard metric/trigger/Monitor pipeline. Do not add another provider endpoint or independent acquisition subsystem. Missing, malformed, stale or gapped taker volume and zero total quote volume remain UNAVAILABLE, never invented zero. Ratio and imbalance are algebraically dependent, not independent sources of market evidence.

Preserve legacy normalized OHLCV warm-start **version 1** cache compatibility for existing price/volume metrics; introduce nullable taker fields in **version 2** cache records and selectively source-verify only the needed taker period on configured trends. Verified taker repair must persist immediately despite the normal save throttle. Do not delete or invalidate the full old cache, or fetch extra taker data when disabled.

**Implemented reference:** application revision [`f7d802facfabb4611098d695d88a269d60daa278`](https://github.com/HojouFotytu/PTMagic/commit/f7d802facfabb4611098d695d88a269d60daa278); [implementation record](updates/2026-11-12-phase2-taker-flow-implementation.md). The existing TestMode analyzer is updated in place to 26 metrics (17 global-capable, nine asset-only). Only PTMagic software development is in scope; the user's personal LONG/SHORT settings and strategy repositories remain independent. This supersedes older language that taker flow is not yet implemented, but is **not** a build PASS claim.
