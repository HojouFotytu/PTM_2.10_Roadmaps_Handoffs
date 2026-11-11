# PTMagic 2.10 — Current Technical Roadmap

**Current authority:** November 11, 2026

**Application:** [HojouFotytu/PTMagic](https://github.com/HojouFotytu/PTMagic), branch `phase1/market-data-foundation`

**Current inspected application branch head:** `66f88f73f46d5c7863ff27e55c00b98d6917cf83`

**Latest user-tested application source:** `875b4feb71104fbc609bd07dc3120405218d325f` (.NET 10 solution build PASS; **17/17 offline harnesses PASS**). Current branch head `66f88f73f46d5c7863ff27e55c00b98d6917cf83` contains two later reminder-document-only commits; application/runtime source is unchanged after the tested revision.

**Offline acceptance:** .NET 10 solution build PASS in 17.4s; **17/17 offline harnesses PASS** at the latest tested source. Eight nonfatal nullable warnings occurred in two existing test projects. Configured restart, live exchange/PT and browser acceptance remain separate.

**Documentation:** [STATUS](../STATUS.md) · [DECISIONS](../DECISIONS.md) · [current handoff](../handoffs/2026-11-10-som-enable-only.md)

This is the standalone current plan for PTMagic 2.10. It replaces the active guidance in the dated November 4 technical roadmaps while preserving those files as history. A reader does not need to reconstruct the old conversation to determine the current contract or next step.

Implementation and execution evidence are different states. The latest user-executed build and 17/17 offline harnesses passed at `875b4feb71104fbc609bd07dc3120405218d325f`. The two subsequent commits through `66f88f73f46d5c7863ff27e55c00b98d6917cf83` changed only `RANDOM_THOUGHTS_AND_REMINDERS.md`. Live Binance/PT, configured two-startup cache recovery and Monitor browser acceptance remain open; each result retains its actual source identity.

**November 10 — Market Trends positive color:** The existing Market Trends column displays its activation-time PriceTrend percentage when available. Positive values (>0%) are **green**, regardless of setting-trigger membership; nonpositive/unknown trends remain **white** if referenced by the selected setting, **gray** if unused. The Market Metrics gray/white/green trigger-color policy is unchanged. Monitor-only UI change published; the last reported 71/71 ConfigurationLifecycle PASS and solution build predate this color adjustment. Local build/browser verification of the new source is pending.

## November 11 — Derivatives persistence and latest offline validation

**Current branch head:** `66f88f73f46d5c7863ff27e55c00b98d6917cf83`. **Last user-tested application source:** `875b4feb71104fbc609bd07dc3120405218d325f`. The two later commits (`8d8873b`, `66f88f7`) changed only `RANDOM_THOUGHTS_AND_REMINDERS.md`; application/runtime source is unchanged since the tested revision.

At `875b4feb71104fbc609bd07dc3120405218d325f`, the user ran the .NET 10.0.403 solution build: Core, PTMagic and Monitor **PASS in 17.4 seconds**; **17/17 offline harnesses PASS**. New-family results: funding 18 groups, raw OI 18, incremental OI 17, and long/short ratios 29. Eight nonfatal nullable warnings came from the existing `Phase1SmsSummaryIsolation` and `NormalizedPriceTrendMigration` test projects. No build errors or failed harnesses.

### Persistent derivative caches

- OI: `_data/DerivativesOpenInterestCache` (existing).
- Funding: `_data/DerivativesFundingCache`.
- Ratios: `_data/DerivativesLongShortRatioCache`, partitioned by endpoint source and symbol.

Funding and ratio caches store versioned compressed raw observations and verified provider-query coverage intervals. They use temporary-file/atomic replacement, validate restored identity/timestamps/values and defensive limits, and discard corrupt files fail-open. Coverage does not fabricate observations or turn missing data into zero. Funding cache ordering preserves distinct Regular/Special settlements at the same timestamp.

### Remaining acceptance

Current tests directly verify cache save/restore, ratio source isolation and corruption recovery. They do **not** yet prove end-to-end restart through newly constructed `FuturesFundingDataService` and `FuturesLongShortRatioDataService` instances.

**Next task:** add service-level restart tests: persist through one service instance, construct a second instance against the same directory, and prove complete restored coverage avoids another provider request. Also verify partial coverage resumes only the missing range and corrupt-cache recovery triggers bounded reacquisition.

Then perform configured two-startup acceptance: verify cache restoration, reduced Binance request counts, and unchanged metric availability/values. Live Binance endpoint/API-key acceptance and Monitor browser rendering remain pending. Taker-flow development follows persistence acceptance; do not start another metric family before this is resolved.

## November 11 — Dashboard refresh investigation and current owner direction

**Current application branch:** `HojouFotytu/PTMagic`, `phase1/market-data-foundation`.  
**Inspected application branch head:** `731f4bd502e0daa508368c8e164f9cf4c0d7d33e`.  
**Dashboard rollback baseline:** `438acbe8e40241cd190e45385dffbee5637b3eb8`.  
**Last full offline acceptance:** `fb94373d8928b681e3ebe1f7209bd1439db42e72`, 16/16 harnesses and 337/337 groups PASS twice. That acceptance is earlier than subsequent Monitor edits and the dashboard rollback; it is not current DashboardTop runtime acceptance.

### Dashboard/PBL state — fully rolled back

The owner directed a complete rollback of every Possible Buys/dashboard layout and count experiment. Current source files were checked against the baseline Git blobs:

| File | Current blob | Baseline blob | Result |
| --- | --- | --- | --- |
| `Monitor/Pages/Index.cshtml` | `520f94d549a6b5d728f3688e1e82a93cc1add582` | same | Exact match |
| `Monitor/Pages/_get/DashboardTop.cshtml` | `914f18da75ec44213e061fb5613d7af276e79b44` | same | Exact match |
| `Core/DataObjects/ProfitTrailerData.cs` | `c725ddba129ad8013be9b07c4f876086d244b091` | same | Exact match |

The separate `PossibleBuysCount` endpoint and async count cache are absent; the experimental dashboard test was removed. The original `BuyLog` zero-limit short-circuit is restored. Therefore `MaxDashboardBuyEntries=0` again hides the entire Possible Buys card, and the PBL getter does not fetch a new PBL response in that mode. The requested compact count card above full-width Positions is **not implemented**; that experiment was withdrawn.

The original DashboardTop jQuery `.load()` method, tooltip cleanup/initialization, and `.text-autocolor(false)` post-load call are present. No new local build or browser verification has been supplied after the rollback.

### Refresh defect — still open after rollback

The owner reports that the top dashboard remains stale (reported as 12 minutes since its last update), including PBL/Positions data. Restoring the PBL-related files to their pre-experiment blobs did **not** restore observed refresh behavior. The PBL experiment was therefore not the only possible cause.

Git history identifies the November 2 refresh rewrite:

- `ec19a5eff1e2389c638b6cd71435a525fb99a8f2` — `Optimize dashboard AJAX polling`: replaced the previous interval-driven DashboardTop polling in `Monitor/Pages/Index.cshtml` with a request-running flag and a one-shot timer scheduled only from the `.load()` completion callback; added `document.hidden` gating.
- `26ce2d80a66e392d389fff11a07cfd9ad3dc3260` — `Preserve active dashboard tooltips during refresh`: inserted `cleanupOrphanedTooltips()`, tooltip initialization and profit autocoloring in the callback **before** clearing `dashboardTopRequestRunning` and scheduling the next request.

The current `Index.cshtml` is byte-identical to the November 2 post-tooltip version at `26ce2d8`. Ticker tooltip preservation was implemented separately in `Monitor/Pages/_Layout.cshtml` and `Monitor/Pages/_get/TickerWidgets.cshtml`; those ticker changes are not the same code path as DashboardTop polling.

**Source-level risks, not runtime-confirmed causes:**
1. The current `.load()` request has no explicit timeout; if it never completes, the callback never schedules another refresh.
2. The next refresh is scheduled only at the end of the completion callback.
3. Tooltip cleanup, tooltip initialization, and autocoloring run before the request-running flag is reset and the next refresh is scheduled. An exception in any of those operations can prevent subsequent polling.
4. The `document.hidden` guard pauses refresh while the browser tab is hidden and triggers an immediate request when the tab becomes visible.

No runtime log, failed HTTP response, or browser trace confirms which failure path is occurring. Do not state that the ticker tooltip fix itself caused the dashboard failure.

### Current owner requirements for the next implementation

- The data in **Possible Buys (PBL)** and **Positions** must refresh. The entire dashboard does not need to be re-rendered if a narrower update is sufficient.
- Preserve the existing DashboardTop jQuery `.load()` request and callback; the correction is limited to **refresh scheduling in `Monitor/Pages/Index.cshtml`**.
- Do not reintroduce the experimental PBL count endpoint, async count cache, or custom AJAX replacement. Do not change PBL/Positions data retrieval, calculations or DashboardTop rendering as part of the scheduling fix.
- Do not alter the separate ticker tooltip-preservation code as a side effect.
- Preserve existing PBL/Positions calculations and profit coloring.
- **Explain the exact proposed change, files, and scope before editing any files.** The owner specifically corrected the workflow after an attempted premature update.
- No implementation for this refresh correction has been agreed or committed. The current source remains the exact rollback state above.

**Dashboard follow-up:** review the November 2 callback-dependent polling path and propose a scheduling-only change in `Monitor/Pages/Index.cshtml`. Preserve the original `.load()` request and callback. Explain the exact change, affected files and scope before editing; wait for the owner's review. Keep PBL/Positions retrieval and rendering, DashboardBottom, ticker refresh, tooltip behavior and profit coloring unchanged.

**Analyzer development continues in parallel:** the three Futures long/short ratio feeds are implemented in source and wired into the raid pipeline. The next step is local build and focused verification, followed by live endpoint and Monitor checks.


## Phase 2 — Binance Futures long/short ratios and derivative persistence (implementation and offline suite passed)

The three opt-in asset metrics `GlobalLongShortAccountRatio`, `TopTraderLongShortAccountRatio`, and `TopTraderLongShortPositionRatio` are implemented. Global account participation, top-trader account counts and top-trader position-size participation remain distinct. All use exact 5-minute source observations over each MarketTrend's `TrendMinutes`; all expected timestamps are required and missing data remains UNAVAILABLE. The ratio window calculation averages implied long-side shares `r/(1+r)`, then converts the mean back to a ratio; neutral is 1.0. Top-trader endpoints require the optional read-only `BinanceFuturesApiKey`; no API secret is needed.

Funding and ratio histories now use persistent versioned compressed caches. Raw observations and verified coverage intervals are saved atomically; corrupt cache files are discarded fail-open. OI's existing disk cache remains unchanged. Cache paths and restart acceptance are documented above.

**Validation:** .NET 10 solution build PASS in 17.4s and all 17 offline harnesses PASS at `875b4feb71104fbc609bd07dc3120405218d325f`, including 29 ratio groups, 18 funding, 18 raw OI and 17 incremental OI groups. Eight nonfatal nullable warnings in two existing test projects.

**Outstanding:** service-level restart tests through newly constructed funding/ratio data services; configured two-startup request-reduction and unchanged-metric acceptance; live Binance/API-key and Monitor browser checks. Taker flow follows after persistence acceptance.

## November 11 — Latest Monitor formatting focused validation PASS

User-executed `.NET 10` solution build **PASS (15.7 seconds)** for Core, PTMagic and Monitor, with **75/75 ConfigurationLifecycle checks PASS** and no warnings/errors reported. Includes the latest Market-Wide Metrics page-local uppercase/gray/centering source check, plus PBL-count, compact ticker and SOM checks. `git pull` reported "Already up to date" but **the local run did not print a source SHA**. At documentation review the existing PTMagic branch head was `44dd757e29808eaa8662fbdf8a63835efb02378a`; do not treat this as a locally stamped test SHA. Previous unverified-build statements for this change are superseded by this evidence.

**Offline build and focused validation are complete.** Live Monitor browser appearance, actual ProfitTrailer PBL count agreement and external PT/Binance integration remain unverified. No need to repeat these focused tests absent relevant source changes. [Evidence](../updates/2026-11-11-monitor-market-wide-formatting-validation.md).

## November 10 — Market-Wide Metrics display correction (validation pending)

Corrected the reported left-aligned, white metric labels by adding **page-local, scoped rendering rules** in `Monitor/Pages/MarketMetrics.cshtml`. Seven group titles are now emitted **uppercase white**, metric subheadings are **muted gray**, and **all columns and stacked content are centered**. This avoids stale cached external `custom.css` overriding the new presentation. No analytics, Per-Market Metrics, or PT behavior changed. Extended one focused source regression check. Published on existing `phase1/market-data-foundation` branch; local solution build and browser verification are **pending** for this change. Prior **75/75 PASS** applies to earlier source.

## November 10 — Market Metrics and PT PBL focused validation PASS

The user's local `.NET` solution build passed for Core, PTMagic and Monitor (15.3 seconds); **ConfigurationLifecycle 75/75 PASS**, including the two new checks for centered/two-row Market-Wide Metrics headings and for retrieving PT's complete PBL even when `MaxDashboardBuyEntries=0`. No errors or warnings were reported. The `git pull` output showed "Already up to date" without a printed source SHA. At review the application branch head was `33c7a1ef80811677e5cc3559f561cfe773f31961`; do not claim this is an independently local-reported SHA.

The previous "build pending" statements for this batch are superseded by these passing results. **Browser layout verification and actual PT PBL count agreement remain unverified**; this was an offline source-level regression harness, not PT live API acceptance. Do not repeat these passed focused checks without another relevant code change. [Validation evidence](../updates/2026-11-10-monitor-pbl-metrics-75-validation.md).

## November 10 — Market Metrics header alignment and accurate PBL count (build pending)

**Market-Wide Metrics:** seven grouped columns now use a separate **upper heading row** for uppercase white group names and **lower heading row** for muted-gray individual metric names. Trend/Timeframe/Markets headings span both rows. Every header and value column is centered, including group stacks; the Per-Market Metrics table and analytics computations are unchanged. Source check added for header structure and styling.

**Dashboard Possible Buys:** identified and removed an early return in `ProfitTrailerData.BuyLog` that prevented the native PT `/api/v2/data/pbl` refresh whenever `MaxDashboardBuyEntries=0`. Now the heading always uses the full cached PT PBL count independent of `Take(MaxDashboardBuyEntries)`, while the list stays hidden at zero and Positions occupies the full width below. The existing cache interval still bounds PT requests. Source regression added; allowing PBL fetches with a zero display limit changes PT API traffic compared with the former early return.

**Validation:** changes committed to existing PTMagic `phase1/market-data-foundation`. No local build, focused tests, or browser verification has yet been supplied for the newest changes. Previous 73/73 focused PASS predates these changes. Run `git pull --ff-only`, `dotnet build .\\PTMagic.sln` and `dotnet run --project .\\Tests\\ConfigurationLifecycle\\ConfigurationLifecycle.csproj`.

## November 10 — Monitor focused build/validation evidence (PASS)

**User-local evidence:** three `.NET` solution builds passed (14.5s at explicit `438acbe`; 12.1s at explicit `3bd6eb5`; 11.0s on a later invocation without a printed SHA). The last two focused `ConfigurationLifecycle` runs passed **72/72** and **73/73**, respectively. The final pass includes the new zero-limit dashboard count/full-width Positions assertion, the compact global ticker tooltip, and SOM lifecycle checks. No compiler warnings appeared in these outputs.

**Source identity:** latest inspected PTMagic development branch head `16cfebced666bff3203ce3bea44f1bacd15a1ce2`; however, the final local invocation did not print its SHA, so do not claim it was independently SHA-stamped. Previous 337/337 all-harness acceptance at `fb94373` remains separate.

**Acceptance:** current Monitor changes **built successfully and passed focused regression checks**; live Monitor/browser layout (zero and positive buy limits, tooltip and metric table rendering) remains unverified. The earlier “build pending” language for these Monitor changes is superseded by this note. No need to repeat already passed checks without an additional source change. [Detailed evidence](../updates/2026-11-10-monitor-focused-validation-73.md).

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

**Evidence:** [November 10 — 337-group offline validation](../updates/2026-11-10-som-monitor-offline-validation.md).

## Next validation — November 10 Monitor metrics display update

At application source `f95ace1a0d8300cb63becf04e6a774439b505f71`, the Market Metrics **History Requirements** table has been removed from the Monitor only. All retention, metric readiness and warning calculations remain active. Global Settings Log now records all configured trend-level market-wide metrics at selection, with gray for unused metrics and bright white for those referenced in the setting trigger expression, regardless of the individual trigger truth value. The Activation Triggers column remains the Boolean-condition audit. Historical records are not backfilled from current snapshots; asset-only derivatives remain on their own per-asset metric page. The implementation adds two ConfigurationLifecycle offline tests but is **not yet compiled or executed locally**.

**Immediate verification:** the existing `Tests/Phase2OpenInterestIncremental/Run-Phase2Validation.ps1` must compile Monitor and run the full regression suite, including the two new cases and earlier SOM safety tests. Validate both the Market Metrics and Status Summary Monitor pages in a browser; thereafter proceed to Phase 2 global account/top-trader long/short ratio families. No new branches or candidate paths are authorized by this update.

## NEXT CHAT — verify SOM safety changes

Application source `891f709010c867259a6cde3df8e9c82781091b7f` (existing `phase1/market-data-foundation` branch) contains enable-only startup SOM, manual ProfitTrailer release, legacy release-checkpoint migration, and the red `PT: SOM` ticker plus raid-summary warnings on startup raids 1–2. **The source has NOT yet passed its new local .NET build or regression suite.** Last verified source `49f2aab66592b6e2922097ca5242b5a614090602` passed **332/332** before these changes.

**First action:** run/review `Tests/Phase2OpenInterestIncremental/Run-Phase2Validation.ps1`, fix any errors on the existing branch, and record actual test results with exact SHA. Never automatically issue global SOM `enabled=false`. Disappearing ticker after raid 2 is not proof of PT state and does not switch SOM off. After SOM validation, resume Phase 2 separate global account, top-trader account, and top-trader position long/short ratio metrics.

[Complete active new-chat handoff](../handoffs/2026-11-10-som-enable-only.md). Only specified unfinished Phase 1 *configured integration* tests were deferred; normal source builds and regressions remain mandatory.

## November 10 — Startup global SOM made enable-only; two-raid manual-release warning

**Safety correction source:** `891f709010c867259a6cde3df8e9c82781091b7f`, existing PTMagic branch `phase1/market-data-foundation`. **Published, not yet build/regression verified.** The previous verified 332/332 offline tests were for source `49f2aab66592b6e2922097ca5242b5a614090602` before this change.

The startup SOM API in PTMagic is now **enable-only**. The application no longer issues global `enabled=false` after normal analysis or configuration delivery, nor from restart/legacy release checkpoints. When `StartupSellOnlyMode=true`, an initial startup may send `enabled=true` to ProfitTrailer before long data loading; the user must manually disable global SOM in ProfitTrailer when ready. Without an ownership-aware live state API PTMagic cannot establish whether SOM is presently on, so it must not claim live-state monitoring or automatic restoration.

The checkpoint is versioned to schema 2 with enable intent, acknowledgement, and manual-review metadata. Old pending-release checkpoints migrate into manual review, never an automatic `false` request. An unacknowledged enable blocks unsafe bootstrap rather than repeatedly overriding manual choices. Normal user-selected settings continue to be delivered after conclusive analysis independently of the global SOM flag. TestMode never sends a remote SOM command.

**User-visible notice:** on the **first two raids of each startup**, when PTMagic requested the SOM guard, the RAID SUMMARY logs a warning to manually release SOM in PT. The shared Monitor ticker row displays a **red `PT: SOM`** badge alongside Selected Global Setting, SMS and PT health, with an information tooltip explaining startup activation, continued block on new/DCA buys, and manual release. The ticker disappears after raid 2; it does not verify the live PT flag or secretly switch it off. The underlying manual-review status remains inspectable in Status Summary.

**Mandatory verification:** updated `ConfigurationLifecycle` offline regressions cover no-auto-disable behavior, interrupted startup, restart, legacy checkpoint migration and first-two-raid notice. Execute the complete `Tests/Phase2OpenInterestIncremental/Run-Phase2Validation.ps1` .NET build and all offline harnesses. UI/browser rendering remains a separate acceptance step.

## November 10 — Funding and open-interest deterministic regression PASS

**Verified exact application source:** `49f2aab66592b6e2922097ca5242b5a614090602` · **.NET SDK 10.0.403** · solution build **11.0 seconds** · **16/16** offline harnesses, **332/332** test groups. All **17 funding tests**, **35 open-interest tests**, and **280 pre-existing regression groups** passed. Eight nonfatal nullable warnings remain in two older test harnesses. [Full source-attributed evidence](../updates/2026-11-10-phase2-funding-offline-validation.md).

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

**Status:** Phase 2 open-interest **deterministic development acceptance complete** at the exact tested source; configured live Binance data acquisition, native PT integration and Monitor/browser acceptance remain unverified. The specific outstanding Phase 1 integration scenarios remain deferred under D-042/D-045, **not** the Phase 2 offline tests. [Full 315-group evidence](../updates/2026-11-10-phase2-oi-offline-validation.md).

## November 10 — Testing scope clarified (D-045)

The owner deferred only the specific remaining Phase 1 configured-runtime / PT API / Monitor-browser integration acceptance checks discussed before moving to Phase 2. Phase 2 compilation, deterministic feature tests and affected regressions were **never deferred**. New source must be built and relevant harnesses executed before marking a development batch validated.

The source was subsequently built and tested: 315/315 deterministic groups passed at `5f51faa` on November 10. This older section preserves the mandatory testing policy rather than current status. The fail-fast PowerShell runner is available at `Tests/Phase2OpenInterestIncremental/Run-Phase2Validation.ps1` in the application repository. The Phase 1 configured integration checks remain separately pending, not waived.

## November 10 — OI retention corrected to MarketTrend-derived history

**Correction source:** `0ae76f4c7886397a06ad346b42a375f6aa06be00` on `phase1/market-data-foundation`.

The previously introduced independent `OpenInterestRetentionHours=72` setting and hard 672-hour software horizon were incorrect and have been removed from the application, supplied analyzer templates, and calculations. For each configured `MarketTrend` that explicitly enables `OpenInterestChange` and/or `OpenInterestValueChange`, the requirement is its exact `TrendMinutes` plus the reference/overlap observation. The OI collector retains enough history for the **longest eligible OI-enabled MarketTrend**, and recalculates that requirement when the configuration changes; no fixed history duration or 72-hour default controls OI.

`OpenInterestMaxRequestsPerRaid` remains an independent **request budget**, not a history duration (default 60, 0 disables acquisition). The provider's roughly one-month historical data availability remains an external source limitation: if the requested horizon or exact observation is not obtainable, the metric remains **UNAVAILABLE** rather than being silently shortened. Requests, memory and disk cache storage remain bounded for safety, but their caps are not a substitute for user-specified analytical history requirements. OHLCV `StoreDataMaxHours` continues to govern the existing OHLCV store separately.

The Monitor History Requirements view now distinguishes OI-derived duration and provider availability from OHLCV retention; OI no longer displays misleading `0 h` retention/capacity sufficient labels. Offline regression cases were extended for dynamically selected horizons, greater-than-72-hour history, and per-source independence. **Superseded result:** the subsequent November 10 build and 315/315 offline tests passed at `5f51faa`. Other runtime/browser/actual PT acceptance remains deferred under D-042.

## November 10 — Phase 2 incremental open-interest integration

**Application checkpoint:** `b723f76664aa0de6b76de3f5ddf281c036c32275` (`phase1/market-data-foundation`). The second Phase 2 implementation batch now connects the optional Binance USD-M open-interest client to a per-symbol, independently bounded cache and the normal normalized MarketTrend metric pipeline.

**Selectable asset-scoped metrics:** `OpenInterestChange` measures the percentage change in the Binance-native historical `sumOpenInterest` field. `OpenInterestValueChange` measures the percentage change in the separately reported `sumOpenInterestValue` field. Both use exact five-minute historical endpoints over the configured `TrendMinutes`; missing, mismatched or unaligned samples remain unavailable. Do not interpret reported value as a reconstructed quote notional.

**Opt-in config:** `MarketTrend.Metrics` must explicitly list either metric. OI history is **automatically derived from the longest OI-enabled MarketTrend**; no independent OI retention hours setting remains. The OHLCV `StoreDataMaxHours` limit is separate. `MarketAnalyzer.OpenInterestMaxRequestsPerRaid` defaults to **60** (range **0–400**, zero disables OI acquisition). Every request is a bounded single page (maximum 500 rows); pages are retrieved serially with fairness across markets and up to two pages per symbol per raid. The existing shared Binance HTTP transport applies retry/rate limits. The OI disk cache is per-symbol, compressed/versioned, validates integrity and timestamps, and is not authoritative for unavailable metrics.

**Integration:** after frozen-universe selection but before normalized metric evaluation, the runtime refreshes only the OI-enabled Futures asset population, using the existing pinned raid timestamp. The metric registry, existing asset trigger resolver, exported `MarketTrendAnalytics.json`/Monitor snapshot and independent history requirements now recognize OI. Spot and Binance US never fetch Futures OI. Existing PriceTrend-only configurations make **zero new OI requests**.

**Validation status:** 15 additional incremental offline case groups were authored alongside the original 18 raw OI groups. Source review was performed, but **no .NET build or C# harness execution occurred** in this turn. Therefore compile and runtime acceptance remain **UNVERIFIED**. The owner's deferral of further runtime testing remains in force; it is not a claim that the new code has passed.

**Remaining Phase 2:** OI deterministic tests are accepted at `5f51faa`; next develop funding, distinct account/position ratios, and taker-flow adapters, then Phase 2B market-wide derivatives aggregates. Live provider/runtime acceptance remains separate. The full Phase 1 PT API/browser checks remain deferred.

## November 10 — Phase 2 active (D-042)

The owner directed immediate continuation into Phase 2 and deferral of further Phase 1 configured acceptance. Earlier runtime, actual PT API, browser and restart checks stay **pending**, not accepted. They no longer block Phase 2 source development. See [Phase 2 handoff](../handoffs/2026-11-10-phase2-open-interest.md).

At application source `314214b1a20bcddd1643b8fa8df032db5463b04d`, the first **source-only** USD-M open-interest batch adds strict current/history observation models, one-page opt-in Binance endpoints and exact 5-minute historical change logic. Eighteen deterministic offline test groups were **authored but have not been executed**. No new metrics are registered and there are no new automatic raid requests. Next: bounded, pinned, cache-aware opt-in OI collection, then expose `OpenInterestChange` in the existing metric pipeline. Do not begin performance optimization or revise trading strategies.

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
3. Enable-only startup global SOM through PT API; release is exclusively manual in ProfitTrailer (D-047).
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

### 8.1 Startup global SOM — current enable-only contract (D-047)

With `Application.StartupSellOnlyMode=true`, PTMagic requests native PT global SOM ON before an uncertain first-run market-data bootstrap, using the configured ProfitTrailer API token and `POST /api/v2/globalSellOnlyMode?enabled=true`. Global SOM prevents new buys and DCA buys while allowing sells. No PAIRS/DCA/INDICATORS overlay is sent.

**PTMagic never disables SOM automatically.** After conclusive market analysis and acknowledged normal configuration delivery, it leaves the native PT SOM flag untouched. **Only the user disables SOM manually in ProfitTrailer** when ready. PTMagic cannot read an authoritative current SOM state or establish previous user ownership with this setter. Its acknowledgement/checkpoint is NOT a live state readback. `StartupSellOnlyMode=false` opts out of new automatic enabling but does not clear an existing SOM.

Startup guard metadata uses schema-v2 `_data/StartupSellOnlyModeState.json`. Legacy schema-v1 `PendingRelease` markers migrate to manual review; never replay an automatic OFF. A failed/unknown enable or partial multi-target acknowledgement cannot be treated as successful global protection. Persist local intent before sending, fail closed on uncertainty, maintain TestMode no-write isolation and keep confirmed normal configuration delivery separate from SOM control.

**Two-raid notice:** On startup raids 1 and 2, the RAID SUMMARY logs a manual-release warning. The Monitor's header displays a red `PT: SOM` informational ticker with an `(i)` tooltip beside Global Setting, SMS and PT health. Starting at raid 3, the warning/ticker disappear; their disappearance NEVER turns SOM off or proves the current remote state. Manual-review context remains in Status Summary.

**Verification:** current SOM source `891f709010c867259a6cde3df8e9c82781091b7f` remains untested by local .NET build/regressions. Earlier source `49f2aab66592b6e2922097ca5242b5a614090602` passed 332/332 offline groups *before* these SOM changes. [Active handoff](../handoffs/2026-11-10-som-enable-only.md).

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

**Status: started November 10 with optional raw OI source models/client; full acquisition/selection/trigger integration remains planned.** Owner explicitly deferred further Phase 1 acceptance and authorized moving into Phase 2 now. Do not start a separate performance program first.

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
- Global SOM enable-only guard with no automatic release, even after conclusive analysis or configuration acknowledgement; uncertain enable remains explicit for manual review.
- Persistent SMS deactivation without same-raid activation.
- Actual PT payload/readback for removal and delivery recovery, beyond TestMode simulation.
- Invalid timeframe/reference startup handling.
- Original Market Analyzer/graph continuity and the new editor/metrics behavior.
- Matching timestamps, units, coverage, setting identity, and delivery outcomes across logs, exports, history, and Monitor.

Use neutral application fixtures. Runtime observations should identify exact source/binary, exchange, quote, settings hash, TestMode state, and log interval. Do not include credentials in repository evidence.

### 18.4 Acceptance gates

A new metric family is accepted only when its contract, source, meaningful fixtures, execution results, exports/UI integration, and applicable runtime checks are accounted for. Unavailable external environments remain explicitly pending; do not infer cross-exchange acceptance from shared dispatch code.

A release candidate additionally needs documented migration/default changes, acknowledged-delivery behavior, restart recovery, consistent current documentation, supported packaging/runtime, and reproducible provenance.

## Immediate handoff and next development order

1. Run the existing `Tests/Phase2OpenInterestIncremental/Run-Phase2Validation.ps1` from the user's clone at application branch head `c35cc9f3ac180e241d240f6c2c06a00c2d887d8f`. Record the exact local SHA, .NET build result, all harness counts and warnings. The newly added complete-restart, partial-resume and corrupt-cache repair regressions have not yet been executed locally.
2. After offline validation passes, perform configured two-startup acceptance: confirm cache restoration, reduced Binance request counts, and unchanged metric availability/values across both startups.
3. Verify live Binance global-account and top-trader account/position endpoints, optional API-key handling, and Monitor browser display.
4. Only after derivative persistence acceptance, continue with taker-flow metrics and then Phase 2B aggregates. Dedicated performance optimization remains after all approved metric families.

Maintain D-047: PTMagic never sends global SOM OFF; the user manually releases PT global SOM. Dashboard PBL/Positions refresh remains a separate open task. Preserve the original jQuery `.load()` path and restrict any approved correction to scheduling in `Monitor/Pages/Index.cshtml`, after explaining the exact change and waiting for owner review.

Work directly on existing branches. **Ask before creating a new branch or duplicate candidate path.**

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
- [Current handoff](../handoffs/2026-11-10-som-enable-only.md): exact verification and next action.
- [Update index](../updates/README.md): dated evidence.
- [Historical roadmap index](README.md): preserved earlier plans.
- [Historical current documents](../history/README.md): pre-reconciliation snapshots.

This roadmap is maintained as current guidance. Preserve an earlier snapshot when a future change materially replaces its contract or ordering.
