# PTMagic 2.10 — Current Decision Register

**Reconciled:** November 10, 2026

**Source checkpoint:** `0ae76f4c7886397a06ad346b42a375f6aa06be00`

**Scope:** PTMagic 2.10 application development. Personal trading-strategy work is independent.

This register governs current intent. “Accepted” identifies a design or user decision, not successful execution. [STATUS.md](STATUS.md) records implementation and evidence separately. The previous register is preserved in [history](history/2026-11-07-pre-reconciliation/DECISIONS.md); dated implementation records remain unchanged.

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

## D-046 — Binance USD-M funding metrics use settled events and dynamic history

**Date:** November 10, 2026. Opt-in `FundingRate` and `FundingSum` are per-asset percentage-point metrics of **Regular** historical funding settlements (native decimal ×100). Preserve Special and unknown types separately; never treat an unknown type as a regular zero. The full user-specified MarketTrend window must be source-verified, not replaced with an assumed 8-hour funding period. `FundingRate` is the latest regular settlement in that window, unavailable if none. `FundingSum` is the arithmetic sum of regular settlements, valid zero only for fully verified empty regular history. No annualization or future estimated rates.

Use the historical Binance USD-M `fundingRate` endpoint with pinned time, limited pages, fair request budgeting, and incomplete/failed history remaining unavailable. Funding history derives exclusively from configured funding-enabled MarketTrends, not an independent fixed retention setting. The request budget (default 60 pages/raid) is a separate operational throttle. Futures-only; no queries on Spot/US. Provider's `fundingIntervalHours` changes and interval metadata require distinct handling from raw settlement history.

Source published at `6430bab1afa262fadd4ae31199c11084508b28c7`; **new funding build and deterministic test results pending** under D-045. Earlier OI 315/315 tests remain verified only at their actual tested revision.

## D-045 — Development tests are not deferred

**Owner clarification:** November 10, 2026.

D-042 deferred only the remaining Phase 1 configured integration checks explicitly discussed before proceeding to Phase 2. This never deferred normal Phase 2 builds, new-feature unit/scenario tests, affected regression harnesses, or fixing and re-running failed tests. Every new code batch requires execution evidence tied to the actual source SHA before it can be reported as validated. Authored but unexecuted tests do not count as PASS.

The remaining Phase 1 real PT API, Monitor/browser, selected cross-exchange and restart tests stay pending for a future integration/release gate. They are not a reason to skip ordinary Phase 2 verification. Use the fail-fast PowerShell runner documented in the current Phase 2 handoff.

## D-044 — Open-interest history derives from configured MarketTrends

**Owner instruction:** November 10, 2026.

Remove the independent OI retention-hours setting and any fixed application history horizon. All OI data requirements must follow the user's explicit OI-enabled MarketTrends, just as the existing normalized metric families use their own TrendMinutes and lookbacks. Retain enough source observations for the longest required OI duration, with the exact reference and overlap. Recompute the requirement on configuration changes. The exchange's supported historical availability is an external limitation to report as unavailable, never justification for silently truncating a user's chosen trend. The OI request budget is a separate operational throttle, not a retention setting. Fixed-size corruption protections do not dictate metric history. Published at `0ae76f4c7886397a06ad346b42a375f6aa06be00`; native build/tests remain unexecuted.

## D-043 — Opt-in bounded Binance Futures open-interest metrics

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
