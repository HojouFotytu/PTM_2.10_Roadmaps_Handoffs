# PTMagic 2.10 — Current Development Status

**Updated:** November 10, 2026

**Application branch:** `phase1/market-data-foundation`

**Current published and tested application source:** `fb94373d8928b681e3ebe1f7209bd1439db42e72`

**Latest deterministically tested application source:** `fb94373d8928b681e3ebe1f7209bd1439db42e72`

**Latest verified offline suite:** 16/16 harnesses, **337/337 groups** (two successful full runs)

**Current handoff:** [Startup SOM enable-only safety correction](handoffs/2026-11-10-som-enable-only.md)

This file describes the present state. Dated evidence stays in [updates](updates/README.md). The earlier append-heavy status is preserved in [history](history/2026-11-07-pre-reconciliation/STATUS.md). Accepted behavior is in [DECISIONS](DECISIONS.md); the complete plan is [roadmaps/CURRENT.md](roadmaps/CURRENT.md).

**November 10 — Market Trends positive color:** The existing Market Trends column displays its activation-time PriceTrend percentage when available. Positive values (>0%) are **green**, regardless of setting-trigger membership; nonpositive/unknown trends remain **white** if referenced by the selected setting, **gray** if unused. The Market Metrics gray/white/green trigger-color policy is unchanged. Monitor-only UI change published; the last reported 71/71 ConfigurationLifecycle PASS and solution build predate this color adjustment. Local build/browser verification of the new source is pending.

## November 10 — Dashboard zero-limit Possible Buys layout (pending build)

The Monitor dashboard now preserves the **Possible Buys (N)** heading (and its Buy Analyzer link) when `MaxDashboardBuyEntries=0`, displaying it as a compact full-width row **above** Positions. The buy table remains hidden and Positions receives the whole row. Any positive limit continues to render the original two side-by-side cards. Count is the actual `PTData.BuyLog.Count`, not the number of entries displayed. Only `Monitor/Pages/_get/DashboardTop.cshtml` and a focused `ConfigurationLifecycle` source regression assertion changed. No analyzer, PT, or SOM behavior changed.

**Acceptance:** GitHub source published on existing PTMagic `phase1/market-data-foundation`; local .NET build, the focused ConfigurationLifecycle test and browser checks for zero/nonzero limits are **not yet recorded**. Run `git pull --ff-only`, `dotnet build .\\PTMagic.sln` and `dotnet run --project .\\Tests\\ConfigurationLifecycle\\ConfigurationLifecycle.csproj` from the existing clone.

## November 10 — Compact Global Setting header tooltip (build pending)

The Monitor header's Global Setting `(i)` tooltip now shows only the instance name, full selected GlobalSetting name, `Delivered to PT` or `Not Delivered to PT`, and a conditional `Startup SOM` line. Delivery is positive only when the selected name matches the confirmed applied setting and the delivery status is Applied/Unchanged; otherwise the tooltip does not imply that the selected configuration reached PT. The SOM line depends on PTMagic's acknowledged startup-enable flag, **not a live read of ProfitTrailer's global SOM state**. Full diagnostic detail remains on Status Summary. A dedicated CSS class prevents name wrapping. No PT API or trading behavior changed.

**Source:** existing application `phase1/market-data-foundation` branch. One focused ConfigurationLifecycle source assertion was added. **New source has not yet been compiled or browser-validated locally.** Run `git pull --ff-only`, `dotnet build .\\PTMagic.sln`, and `dotnet run --project .\\Tests\\ConfigurationLifecycle\\ConfigurationLifecycle.csproj`; verify the compact tooltip visually.

## November 10 — Seven-column grouped Market-Wide Metrics display (build pending)

The Monitor **Market Metrics** page now groups the same **17 market-wide metrics** into **seven columns**, with bold group headings, vertically stacked individual metric labels, and values in matching order for each trend. Groups: Price Direction (3); Market Structure (3); Volatility (2); Volume Expansion (3); Volume Concentration (2); BTC / ETH Volume Share (2); BTC Correlation (2). Existing Trend, Timeframe, Markets, numeric formatting/colors, metric/availability tooltips and the Per-Market Metrics table are unchanged. A scoped CSS rule aligns headings/values and permits the existing horizontal table scroll when needed.

**Source review:** all 17 original metrics appear exactly once in the seven group definitions; both markup loops consume the same ordered definitions. This is Monitor presentation only; no metric calculations, trigger conditions, retention requirements, or PT/SOM behavior changed.

**Current acceptance:** published on the existing application `phase1/market-data-foundation` branch; no new .NET solution build or browser verification has yet been provided for the grouped-table change. Previous offline 337/337 and focused 71/71 results are earlier-source evidence and not automatic acceptance of this UI. Run `git pull --ff-only` then `dotnet build .\\PTMagic.sln`; visually inspect stacked labels/values across multiple MarketTrend rows and preserve metric tooltips.

## November 10 — Corrected Global Settings Log layout (pending local build)

**Owner-directed UI:** exactly two market-data columns, **Market Trends** and **Market Metrics**, following Activation Time / Setting / Active Time. The separate Activation Triggers column, expression, and TRUE/FALSE labels have been removed from the page. All configured MarketTrends are listed gray unless referenced by the selected setting (white). All configured metrics are listed gray unless referenced (white); a condition whose recorded trigger result is TRUE is **green**. Asset-only metric names are included without a fabricated global value. A selected setting's own recorded trigger set determines colors, not later analytics. No changes to trading logic, metric calculations, SOM, or provider acquisition. Historical entries lacking full metric snapshots cannot be reconstructed reliably.

**Implementation:** committed to the existing PTMagic `phase1/market-data-foundation` branch. **Validation:** newest change not yet locally compiled or browser-tested; the earlier full 337/337 PASS belongs to source `fb94373` before the UI correction. Focused command after `git pull --ff-only`: `dotnet build .\\PTMagic.sln` and `dotnet run --project .\\Tests\\ConfigurationLifecycle\\ConfigurationLifecycle.csproj`. Visually check two columns and white/gray/green logic.

## November 10 — SOM and Monitor validation accepted (latest evidence)

**Exact verified application source:** `fb94373d8928b681e3ebe1f7209bd1439db42e72`. The user ran the existing full validation script twice: .NET SDK 10.0.403 solution builds **PASS** in 15.6s and 10.3s; **all 16 offline harnesses and 337/337 test groups PASS in both runs**. This includes 71 ConfigurationLifecycle checks (SOM enable-only, startup manual-release notice, new metric snapshots), 28 Monitor settings roundtrip checks and 13 DecisionHistory checks. The first build reported eight nonfatal pre-existing nullable test-source warnings; the second reported no warnings, consistent with incremental compilation. No live exchange, PT API or browser acceptance is claimed.

The Market Metrics History Requirements **UI panel** is removed; its diagnostic calculations remain active. Global Settings Log captures all available **market-wide** metrics across configured trends at entry creation and highlights a metric in white when referenced by any selected-setting trigger (even if FALSE/UNAVAILABLE); other metrics are gray. Existing history must not be fabricated from later snapshots. The red startup `PT: SOM` notice lasts only the first two raids; PTMagic never automatically requests global SOM OFF and the user releases it manually. **Do not rerun this completed offline suite as a prerequisite for new Phase 2 work.** Next development: distinct Futures global account, top-trader account and top-trader position long/short ratios. Configured runtime and Monitor browser verification remain separately open.

**Evidence:** [November 10 — 337-group offline validation](updates/2026-11-10-som-monitor-offline-validation.md).

## November 10 — Monitor metric audit and removed History Requirements UI (UNTESTED)

**Application source:** `f95ace1a0d8300cb63becf04e6a774439b505f71` on the existing `phase1/market-data-foundation` branch. The Market Metrics page **no longer displays** the History Requirements panel. Metrics calculation/readiness, OHLCV/OI/funding retention, warnings and diagnostic generation remain unchanged.

**Global Settings Log:** each new setting log entry now captures all configured market-wide metrics across all configured trends **at selection time**. Entries are gray by default; entries whose metric/trend participates in the selected setting's activation-trigger set are white, irrespective of whether the condition was TRUE, FALSE or UNAVAILABLE. Activation Triggers remains an independent condition/result audit. Asset-only metrics have no global aggregate to display; older historical records are never reconstructed from new data. Retained DEFAULT has no highlighted values if no evaluated trigger set selected it.

**Validation:** authored two new ConfigurationLifecycle assertions, but **no updated local .NET build, complete regression run, or browser validation has occurred**. The prior SOM safety regression testing is also pending. Run the existing full fail-fast validation script, inspect the Status Summary display for both matching and retained settings and check the Market Metrics page no longer contains the panel. Full-suite count must be taken from actual execution; do not treat the old 332/332 evidence as validation of this source.

## NEXT CHAT — verify SOM safety changes

Application source `891f709010c867259a6cde3df8e9c82781091b7f` (existing `phase1/market-data-foundation` branch) contains enable-only startup SOM, manual ProfitTrailer release, legacy release-checkpoint migration, and the red `PT: SOM` ticker plus raid-summary warnings on startup raids 1–2. **The source has NOT yet passed its new local .NET build or regression suite.** Last verified source `49f2aab66592b6e2922097ca5242b5a614090602` passed **332/332** before these changes.

**First action:** run/review `Tests/Phase2OpenInterestIncremental/Run-Phase2Validation.ps1`, fix any errors on the existing branch, and record actual test results with exact SHA. Never automatically issue global SOM `enabled=false`. Disappearing ticker after raid 2 is not proof of PT state and does not switch SOM off. After SOM validation, resume Phase 2 separate global account, top-trader account, and top-trader position long/short ratio metrics.

[Complete active new-chat handoff](handoffs/2026-11-10-som-enable-only.md). Only specified unfinished Phase 1 *configured integration* tests were deferred; normal source builds and regressions remain mandatory.

## November 10 — Startup global SOM made enable-only; two-raid manual-release warning

**Safety correction source:** `891f709010c867259a6cde3df8e9c82781091b7f`, existing PTMagic branch `phase1/market-data-foundation`. **Published, not yet build/regression verified.** The previous verified 332/332 offline tests were for source `49f2aab66592b6e2922097ca5242b5a614090602` before this change.

The startup SOM API in PTMagic is now **enable-only**. The application no longer issues global `enabled=false` after normal analysis or configuration delivery, nor from restart/legacy release checkpoints. When `StartupSellOnlyMode=true`, an initial startup may send `enabled=true` to ProfitTrailer before long data loading; the user must manually disable global SOM in ProfitTrailer when ready. Without an ownership-aware live state API PTMagic cannot establish whether SOM is presently on, so it must not claim live-state monitoring or automatic restoration.

The checkpoint is versioned to schema 2 with enable intent, acknowledgement, and manual-review metadata. Old pending-release checkpoints migrate into manual review, never an automatic `false` request. An unacknowledged enable blocks unsafe bootstrap rather than repeatedly overriding manual choices. Normal user-selected settings continue to be delivered after conclusive analysis independently of the global SOM flag. TestMode never sends a remote SOM command.

**User-visible notice:** on the **first two raids of each startup**, when PTMagic requested the SOM guard, the RAID SUMMARY logs a warning to manually release SOM in PT. The shared Monitor ticker row displays a **red `PT: SOM`** badge alongside Selected Global Setting, SMS and PT health, with an information tooltip explaining startup activation, continued block on new/DCA buys, and manual release. The ticker disappears after raid 2; it does not verify the live PT flag or secretly switch it off. The underlying manual-review status remains inspectable in Status Summary.

The new source-level Monitor ticker regression assertion is included in `ConfigurationLifecycle`. The exact code and all normal regression projects **still require a fresh .NET build and execution**; the 332 previous passing groups belong to the pre-SOM implementation. The user-visible warnings are scoped to the first two startup raids, not a real-time read of ProfitTrailer's SOM state.

**Mandatory verification:** updated `ConfigurationLifecycle` offline regressions cover no-auto-disable behavior, interrupted startup, restart, legacy checkpoint migration and first-two-raid notice. Execute the complete `Tests/Phase2OpenInterestIncremental/Run-Phase2Validation.ps1` .NET build and all offline harnesses. UI/browser rendering remains a separate acceptance step.

## November 10 — Funding and open-interest deterministic regression PASS

**Verified exact application source:** `49f2aab66592b6e2922097ca5242b5a614090602` · **.NET SDK 10.0.403** · solution build **11.0 seconds** · **16/16** offline harnesses, **332/332** test groups. All **17 funding tests**, **35 open-interest tests**, and **280 pre-existing regression groups** passed. Eight nonfatal nullable warnings remain in two older test harnesses. [Full source-attributed evidence](updates/2026-11-10-phase2-funding-offline-validation.md).

The current source includes an additional **Monitor Global Settings activation-trigger audit** change beyond the previous funding checkpoint. Core/PTMagic/Monitor compilation and 28/28 existing Monitor settings roundtrip checks passed, but the new Monitor screen has **not** been independently browser-tested.

**Acceptance:** Funding and OI **deterministic development tests PASS at this source**. Live Binance history, ordinary configured raids, remote PT API acceptance and user-interface/browser checks are not established by these offline results. The separate specific deferred Phase 1 integration cases remain open. Next Phase 2 code work: distinct account/position long-short ratios with mandatory new unit/regression tests.

## November 10 — Phase 2 funding-rate acquisition and normalization published

**Application implementation source:** `6430bab1afa262fadd4ae31199c11084508b28c7` (`phase1/market-data-foundation`).

Funding history is now an opt-in, Binance USD-M Futures-only data family using the documented `GET /fapi/v1/fundingRate` API, bounded ascending pages and the existing HTTP rate limiter. Each observation retains its native signed decimal `fundingRate`, `fundingTime`, `rateType` (Regular/Special/Unknown), and available `markPrice`; future `premiumIndex` funding estimates are not substituted for settled history.

The two new per-asset metrics are `FundingRate` (latest **Regular** settled rate in the selected MarketTrend) and `FundingSum` (sum of **Regular** settled rates across that MarketTrend). Their output is in **percentage points** (native decimal rate ×100), not annualized. Special funding from stock dividends is separate and not included; an unclassified type makes affected metrics unavailable rather than inventing zero or guessing Regular. Complete funding history must be retrieved before either metric is valid. An exhausted empty period yields a valid zero for the `FundingSum` only; absent regular settlements make `FundingRate` unavailable.

**Dynamic retention contract:** History begins at the longest funding-enabled Exchange MarketTrend's `TrendMinutes`, with no fixed 8-hour rate schedule or independent retention-hours setting. The `FundingMaxRequestsPerRaid` property controls acquisition only (default 60, allowed 0–400; 0 disables). Provider pages are limited to 1000 observations and two pages per selected symbol per raid; incomplete pages remain unavailable until pagination completes. Source is kept in a separate in-memory store and the existing metric/trigger/export/Monitor path is reused. No funding requests are made for configurations without funding metrics, or on Binance Spot/US.

**Verification:** 17 new offline funding case groups have been authored and added to the now **16-project** fail-fast development runner. **No .NET build or execution of these new funding tests has been performed.** The earlier **315/315** deterministic PASS at source `5f51faaa` belongs to the preceding OI-only code, not this new funding source. Separate Phase 1 configured integration testing remains deferred; normal Phase 2 builds and regressions remain mandatory under D-045. The next Phase 2 family is account/position long-short ratios; provider-specific fundingIntervalHours metadata, live funding API acceptance and configured live integration remain pending.

## November 10 — Phase 2 offline build and full regression suite PASS

**User-run acceptance evidence:** exact source `5f51faaa0db928cf33c52f6f93ca6f1b301735fb`, .NET SDK **10.0.403**, solution build **11.3 seconds** (Core, PTMagic, Monitor), followed by **15/15 offline harnesses and 315/315 test groups passing**. Phase 2 OI raw mapping passed **18/18** and incremental cache/metric integration passed **17/17**. The preceding `CS4008` test fixture error was corrected at this source. Older nullable-reference warnings remain nonfatal (two in Phase1SmsSummaryIsolation; six in NormalizedPriceTrendMigration).

**Status:** Phase 2 open-interest **deterministic development acceptance complete** at the exact tested source; configured live Binance data acquisition, native PT integration and Monitor/browser acceptance remain unverified. The specific outstanding Phase 1 integration scenarios remain deferred under D-042/D-045, **not** the Phase 2 offline tests. [Full 315-group evidence](updates/2026-11-10-phase2-oi-offline-validation.md).

## November 10 — Testing scope clarified (D-045)

The owner deferred only the specific remaining Phase 1 configured-runtime / PT API / Monitor-browser integration acceptance checks discussed before moving to Phase 2. Phase 2 compilation, deterministic feature tests and affected regressions were **never deferred**. New source must be built and relevant harnesses executed before marking a development batch validated.

**Result (November 10):** The required .NET build and all 15 offline harnesses subsequently passed at exact source `5f51faa` (315/315 groups). This section preserves the original testing-policy clarification; see the new result above. The fail-fast PowerShell runner is available at `Tests/Phase2OpenInterestIncremental/Run-Phase2Validation.ps1` in the application repository. The Phase 1 configured integration checks remain separately pending, not waived.

## November 10 — OI retention corrected to MarketTrend-derived history

**Correction source:** `0ae76f4c7886397a06ad346b42a375f6aa06be00` on `phase1/market-data-foundation`.

The previously introduced independent `OpenInterestRetentionHours=72` setting and hard 672-hour software horizon were incorrect and have been removed from the application, supplied analyzer templates, and calculations. For each configured `MarketTrend` that explicitly enables `OpenInterestChange` and/or `OpenInterestValueChange`, the requirement is its exact `TrendMinutes` plus the reference/overlap observation. The OI collector retains enough history for the **longest eligible OI-enabled MarketTrend**, and recalculates that requirement when the configuration changes; no fixed history duration or 72-hour default controls OI.

`OpenInterestMaxRequestsPerRaid` remains an independent **request budget**, not a history duration (default 60, 0 disables acquisition). The provider's roughly one-month historical data availability remains an external source limitation: if the requested horizon or exact observation is not obtainable, the metric remains **UNAVAILABLE** rather than being silently shortened. Requests, memory and disk cache storage remain bounded for safety, but their caps are not a substitute for user-specified analytical history requirements. OHLCV `StoreDataMaxHours` continues to govern the existing OHLCV store separately.

The Monitor History Requirements view now distinguishes OI-derived duration and provider availability from OHLCV retention; OI no longer displays misleading `0 h` retention/capacity sufficient labels. Offline regression cases were extended for dynamically selected horizons, greater-than-72-hour history, and per-source independence. **Superseded result:** the later November 10 full offline build and 315/315 checks passed at `5f51faa`. Other runtime/browser/actual PT acceptance remains deferred under D-042.

## November 10 — Phase 2 incremental open-interest integration

**Application checkpoint:** `b723f76664aa0de6b76de3f5ddf281c036c32275` (`phase1/market-data-foundation`). The second Phase 2 implementation batch now connects the optional Binance USD-M open-interest client to a per-symbol, independently bounded cache and the normal normalized MarketTrend metric pipeline.

**Selectable asset-scoped metrics:** `OpenInterestChange` measures the percentage change in the Binance-native historical `sumOpenInterest` field. `OpenInterestValueChange` measures the percentage change in the separately reported `sumOpenInterestValue` field. Both use exact five-minute historical endpoints over the configured `TrendMinutes`; missing, mismatched or unaligned samples remain unavailable. Do not interpret reported value as a reconstructed quote notional.

**Opt-in config:** `MarketTrend.Metrics` must explicitly list either metric. OI history is **automatically derived from the longest OI-enabled MarketTrend** and is independent of OHLCV `StoreDataMaxHours`. The former `OpenInterestRetentionHours` property has been removed. `MarketAnalyzer.OpenInterestMaxRequestsPerRaid` defaults to **60** (range **0–400**, zero disables OI acquisition). Every request is a bounded single page (maximum 500 rows); pages are retrieved serially with fairness across markets and up to two pages per symbol per raid. The existing shared Binance HTTP transport applies retry/rate limits. The OI disk cache is per-symbol, compressed/versioned, validates integrity and timestamps, and is not authoritative for unavailable metrics.

**Integration:** after frozen-universe selection but before normalized metric evaluation, the runtime refreshes only the OI-enabled Futures asset population, using the existing pinned raid timestamp. The metric registry, existing asset trigger resolver, exported `MarketTrendAnalytics.json`/Monitor snapshot and independent history requirements now recognize OI. Spot and Binance US never fetch Futures OI. Existing PriceTrend-only configurations make **zero new OI requests**.

**Validation status:** 15 additional incremental offline case groups were authored alongside the original 18 raw OI groups. Source review was performed, but **no .NET build or C# harness execution occurred** in this turn. Therefore compile and runtime acceptance remain **UNVERIFIED**. The owner's deferral of further runtime testing remains in force; it is not a claim that the new code has passed.

**Remaining Phase 2:** offline OI regression testing has passed; next implement and test funding, distinct account/position ratios, and taker-flow adapters, then Phase 2B aggregates. Live OI provider/runtime verification remains a separate pending gate. The full Phase 1 PT API/browser checks remain deferred.

## November 10 — Phase 2 started; further Phase 1 testing deferred

**Owner decision:** Resume market-analysis feature development now. Defer the remaining configured runtime, PT API, browser, Spot/US, non-USDT, and two-startup acceptance checks. Preserve existing evidence and open issues; do not convert untested items into PASS or require another Phase 1 validation run before continuing Phase 2.

**Source:** `314214b1a20bcddd1643b8fa8df032db5463b04d` on `phase1/market-data-foundation` publishes an optional Binance USD-M futures open-interest source foundation: raw current/history endpoint models, native quantity/value preservation, exact-time horizon change calculation, provider page bounds, and **18 authored offline test groups**. It is not yet integrated into normal analyzer raids or selectable MarketTrend metrics, and **no .NET build or tests of this new commit have been executed** in this turn. Next: implement bounded opt-in OI collection and application metric registration. [Phase 2 handoff](handoffs/2026-11-10-phase2-open-interest.md).

## November 9 — Reused configured TestMode acceptance evidence

The prior LONG and SHORT performance reports and their stored decision-audit CSVs were reviewed again, without a fresh configured run. The SHORT audit contains **358 TestMode decisions** (238 at `a0b375c`, 120 at `86c7d2b`), with **352 fresh**, **six deferred**, **zero recorded confirmed PT deliveries**, and **two consecutive fresh decisions** near the end of the November 9 capture. The latest SHORT snapshot previously reviewed has nine trends, 250/250 valid global markets, 717/717 asset markets, and sufficient 100-hour history. The present source `87b9eaa` differs from `86c7d2b` only in the changelog and three NLog console configurations; the analyzer/delivery engine is unchanged. These observations are **accepted for the tested engine's configured SHORT TestMode decision/no-delivery behavior**; they do not establish actual PT API action, paired raw RAID SUMMARY log lines, or browser acceptance.

The LONG review has 380 PTM TestMode decisions and 117 PTM non-TestMode decisions; 36 of the latter were applied. These must not be conflated with TestMode. Historical SHORT preset-file errors and transient locks remain separate reliability concerns. Do **not** request repetition of the recorded 358 SHORT TestMode decision cycles or 117 LONG delivery decisions as a prerequisite to accepting the evidence already available. Exact file/log identity, live PT API acknowledgements, Monitor editing, and configured restart comparison remain distinct pending gates. See [reused configured evidence](updates/2026-11-09-reused-configured-testmode-evidence.md).

## November 9 — Uniform TestMode console styling

Application source `87b9eaa1c865e39d8fff6a657e1b332012be8c16` adds the same `Magenta` NLog `ColoredConsole` highlighting condition for every case-insensitive `TestMode` message in `PTMagic/nlog.config`, `Monitor/nlog.config` and the packaged default PTMagic `nlog.config`. INFO/WARN levels and file output are unchanged. **User-local validation PASS (November 9):** `dotnet build` succeeded for Core (4.0s), PTMagic (0.7s) and Monitor (9.1s) in **15.1s** overall; all three logging config XML and `highlight-row` checks printed **PASS**. `git pull --ff-only` reported *Already up to date*. The command did not print the checked-out commit SHA. **Console color rendering and deployment to the live runtime remain unverified.** Existing installed `nlog.config` requires deployment or copying the new config into the correct runtime folder.

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

**November 10 override:** Phase 2 OI source development is next; the older validation instructions below are deferred and retained for eventual acceptance, not the present execution queue.


Collect the user-reported long run and its source/main-market/completion evidence. If another run is needed, use the explicit-DLL procedure in the [current verification handoff](handoffs/2026-11-07-stabilization-correlation-validation.md) with the existing runtime configuration. Native SOM and normal PT delivery require separate live acceptance because TestMode sends neither. The Monitor control is General Settings → APPLICATION → Startup Global SOM, immediately below Test Mode. Continue the applicable runtime/PT/browser checks before the remaining metric families in [the current technical roadmap](roadmaps/CURRENT.md).

Earlier files that instructed a restart of Phase 1C, preservation of a separate legacy PriceTrend path, use of the removed selective-legacy harness, or optimization before correlation are historical and superseded.
