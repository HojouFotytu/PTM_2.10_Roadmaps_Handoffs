# PTMagic 2.10 — Current Technical Roadmap

**Current authority:** November 9, 2026

**Application:** [HojouFotytu/PTMagic](https://github.com/HojouFotytu/PTMagic), branch `phase1/market-data-foundation`

**Source checkpoint:** `87b9eaa1c865e39d8fff6a657e1b332012be8c16`

**Documentation:** [STATUS](../STATUS.md) · [DECISIONS](../DECISIONS.md) · [current handoff](../handoffs/2026-11-07-stabilization-correlation-validation.md)

This is the standalone current plan for PTMagic 2.10. It replaces the active guidance in the dated November 4 technical roadmaps while preserving those files as history. A reader does not need to reconstruct the old conversation to determine the current contract or next step.

Implementation and execution evidence are different states. All twelve harnesses now have passing results across the two recorded November 7 runs, totaling 272 checks. Configured runtime, actual PT API, and browser acceptance remain open. Each result retains its actual source identity.

## Uniform TestMode console diagnostics (D-041)

At the user's November 9 instruction, the `ColoredConsole` rules in PTMagic, Monitor and packaged default logging configuration now highlight case-insensitive `TestMode` text in purple/magenta at any severity. Normal file logs and severity classifications do not change. Source published as `87b9eaa1c865e39d8fff6a657e1b332012be8c16`; the user-local .NET build passed in 15.1s, and all three XML/rule checks passed on November 9. Visible Windows console color acceptance and installed-config deployment remain pending. Updating the deployed `nlog.config` is necessary if the running instance uses an older copy.

## Immediate targeted warm-start enhancement (D-040)

At the user's November 9 instruction, the persistent normalized OHLCV warm-start cache was implemented ahead of the broad performance program. Complete validated five-minute candles are saved under `_data/NormalizedOhlcvCache`, restored by exchange/symbol, and refreshed with the same pinned bounds; corrupt/incomplete caches fall back to full exchange fetching. File writes are throttled and atomic. The existing metric validity gates remain authoritative.

**Implementation published at `925db7c153ee4d53cfe3b7bf736318e7a30bccf1`. Seven focused tests authored; local build, harness execution and two-startup evidence are pending.** Previously recorded 272 passes belong to earlier revisions. This improvement does not alter legacy minute-tick reconstruction. Broader performance work stays deferred under D-032.

## 1. Purpose and scope

PTMagic measures market conditions and deterministically selects the PAIRS, DCA, and INDICATORS configuration sent to ProfitTrailer. ProfitTrailer remains responsible for native order and position execution.

The expanded application measures:

- Direction and return distribution.
- Market breadth and dispersion.
- Volatility and participation.
- Relative strength and concentration.
- Correlation and market cohesion.
- Futures open interest, funding, positioning, and taker flow.
- Transparent higher-order market conditions.
- Liquidity, depth, spread, and stress.

All analysis is implemented within PTMagic. No external AI service, AI-generated trading signals, or AI-driven settings authority is part of this architecture.

### Explicit project boundary

Personal trading strategies, their repositories, preset tuning, long/short development tracks, leverage choices, and trading profitability are independent of PTMagic 2.10. They must not be inserted into this roadmap or used as application acceptance gates. Application tests use neutral fixtures that exercise supported engine behavior.

PTMagic 2.9 modernization is complete historical work. The current target is 2.10; the application identifies as 2.10.0 and targets .NET 10. Previously reported 2.9 performance improvements are not measurements of the expanded 2.10 engine.

## 2. Current state and evidence

### Accepted pre-change baseline

At application source d0b0b87, the documentation records:

- A successful user-run .NET 10 build of Core, PTMagic, and Monitor.
- 88 passing deterministic checks in six console harnesses.
- Nine reviewed Binance Futures USDT TestMode raids.
- Full requested return coverage in the reported successful runs.
- 5,192 matching values between normalized analytics and runtime-summary outputs.
- Corrected uncapped SMS Relative reference behavior and PriceTrend-only threshold application.
- TestMode suppression of PT settings writes.

The deployed SHA in those logs was inferred from the preceding workflow; the binary printed 2.10.0, not a Git SHA. Matching normalized outputs demonstrate internal consistency, not old-engine numerical parity. A positive OffTrigger immediately reactivated because its entry remained true; sustained deactivation was not proven.

[Baseline evidence](../updates/2026-11-05-price-compatibility-nine-raid-testmode.md).

### November 7 implementation checkpoint

The current work adds:

1. Correct SMS-set transitions, including removal of the last active SMS.
2. Explicit configuration delivery results, retry state, and a confirmed-state checkpoint.
3. Initial global SOM through the PT control API, with a conclusive/fresh configuration and separately acknowledged release condition.
4. Monitor preservation of distinct trigger rows, tags, metrics, and precision.
5. Structural reference and expression validation.
6. Pinned acquisition boundaries, decision-age checks, and history requirement reporting.
7. The TrendMinutes ranking-window correction for return Concentration.
8. Three Phase 1D correlation metrics.
9. Bounded native decision-history records.
10. Main-market bootstrap validation and preservation of inherited default-file assignments when a property group is null.

**Deterministic execution is complete across two recorded revisions: ten harnesses passed 193 checks at `86c2ea3`, and the continuation at `d331fbd` passed all 66 ConfigurationLifecycle and 13 DecisionHistory checks.** The latest solution build succeeded with SDK 10.0.403 in 10.9 seconds. The total is 272 passing checks across twelve projects, not a single full-suite execution at one revision. [Detailed evidence](../updates/2026-11-07-completed-harness-validation.md).

The qualified Telegram fixture references are now verified by native execution; production source and test expectations were unchanged between the two tested revisions. Main-market parsing/inheritance, startup SOM orchestration, delivery retry, freshness, SMS transitions, and bounded history now have passing deterministic coverage. A later runtime log reproduces the old bare-USDT request and omits the current source/main-market logs. It executes pre-fix Core behavior with a runtime working directory separate from the checkout; its exact SHA and loaded DLL path are unknown. The next step explicitly selects the freshly built DLL with the existing runtime configuration and verifies identity in TestMode. This validation run does not permanently update the installed launcher, which needs a coherent application-bundle update before reuse. Actual PT and browser checks follow separately. Use the [current handoff](../handoffs/2026-11-07-stabilization-correlation-validation.md); its full twelve-project sequence remains a reference, with no rerun required for documentation-only updates.

### Phase map

| Stage | Present state |
|---|---|
| Phase 0 — architecture baseline | Completed historical audit; revisit specific changed assumptions when necessary |
| Phase 1A — normalized data/readiness | Implemented and accepted baseline; November 7 boundary/freshness/startup extensions require validation |
| Phase 1B — return-derived metrics | Implemented baseline; Concentration-window change requires new acceptance |
| Phase 1C — OHLC/volume metrics | Accepted baseline; new requirement reporting requires validation |
| Phase 1D — correlation | 21/21 deterministic checks passed at `86c2ea3`; configured runtime acceptance pending |
| Phase 1E — inspection and robustness | Deterministic lifecycle/editor/history checks passed; configured PT, browser, cross-exchange and failure-path acceptance remain |
| Phase 2 — futures raw observations | Planned |
| Phase 2B — futures market aggregation | Planned |
| Phase 3 — higher-order conditions | Planned |
| Phase 4 — trigger/UI integration | Implemented for current families, extended with each new family |
| Phase 5 — liquidity/depth/stress | Planned |
| Phase 6 — native history and historical analysis | Minimal decision audit trail has 13/13 passing checks at `d331fbd`; configured integration and the full analysis system remain |
| Post-metric performance program | Deferred until all approved metric additions are complete |

## 3. Architectural rules

### 3.1 Separate observations, calculations, decisions, and delivery

The production flow has distinct responsibilities:

| Layer | Responsibility |
|---|---|
| Exchange clients | Retrieve documented raw observations, respecting cancellation, timeouts, endpoint cadence, and request limits |
| Normalization and store | Validate and retain PTMagic-owned observations with UTC timestamps and explicit units |
| Population selection | Freeze the exact per-raid/per-trend eligible global and asset populations |
| Feature calculators | Produce deterministic values and availability metadata from normalized inputs |
| Trigger evaluation | Apply metric scope, thresholds, and three-valued expressions |
| Configuration compilation | Build the desired global/SMS properties |
| Delivery state | Track pending versus acknowledged configuration and retry incomplete delivery |
| Inspection/history | Expose the actual evaluated values, decisions, guard state, and delivery outcomes |

A calculator must not independently contact an exchange. A selected setting is not a confirmed PT update until delivery succeeds. Display and history must preserve that distinction.

### 3.2 Normalized inputs

The current base source is five-minute OHLCV:

- Symbol and interval.
- Open/close time in UTC.
- Open, high, low, close.
- Base volume and quote volume.
- Trade count where retained.
- Whether the observation is closed.

Reject malformed OHLC geometry, nonpositive/nonfinite prices, negative/nonfinite volumes, inconsistent timestamps, and invalid intervals. Derived calculations use closed observations and exact declared endpoints.

Current ticker snapshots remain useful for current price and 24-hour volume conditions. Their fields must not be confused with the historical quote-volume series used in trend-sized metrics.

### 3.3 Determinism and validity

Given the same normalized observations, analytical timestamp, population, and configuration, a calculator must produce the same result.

Every usable feature carries sufficient metadata to explain:

- Value and unit.
- Calculation/as-of timestamp.
- Source endpoint.
- Sample count.
- Eligible count and coverage where applicable.
- Valid/stale/unavailable state.
- A meaningful invalidity reason.

Do not fill missing values with zero, silently shorten a lookback, align sparse arrays by index, or use a nearby endpoint as if it were exact.

### 3.4 Scope and exchange applicability

The normalized application paths support Binance Futures, Binance Spot, and Binance US. Later derivatives families apply only to exchange/product scopes that actually expose the required observations. “Not applicable to this product” is a metric-family condition, not a reason to revive removed application exchanges.

Before adding any endpoint, verify its current official contract: availability, symbol and contract scope, units, history limits, interval choices, request weights, timestamps, and response semantics. Conceptual feature names in this roadmap are PTMagic concepts, not claims that an exchange exposes an API called MarketBreadth or CrowdingScore.

## 4. Universe and population contracts

Market-wide values are interpretable only with an explicit denominator.

The application resolves exchange-qualified symbols, quote currency, relevant contract/underlying metadata, configured inclusion/exclusion, and optional PT enabled-pair/type policies. It then freezes per-trend populations.

Preserve these distinctions:

- Exchange source population: series potentially acquired.
- Analyzer-eligible population: symbols allowed by the analyzer policy.
- Global MarketTrend population: ranked/filtered set with its MaxMarkets limit.
- Asset MarketTrend population: eligible per-asset observations, not automatically reduced to the global MaxMarkets cap.
- Valid sample population: members with the required usable data.

Missing data does not remove a member from the eligible denominator. General cross-sectional readiness is at least ceil(0.90 × eligible count), with a nonempty population. Return Concentration and the complete-volume share/concentration families require their specified 100% population.

Underlying categories come from authoritative exchange metadata where available. Do not infer types from symbol spelling or import a personal strategy's universe as a universal application default.

### PriceTrend exceptions that are deliberate

- TrendThreshold affects only arithmetic PriceTrend means.
- Global PriceTrend uses the global population.
- SMS Relative PriceTrend uses a separately calculated uncapped asset-population mean.
- Other distribution/volume measurements preserve their full selected populations.
- RelativeStrengthMarket compares against the market median under its own metric definition.

These differences are explicit semantics, not accidental population drift.

## 5. Timeframe, acquisition, and history contracts

### 5.1 TrendMinutes defines analytical duration

Five-minute candles are the input resolution. A one-hour trend does not secretly use five-minute ATR or correlation.

Exchange TrendMinutes must be positive and divisible by five. Do not round unsupported horizons silently.

Different metrics have explicit endpoint contracts:

| Family | Endpoint/window contract |
|---|---|
| Price returns and relative returns | Exact horizon ending at the latest closed normalized five-minute endpoint at the raid's pinned time |
| Return Concentration | Return horizon above; ranking quote volume covers the same TrendMinutes window and endpoint |
| ATRP and quote-volume period metrics | Complete UTC-aligned TrendMinutes bars |
| Correlation | N synchronized returns between exact complete UTC-aligned TrendMinutes endpoints |
| Future native observations such as funding or spread | Native observation timestamp/cadence retained; any rolling derived horizon is explicitly tied to the configured trend and supported source resolution |

Source cadence, analytical duration, and lookback count must not be conflated.

### 5.2 One pinned boundary

Pin the analytical UTC timestamp before normalized refresh. Carry that boundary into request windows and evaluation. A long refresh may cross a new candle close; later symbols must still preserve the history required by the same pinned decision.

The latest available exchange candle is not automatically the correct endpoint for a raid that began earlier. Preserve both the required latest endpoint and earliest reference/vector observations under tight StoreDataMaxHours retention.

The specific November 5 Futures boundary fix remains accepted for its tested case. The November 7 pinned-request extension addresses the additional tight-retention case and requires its own regression and runtime evidence.

### 5.3 Decision age

Application.MaxAnalysisAgeSeconds defaults to 300 and accepts 1–86400 seconds.

Compare actual decision time with the raid's pinned time. Missing, future, or expired analysis timestamps prevent publication of a new normal configuration. This is independent of whether the historical metric was internally valid at its as-of time.

Every normal configuration requires a completed raid analysis and a fresh runtime pin, including configurations whose conditions use only volume, age, or time. Omitting Exchange MarketTrends does not bypass freshness or startup-release requirements.

Do not reject a complete four-hour/daily metric merely because its own latest bar closed more than five minutes ago. The decision-age limit measures the delay in producing/using the raid, not a universal bar-age limit.

### 5.4 Required history

History requirements are derived from selected metrics and their dependencies. Do not automatically enlarge StoreDataMaxHours or silently reduce sample counts.

| Feature | Required complete observations |
|---|---|
| PriceTrend and return dependencies | Exact current and TrendMinutes-earlier endpoints |
| ATR(P) | P+1 complete trend bars, default 15 |
| VolumeExpansion(N) | One current completed bar plus N earlier completed bars, default 21 |
| Latest-period volume shares | One complete trend bar for every required eligible market |
| Correlation(N) | N returns from N+1 exact trend-duration endpoints, with complete required five-minute observations |
| Return Concentration ranking | Complete TrendMinutes quote-volume window for the full ranking population |

For current defaults:

| Trend duration | ATR(14) complete-bar span | VolumeExpansion(20) complete-bar span |
|---|---:|---:|
| 1 hour | 15 hours | 21 hours |
| 4 hours | 60 hours | 84 hours |
| 8 hours | 120 hours | 168 hours |
| 24 hours | 360 hours / 15 days | 504 hours / 21 days |

These are mathematical complete-bar spans, not guaranteed sufficient retention at every wall-clock alignment. The current incomplete trend period and boundary/reference slots also matter. Use the application requirement report for the actual selected configuration.

The exported HistoryRequirements report includes minimum complete-source retention, required stored slots for the current raid (including the forming source candle and partial UTC trend period), minimum current-raid StoreDataMaxHours, conservative all-alignments retention, configured store capacity, and explicit sufficiency/warning fields. Capacity matches the store's ceiling(hours / source interval) + 2 rule.

For 24-hour trends, the default parameters require conservative StoreDataMaxHours of 384 hours for ATR(14), 528 hours for VolumeExpansion(20), and 744 hours for Correlation(30). Correlation needs thirty daily returns plus the preceding reference close, with complete underlying observations. The report separates these requirements from the raw complete-period lower bounds.

Insufficient retention leaves affected metrics unavailable with an explicit reason; it does not itself reject the whole configuration or resize the store. Unrelated metrics with sufficient history can remain valid. A 96-hour store cannot supply the default eight-hour ATR/expansion histories; that condition must remain visible instead of appearing as a valid zero.

## 6. Current metric catalogue

The current source checkpoint contains the original nineteen canonical metrics plus three Phase 1D correlation metrics. Metric names are selected inside a named MarketTrend; do not create hardcoded metric names such as Breadth4h to replace the trend reference.

| Metric | Scope | Meaning / unit |
|---|---|---|
| PriceTrend | Asset and global | Asset return or configured arithmetic mean; percent |
| MedianPriceTrend | Global | Median eligible valid return; percent |
| MeanMedianSpread | Global | Unfiltered arithmetic mean minus median; percentage points |
| Breadth | Global | Percentage of valid returns strictly above zero, subject to eligible coverage |
| Dispersion | Global | Population standard deviation of returns; percentage-point scale |
| RelativeStrengthMarket | Asset | Asset return minus global median return; percentage points |
| RelativeStrengthBTC | Asset | Asset return minus aligned BTC benchmark return; percentage points |
| Concentration | Global | Mean return of Top10 by volume minus mean return of remaining eligible markets; percentage points |
| ATRP | Asset | Wilder ATR / latest complete trend-bar close ×100; percent |
| MedianATRP | Global | Median valid ATRP; percent |
| VolatilityBreadth | Global | Percentage above configured ATRP breadth threshold |
| VolumeExpansion | Asset | Latest complete trend-period quote volume / mean of prior N complete periods; ratio |
| MedianVolumeExpansion | Global | Median volume-expansion ratio |
| VolumeExpansionBreadth | Global | Percentage above configured expansion threshold |
| StrongVolumeExpansionBreadth | Global | Percentage above the strong-expansion threshold |
| VolumeConcentration | Global | Sum of squared eligible volume shares ×100; HHI index |
| TopNVolumeShare | Global | Combined volume share of configured TopN; percent |
| BTCVolumeShare | Global | BTC share of complete eligible period volume; percent |
| BTCETHVolumeShare | Global | Combined BTC and ETH share; percent |
| CorrelationToBTC | Asset | Pearson correlation of synchronized simple returns; unitless [-1,+1] |
| MeanCorrelationToBTC | Global | Arithmetic mean of eligible valid BTC correlations; unitless |
| MedianCorrelationToBTC | Global | Median of eligible valid BTC correlations; unitless |

Asset-only metrics cannot produce valid GlobalSetting measurements. An unavailable or disabled metric remains unavailable in the trigger layer, with diagnostics. Display units must preserve coefficient versus ratio versus percentage versus index meaning.

### 6.1 Return concentration correction

The November 7 change preserves the Top10-versus-remaining-market return calculation but replaces the fixed 24-hour volume-ranking window with TrendMinutes, ending at the same normalized endpoint as the returns.

At least eleven markets are needed to form a complete Top10 and a nonempty remainder. Preserve deterministic tie handling and full ranking/return coverage. This can change values on non-24-hour trends; revalidate thresholds used in neutral application fixtures. It is not the same metric as volume HHI.

### 6.2 Phase 1C formulas

For each complete trend bar, true range is the maximum of high-low, absolute high-previous-close, and absolute low-previous-close. ATR uses the accepted initial mean of P true ranges followed by Wilder smoothing. ATRP divides by the latest complete trend-bar close.

VolumeExpansion compares the latest complete period to the arithmetic mean of the preceding N complete quote-volume periods. A zero or invalid baseline is unavailable. Partial periods are not included.

Volume concentration/share calculations require a positive finite total and the complete selected volume population. Required BTC/ETH symbols absent from that eligible population cannot be invented or counted as zero.

### 6.3 Phase 1D statistical contract

MarketTrend.CorrelationLookback defaults to 30, with valid range 3–1000.

For each asset and BTC benchmark:

1. Select the same N+1 complete UTC trend-duration endpoints.
2. Require complete normalized source observations across the declared vector.
3. Calculate N simple returns.
4. Calculate Pearson correlation over those exact paired vectors.
5. Reject missing, mismatched, stale, nonfinite, insufficient, or zero-variance input.
6. Publish a coefficient in [-1,+1], never a percentage.

BTC self-correlation is +1 only for a valid nonconstant return vector. Global mean/median correlation uses the exact global population and the 90% gate. BTC contributes only if selected in that population; do not silently remove it from the denominator.

Full pairwise correlation remains optional and unimplemented. Its value and O(M² × N) cost require a separate scope decision. Performance optimization is not part of the current Phase 1D work under D-032.

## 7. Configuration selection and expression semantics

### 7.1 Selection and publication

MarketTrend.Metrics is a comma-separated canonical metric list:

- Blank/omitted enables normalized PriceTrend.
- Nonempty explicitly selects published metrics.
- Omitted Trigger.Metric or OffTrigger.Metric requests normalized PriceTrend through dependency resolution.
- An explicitly named metric must be enabled on the referenced trend.
- Internal dependencies do not force every related metric to appear as a published output.

The old parallel legacy PriceTrend architecture is superseded. CoinMarketCap and removed exchange paths must not be restored to satisfy obsolete handoff language.

### 7.2 Thresholds and three-valued logic

Preserve the production threshold contract and explicit metric units. For the normalized trend conditions, the lower threshold is inclusive and the upper threshold is exclusive.

Use true, false, and unavailable:

| Expression | Result |
|---|---|
| true OR unavailable | true |
| false OR unavailable | unavailable |
| false AND unavailable | false |
| true AND unavailable | unavailable |
| NOT unavailable | unavailable |

A final unavailable expression cannot freshly activate a setting or deactivate an SMS. A conclusive independent match can still be selected under the accepted ordered-setting behavior. An unavailable input is not by itself proof that every branch is unusable.

Validate missing trend references, identity ambiguity, duplicate/unusable expression tags, and invalid custom expressions consistently. Do not turn a missing reference into false or omit it from an AND list.

The current validator rejects missing trend references; blank or duplicate case-insensitive trend/setting names; duplicate nonblank tags; undeclared expression tags; malformed Boolean expressions; OffTriggerConnection other than AND/OR; and invalid ranges for active metric parameters. Unknown, disabled, and wrong-scope metric references remain accepted for deliberate diagnostic use, with warnings and unavailable runtime values. They do not become structurally valid market observations.

### 7.3 SMS persistence and removal

Active long-term SMS follow their documented OffTrigger/refresh rules. The evaluated SMS set is a configuration state, including the empty set.

An already active ordinary SMS is also retained when its activation expression becomes unavailable. Unavailable final SMS activation or OffTrigger expressions keep initial selection indeterminate. Missing/sentinel/future age or activation timestamps and nonfinite/negative volume values are unavailable; they cannot prove that an SMS should activate or end.

When the last applied SMS ends, the next desired PT payload must remove its overrides even if the global preset is unchanged. The system must remember pending versus confirmed application, so failure to deliver that clean payload does not disappear at raid cleanup.

Immediate off-and-reactivation can be legitimate if activation remains true. That observation does not prove lasting removal. Test persistent deactivation with activation deliberately false.

## 8. Startup protection and delivery lifecycle

### 8.1 Startup global SOM through the PT API

Application.StartupSellOnlyMode defaults to true.

Before lengthy exchange bootstrap, use `POST /api/v2/globalSellOnlyMode` with the configured API token and query parameter `enabled=true`. The user's API direction supersedes the initial unpublished preset overlay. This control request contains no PAIRS, DCA, or INDICATORS payload and does not change the local preset files or explicit pair SOM values.

Resolve the endpoint beneath each configured PT Monitor URL, preserving an installation's path prefix. Use Application.ProfitTrailerServerAPIToken for the primary target. Application.ProfitTrailerServerAPITokenXtra defaults to empty, explicitly sharing the primary token with additional targets; a nonempty comma-separated value must align with the additional PT Monitor URLs. Do not hardcode instance addresses or expose query credentials in logs/history.

The user clarified the endpoint's native behavior: global SOM stops new buys and DCA buys while allowing sells. The startup guard changes this global flag without rewriting the existing property sets.

Guard acquisition must be acknowledged before reporting that protection was established. If acquisition fails, abort the raid before slow bootstrap and retry at the next interval.

Release is a separate API operation, ordered after normal configuration delivery:

1. The raid's analysis is complete and fresh.
2. Selection is conclusive under the accepted expression semantics.
3. The required global/SMS configuration has been fully computed.
4. PT acknowledges the normal configuration while the guard remains enabled.
5. The startup lifecycle requests `enabled=false` and obtains its release acknowledgement separately.

Indeterminate/stale evaluation and failed normal delivery do not authorize release. A release failure remains visible and retryable on a fresh conclusive raid; it does not erase the acknowledged normal configuration. Enable outcomes, pending release, and confirmed configuration are separate facts. Guard metadata is stored in `_data/StartupSellOnlyModeState.json`, independently of `_data/ConfigurationDeliveryState.json`, without secrets or raw properties.

Save pending intent before enabled=true; an intent-write failure prevents that command and the slow bootstrap. A checkpoint failure after a real command acknowledgement is reported as a persistence failure without reversing the acknowledged result. StartupSellOnlyModeActive, StartupSellOnlyModePending, and StartupSellOnlyModeStatus expose these distinctions in Summary, Monitor, and decision history independently of normal configuration delivery.

Acknowledgement comes from the setter response, not a later readback. Partial failure or timeout leaves remote state uncertain; reassert the owned guard before the next load and retry release only after another fresh conclusive decision. One target's success does not prove success for every configured target.

Enabling StartupSellOnlyMode assigns the global SOM flag to PTMagic during startup. The implementation uses the supplied setter API and does not read or restore the prior global flag. A pre-existing global SOM=true therefore does not prevent the later requested false after the release conditions are met. This ownership rule is explicit in [D-037](../DECISIONS.md#d-037--direct-global-som-api-supersedes-the-startup-preset-overlay).

TestMode simulates the lifecycle without SOM API calls or configuration writes and without changing either live acknowledgement checkpoint. StartupSellOnlyMode=false prevents acquisition of a new guard and does not clear an untracked existing global SOM flag. A matching checkpoint with pending PTM-owned work still resumes recovery and eventual release, even after opt-out. An indeterminate startup must not invent DEFAULT as the previously applied state: preserve a known confirmed configuration or defer a new normal publication while the prior configuration is unknown.

The user's native-behavior clarification defines the intended buying/selling contract; the new client and lifecycle still require configured PT verification before execution acceptance is claimed.

### 8.2 Confirmed application

Keep desired selection, pending delivery, and confirmed application distinct.

A failed HTTP request, rejected configuration, or exhausted timeout does not advance the confirmed state. Retry pending delivery on later raids even when the desired setting has not changed. Stop retrying an acknowledged unchanged payload unless a legitimate reapplication is requested.

Compile from the current setting definition and preset contents on each raid, including same-name configuration reloads. After a partial multi-target failure, replay is still required if the desired configuration returns to an earlier confirmed payload; the earlier hash does not prove every target has that state.

Persist the confirmed checkpoint at:

`_data/ConfigurationDeliveryState.json`

The checkpoint contains configuration identity and payload hash, not raw properties or secrets. TestMode does not overwrite it. Recovery from absent, invalid, or stale checkpoint metadata must be explicit; never present guessed state as confirmed application.

Logs and Monitor summaries distinguish selected, pending, acknowledged, reapplied, guarded, failed, and simulated outcomes. A property-compilation flag is insufficient evidence that PT changed.

## 9. Monitor contract

The dedicated Market Metrics page renders exported results. It should not independently recompute financial metrics with a different population or timestamp.

The analyzer editor must preserve configuration meaning:

- Multiple Metric/Tag rows referencing the same MarketTrend remain distinct.
- GlobalSetting, SMS activation, and SMS OffTrigger rows retain full metadata.
- Numeric thresholds survive a no-edit save without display rounding altering the saved value.
- Newly added rows have unambiguous identity.
- Removing one row does not mutate another.
- Structurally invalid references or expressions are surfaced before publication.
- Coefficients, ratios, percentages, and indices are labeled correctly.

The implemented editor uses a detached ordered-row transformer, original row indices, unique new-row IDs, and a SHA256 revision check. A stale form must not silently overwrite a changed source configuration. Interleaved trigger types and fields omitted from a form remain intact. Explicit Boolean fields, native property values, and invariant number formatting prevent a no-edit save from changing meaning.

ManageSMS reads and resets the mode-specific summary: SingleMarketSettingSummary.TestMode.json in TestMode and SingleMarketSettingSummary.json for live state. A reset request submitted after the mode changes is rejected. LastRuntimeSummary remains the latest runtime inspection export, including failed/pre-bootstrap status; it is not the confirmed-delivery checkpoint.

General Settings exposes the startup global SOM option and additional-target API tokens. The UI explains that global SOM blocks new and DCA buys while allowing sells and that the enabled option assigns the global flag to PTM for startup. Saving credentials must not expose them in logs or history.

Original Market Analyzer graph/column continuity still needs specific browser acceptance. Adding more optional columns remains Phase 1E work; it does not justify claiming that every older UI already supports every metric.

## 10. Decision history and provenance

### 10.1 Implemented minimum

The current checkpoint brings a limited part of Phase 6 forward.

| Application setting | Default |
|---|---:|
| DecisionHistoryEnabled | true |
| DecisionHistoryRetentionDays | 30 |
| DecisionHistoryMaxMegabytes | 256 |

Retention accepts 1–3650 days and the total quota accepts 16–102400 MiB. The append writer rejects an individual record larger than a segment rather than breaking the storage bound.

Append JSONL segments at:

`_data/DecisionHistory/YYYY-MM-DD-NNNNNN.jsonl`

Rotate segments at 16 MiB and prune complete oldest files by configured age and total quota.

Records preserve safe evidence about:

- Source/version and schema identity.
- Configuration and desired/confirmed payload hashes.
- Analytical as-of and decision timestamps.
- Population/metric inputs relevant to evaluated decisions and their validity.
- Global/SMS selection and startup guard.
- Pending, successful, failed, or simulated delivery.
- Safe error categories for failed/pre-bootstrap raids when services are ready.

The desired/confirmed payload hashes identify compiled output from the selected presets and SMS overrides. They are not a separate inventory of every source preset file.

Do not record license values, tokens, raw general settings, raw PT payloads, or raw exception strings containing sensitive request data.

### 10.2 Evidence limits

This audit trail is not a full normalized candle cache, a complete historical feature database, or a trading backtest. Reproducing a calculation may still require the relevant normalized source observations and configuration version.

Source identity must describe the actual build where available. An unembedded or unavailable identifier is recorded as unknown; the checked-out branch is not automatically the identity of a running binary.

The current build embeds the source revision and appends -dirty when the checkout has uncommitted changes. Record that actual identity instead of labeling it as a clean commit.

The confirmed-delivery checkpoint and decision-history audit trail have different purposes. A history append is not a delivery acknowledgement.

## 11. Phase 2 — Futures raw observations

**Status: planned.** Begin after current source acceptance; do not start a separate performance program first.

For each endpoint family, define:

- Applicable exchange, product, and symbol universe.
- Native unit and transformation rules.
- Exact observation timestamp and publication/settlement delay.
- Supported history horizon and sampling interval.
- Refresh, timeout, cancellation, retry, and rate-limit policy.
- Retention and staleness.
- Availability/coverage metadata.
- A deterministic mapper and numerical fixtures.
- A clear feature-enable/dependency switch.

Verify current official Binance endpoint documentation before coding. The labels below describe required data, not preapproved network method names.

### 11.1 Open interest

Retain current and historical OI in its native documented units. Preserve distinctions between contract counts, base-asset amounts, and quote-notional values.

Derived OI change over an exactly aligned supported trend horizon:

(OI_end / OI_start - 1) ×100.

Require a positive valid reference and aligned observations. Do not silently compare different contract units or aggregate raw quantities across unrelated assets.

Keep raw OI changes separate from interpretation. Price rising with OI rising, price rising with OI falling, and their downward counterparts are observed combinations; they are not automatic predictions.

### 11.2 Funding

Retain native rate, interval/settlement metadata, timestamp, and any explicitly defined normalized representation. Funding schedules can differ; normalization must not discard the raw observation.

Candidate per-asset features include current funding and deviation from a defined market reference. Market median, positive/negative breadth, and extreme-funding breadth belong in Phase 2B.

Positive funding alone is not a sufficient long-crowding conclusion; negative funding alone is not a sufficient short-crowding conclusion.

### 11.3 Account and position ratios

Keep global account long/short ratio, top-trader account ratio, and top-trader position ratio distinct. Account counts and position sizes measure different things.

Where native fields permit a long-share transformation, retain both the raw ratio and the transparent transformation. Do not fabricate history for products or symbols the provider does not cover.

### 11.4 Taker flow

Retain buy and sell flow with units and matching intervals. Derived examples:

- TakerBuyRatio = buy / (buy + sell), range [0,1].
- TakerImbalance = (buy - sell) / (buy + sell), range [-1,+1].

A zero/invalid denominator is unavailable. Reuse adequate already-ingested source fields when supported rather than inventing additional endpoint dependencies.

Change and persistence measures can be added once the underlying series is validated.

## 12. Phase 2B — Futures market aggregates

Aggregate only after per-asset measurements have a verified contract.

Planned families include:

| Family | Candidate aggregate measurements |
|---|---|
| OI | Median change, expansion breadth, contraction breadth, extreme expansion/contraction breadth |
| Funding | Median rate, positive/negative breadth, extreme positive/negative breadth |
| Positioning | Median account/position ratios and explicitly defined concentration/breadth measures |
| Taker flow | Median buy ratio, buy-dominance breadth, strong-dominance breadth, imbalance distribution |

Use explicit eligible and valid populations. A ratio available for fewer symbols must not silently change the market universe relative to another metric.

Decide equal weighting versus a meaningful normalized notional weighting separately for each aggregate. Raw cross-asset OI sums are not comparable until their units are reconciled. Preserve numerator, denominator, sample coverage, and freshness in outputs.

Do not apply the current 90% policy blindly to a newly defined measure whose mathematical meaning requires complete data; record any stricter requirement.

## 13. Phase 3 — Transparent higher-order conditions

Build these only from validated inputs. Expose components and validity rather than beginning with opaque scores.

Planned concepts:

- Leverage expansion: a declared combination of OI, participation, and volatility changes.
- Long crowding: funding, OI, and distinct positioning inputs.
- Short crowding: the corresponding measured conditions on the other side.
- Deleveraging: explicit OI contraction with participation/volatility context, with price direction recorded separately.
- Flow confirmation/divergence: transparent combinations of price, taker flow, OI, and quote-volume behavior.

Choose Boolean components, labeled states, or a transparent score only after defining units, ranges, thresholds, weights, and missing-input behavior. If a score is adopted, every component and weight must be configurable or fixed in a documented versioned contract, and inspectable in diagnostics.

Do not label all OI contraction as liquidation or infer trader identity from public aggregate data. Preserve what was measured and what was derived.

## 14. Phase 4 — Metric integration as each family arrives

Phase 4 began early with the existing normalized trigger adapter and continues with every added family.

For each metric:

1. Register the canonical name, scope, unit, and enable/dependency behavior.
2. Add independent calculation and invalid-input fixtures.
3. Expose it in read-only exports and inspection.
4. Route it through GlobalSettings or SMS only where scope permits.
5. Exercise thresholds, three-valued combinations, and OffTrigger behavior.
6. Preserve Monitor load/save meaning.
7. Record provenance and delivery outcome in history.
8. Obtain the relevant configured runtime acceptance.

Avoid a second arbitrary expression language for each family. Keep metric availability separate from regime matching and configuration delivery.

A future metric cannot force new optional endpoints merely by being present in a registry. Dependencies follow enabled/configured uses.

## 15. Phase 5 — Liquidity, depth, and stress

**Status: planned after derivatives/higher-order metric work.** Endpoint cost and native sampling make this a deliberate separate stage, but the dedicated performance program remains after its approved metric additions.

### 15.1 Spread

Retain best bid/ask and observation timestamp. Define:

- Mid = (bid + ask) /2.
- SpreadPercent = (ask - bid) /mid ×100.

Reject nonpositive mid, crossed/invalid books according to an explicit policy, stale samples, and mismatched observation legs. Market median spread and wide-spread breadth need declared coverage and thresholds.

### 15.2 Depth and imbalance

Measure bid and ask depth separately within configured basis-point bands, such as 10, 25, and 50 bps, with consistent notional units.

Depth imbalance can be defined as:

(bid depth - ask depth) / (bid depth + ask depth).

Keep the chosen band, unit, sample time, and denominator. A zero/invalid total remains unavailable. Do not treat imbalance alone as validated directional information.

### 15.3 Slippage estimates

Estimate execution cost for declared configurable notionals by walking the observed book. Record side, notional, consumed depth, completion status, timestamp, and estimated slippage.

Do not present an estimate from insufficient or stale depth as an executable quote.

### 15.4 Stress components

Expose widening spreads, falling depth, high volatility, OI contraction, funding extremes, and taker-flow imbalance as separate measured components before introducing a combined stress state.

Sampling must match the supported observation cadence. Do not pretend an instantaneous book snapshot has the same temporal meaning as a full trend-period aggregate.

## 16. Phase 6 — Historical analysis beyond the initial audit trail

The November 7 JSONL history establishes a minimal inspectable decision record. Full historical analysis remains planned.

Future work includes:

- A versioned feature-history schema with exact universes and source timestamps.
- Sufficient source/configuration provenance for independent reproduction.
- Consistent handling of new listings, delistings, missing history, and later source revisions.
- Chronological replay with correct observation availability and no future leakage.
- Explicit comparison of selected, pending, and applied states over time.
- Queries and export tools appropriate to the volume of accumulated data.
- Independent numerical reference comparisons.
- Optional application-level linkage to external outcome data through a declared interface.

Choose SQLite or another storage/query design only when requirements justify it. Do not represent the current single latest MarketTrendAnalytics.json export as durable time-series history, and do not describe the initial JSONL audit trail as a complete backtesting engine.

No personal strategy implementation is part of Phase 6.

## 17. Post-metric performance program — explicitly deferred

**Gate for the broader performance program: all approved new metric additions are complete, including derivatives, aggregation, higher-order conditions, and liquidity/depth.** The narrowly approved normalized-candle warm-start cache was implemented earlier under D-040.

This ordering is the November 7 user decision and supersedes earlier recommendations to optimize before correlation. Preserve required correctness and bounded storage during implementation; keep this separate optimization stage deferred.

### Backlog

- Audit and eliminate unnecessary legacy history reconstruction after verifying remaining consumers.
- Share/reuse immutable source snapshots within and across raids where safe.
- Avoid repeated full-series sorting, closed-candle array allocation, gap scans, and duplicate derived work.
- Consider stateful incremental ATR/return-vector processing with mathematically equivalent results.
- Revisit short-history/new-listing refresh behavior.
- Consider a durable warm-start normalized candle cache.
- Reduce irrelevant per-market DEBUG formatting/output while retaining all distinct warning groups.
- Review JSON, filesystem, allocation, GC, and Monitor serialization costs.
- Revisit network scheduling against all enabled endpoint families.
- Assess whether optional pairwise correlation or heavier depth analysis is worthwhile.

### Measurement contract

Measure cold startup, gap recovery, normal new-data raids, and unchanged idle raids separately.

Record:

- Source/configuration and enabled feature set.
- Exchange cache size, eligible analyzer size, global MaxMarkets size, and asset population.
- Retention and history requirements.
- Network requests/weights/wait time.
- Mapping, storage, calculation, delivery, and serialization time.
- CPU, allocations, GC, memory, disk, and log growth.
- Identical calculation/availability results before and after optimization.

A zero-request idle raid is not proof of zero historical calculation work. A fast cold run is not a steady-state CPU result. Do not claim a gain without measurement.

## 18. Validation program

### 18.1 Ownership and execution evidence

D-021 assigns builds, deterministic harness execution, and configured runtime checks to the user. The assistant implements, reviews, authors tests, and fixes failures. Automatic remote CI is not part of the default workflow.

D-022 requires complete fail-fast PowerShell with exact current projects in each verification handoff. The current command set is in the [November 7 handoff](../handoffs/2026-11-07-stabilization-correlation-validation.md).

Record build, deterministic, configured TestMode, actual PT application, and browser results separately. An authored fixture is not an executed result.

### 18.2 Required deterministic coverage

Maintain existing accepted calculation/helper regressions and add the actual orchestration paths:

| Area | Required behavior |
|---|---|
| Returns/distribution | Exact endpoints, positive/negative/zero cases, median/dispersion identities, threshold isolation, eligible coverage |
| Phase 1C | UTC aggregation, Wilder seed/recurrence, volume baseline, invalid geometry, gaps, insufficient retention, complete share populations |
| Correlation | +1/-1/controlled expected coefficient, self/zero variance, exact common vectors, missing endpoints/source candles, short history, coverage boundaries |
| Pinned boundaries | Early/late symbol requests across a close with tight retained capacity; exact required reference retained |
| Decision age | Fresh, expired, absent, and future pin; delayed raid cannot release startup guard |
| Global selection | Missing references, negation, independent conclusive branches, indeterminate retention |
| SMS lifecycle | Nonempty to empty, stable empty, off while activation false, off-and-reentry, failed removal delivery |
| Delivery | Failure then success without a new regime, acknowledged unchanged payload, forced reapply, confirmed checkpoint, no false success |
| Startup | Direct global SOM enable without property writes, explicit setter ownership, acquisition failure, stale/indeterminate first raid, configuration-before-release ordering, release retry, restart/opt-out behavior, TestMode isolation |
| Monitor | No-edit round-trip, repeated trend with distinct Metric/Tag, edit one row/remove one row, full precision, special SMS triggers |
| History | Safe fields, stable hashes, failure records, rotation, age/quota pruning, disabled mode, malformed-file handling |

Use production entry points or extracted production components. Do not write tests that merely reimplement the algorithm and compare it with itself.

### 18.3 Configured runtime matrix

The current acceptance must include:

- Binance Futures, Spot, and US paths where the user has a configured environment.
- USDT and at least one supported non-USDT Fiat conversion case.
- Warm, cold, cross-boundary, and deliberately incomplete history.
- Global SOM guard retained through indeterminate/stale data, with normal configuration acknowledged before a separately acknowledged eligible release; prior protection and release failures remain explicit.
- Persistent SMS deactivation without same-raid activation.
- Actual PT payload/readback for removal and delivery recovery, beyond TestMode simulation.
- Invalid timeframe/reference startup handling.
- Original Market Analyzer/graph continuity and the new editor/metrics behavior.
- Matching timestamps, units, coverage, setting identity, and delivery outcomes across logs, exports, history, and Monitor.

Use neutral application fixtures. Runtime observations should identify exact source/binary, exchange, quote, settings hash, TestMode state, and log interval. Do not include credentials in repository evidence.

### 18.4 Acceptance gates

A new metric family is accepted only when its contract, source, meaningful fixtures, execution results, exports/UI integration, and applicable runtime checks are accounted for. Unavailable external environments remain explicitly pending; do not infer cross-exchange acceptance from shared dispatch code.

A release candidate additionally needs documented migration/default changes, acknowledged-delivery behavior, restart recovery, consistent current documentation, supported packaging/runtime, and reproducible provenance.

## 19. Immediate handoff and subsequent order

1. Run and review the current application build and all relevant existing/new regression harnesses.
2. Correct any compilation or behavioral failures in this checkpoint.
3. Complete the lifecycle, startup, correlation, history, Monitor, and remaining migration runtime matrix.
4. Mark accepted scope precisely, preserving the earlier Phase 1A–1C baseline and the limits of each execution.
5. Begin Phase 2 raw derivatives data, then Phase 2B aggregates and Phase 3 conditions, extending Phase 4 integration throughout.
6. Complete Phase 5 liquidity/depth measurements.
7. Extend Phase 6 history/analysis according to the application requirements.
8. Start the dedicated performance program only after all approved new metric additions are complete.

Do not return to a historical handoff that instructs initial ATRP implementation or restoration of legacy PriceTrend. Do not import personal strategy work into application acceptance.

## 20. Source and document navigation

Current production areas:

- `Core/MarketAnalyzer/MarketData/`: normalized store, metric engines, validity, correlation, and trigger resolution.
- `Core/Main/PTMagic.cs`: raid orchestration, selection, SMS, startup guard, delivery/history integration.
- `Core/ProfitTrailer/`: property compilation and acknowledged normal configuration delivery.
- `Core/ProfitTrailer/GlobalSellOnlyModeAPI.cs`: direct global SOM setter, target/token mapping, and guarded command acknowledgement.
- `Core/ProfitTrailer/StartupSellOnlyModeState.cs`: separate pending/acknowledged startup guard metadata and restart recovery.
- `Monitor/Pages/`: inspection and configuration editing.
- `Tests/`: explicit console regression harnesses.
- `Core/DataObjects/PTMagicData.cs`: persisted/configured application and trend contracts.

Current documentation:

- [STATUS](../STATUS.md): present implementation/evidence matrix.
- [DECISIONS](../DECISIONS.md): accepted contracts and supersession.
- [Current handoff](../handoffs/2026-11-07-stabilization-correlation-validation.md): exact verification and next action.
- [Update index](../updates/README.md): dated evidence.
- [Historical roadmap index](README.md): preserved earlier plans.
- [Historical current documents](../history/README.md): pre-reconciliation snapshots.

This roadmap is maintained as current guidance. Preserve an earlier snapshot when a future change materially replaces its contract or ordering.
