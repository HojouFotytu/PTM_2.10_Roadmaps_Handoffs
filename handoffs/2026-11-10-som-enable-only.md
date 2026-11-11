# PTMagic 2.10 — ACTIVE NEW-CHAT HANDOFF: SOM safety, Phase 2 derivatives and persistence

**Updated:** November 11, 2026 (KST)  
**Application:** [HojouFotytu/PTMagic](https://github.com/HojouFotytu/PTMagic), existing branch `phase1/market-data-foundation`  
**Current inspected application branch head:** `5a21a482711c8026b50fce10c55b3fb76f4075c3` (offline validated).  
**Last tested source:** `5a21a482711c8026b50fce10c55b3fb76f4075c3` — .NET SDK 10.0.403, Core/PTMagic/Monitor build PASS (13.9s), **18/18 offline harnesses and 386 checks PASS**. Eight nonfatal nullable warnings remain in two existing test projects.  
**Documentation:** [PTM_2.10_Roadmaps_Handoffs](https://github.com/HojouFotytu/PTM_2.10_Roadmaps_Handoffs), existing `main`  
**Scope:** PTMagic 2.10 application, APIs, analytics and Monitor only. ProfitTrailer LONG/SHORT strategy-settings development is a separate workstream with no implicit crossover. No strategy settings or settings-development artifacts are modified by this handoff.

## November 11 — Derivatives persistence and latest offline validation

**Current branch head and last user-tested application source:** `f108cd1ab39c44103bed91d1899f90f86a830eb4`. The exact user-run .NET 10.0.403 build and all 17 offline harnesses (384 checks) passed at this source.

At `f108cd1ab39c44103bed91d1899f90f86a830eb4`, the user ran the existing `Run-Phase2Validation.ps1`: Core, PTMagic and Monitor **PASS in 16.7 seconds**; **17/17 offline harnesses and 384 checks PASS**. Phase 2 results: funding 21, raw OI 19, incremental OI 18, and long/short ratios 39. ConfigurationLifecycle 73 and DecisionHistory 13. Eight nonfatal nullable warnings remain in `Phase1SmsSummaryIsolation` and `NormalizedPriceTrendMigration`; no build errors or failed harnesses.

### Unicode Binance Futures symbol correction

The live raid had failed because five Binance metadata COIN/PERPETUAL symbols use Chinese characters and the shared derivative symbol normalizer was ASCII-only: `哈基米USDT`, `币安人生USDT`, `我踏马来了USDT`, `牛来USDT`, `龙虾USDT`. `FuturesOpenInterest.NormalizeSymbol` now uses Unicode rune-aware letter/digit validation while continuing to reject whitespace, query separators and unsupported punctuation. OI, funding and ratio clients already URL-encode symbols; no endpoint/cache format, market eligibility, request budget, metric or trading-setting changes were made.

Focused tests cover all five names at normalization/URL level and service/cache handling for OI (`哈基米USDT`), funding (`币安人生USDT`) and ratios (`我踏马来了USDT`). The offline suite proves application-side handling only; live Binance endpoint acceptance and a configured raid with these symbols remain pending. Full evidence: [Unicode futures symbol validation](../updates/2026-11-11-unicode-futures-symbol-validation.md).

### Persistent derivative caches

- OI: `_data/DerivativesOpenInterestCache` (existing).
- Funding: `_data/DerivativesFundingCache`.
- Ratios: `_data/DerivativesLongShortRatioCache`, partitioned by endpoint source and symbol.

Funding and ratio caches store versioned compressed raw observations and verified provider-query coverage intervals. They use temporary-file/atomic replacement, validate restored identity/timestamps/values and defensive limits, and discard corrupt files fail-open. Coverage does not fabricate observations or turn missing data into zero. Funding cache ordering preserves distinct Regular/Special settlements at the same timestamp.

### Persistence implementation update — November 11 (local validation pending)

The 10-minute disk-cache save throttle previously skipped writes whenever a cache file was recently written, even if newly acquired observations or verified coverage had changed. Both funding and ratio cache writers now restore/compare the existing snapshot before applying the throttle: unchanged snapshots remain throttled, while changed rows or coverage are persisted immediately. This prevents a recent partial-cache write from suppressing a later progress update and forcing a restart to repeat already completed provider work.

Service-level restart regressions have been added to `Tests/Phase2Funding/Program.cs` and `Tests/Phase2LongShortRatios/Program.cs`. They construct a first service to persist complete coverage, construct a second service against the same directory and assert that no second provider request occurs, then corrupt a separate symbol cache and verify that a fresh service discards it and repairs coverage with one bounded request.

**Exact application source tested:** `86fa4c9a306f7eb61742c26bbb1ae633bb775a2a`. Relevant persistence commits: `6900e4b` funding cache throttle correction; `047abfd` ratio cache throttle correction; `b085aa8` complete funding-service restart test; `51adbb8` complete ratio-service restart test; `71c7f1e` funding partial-coverage restart test; `c35cc9f` ratio partial-coverage restart test; `578aad4` funding corrupt-cache replacement assertion; `320ad5a` ratio corrupt-cache replacement assertion. The Monitor page-consolidation assertion was corrected in `86fa4c9`.

**User-run validation at `86fa4c9`: PASS.** .NET 10.0.403 solution build PASS in 10.3 seconds; all 17/17 offline harnesses and 378 checks PASS. Phase2Funding 20; Phase2OpenInterest 18; Phase2OpenInterestIncremental 17; Phase2LongShortRatios 36; ConfigurationLifecycle 73; DecisionHistory 13. Eight nonfatal nullable warnings remain in two existing test projects. Complete and partial cache restart, no-duplicate-request, and corrupt-cache replacement checks passed for both funding and ratios. See [dated validation evidence](../updates/2026-11-11-phase2-derivative-persistence-offline-validation.md). Configured two-startup runtime acceptance remains pending.


D-051 source changes are implemented and offline validated at `5a21a482711c8026b50fce10c55b3fb76f4075c3`: global-account ratio only, no optional API-key path, no user-configurable or temporary sixty-request ceilings, and shared adaptive derivative admission. **18/18 harnesses and 386 checks PASS.** Configured Unicode-market raid and two-startup persistence acceptance remain pending; taker flow follows.

**November 10 — Market Trends positive color:** The existing Market Trends column displays its activation-time PriceTrend percentage when available. Positive values (>0%) are **green**, regardless of setting-trigger membership; nonpositive/unknown trends remain **white** if referenced by the selected setting, **gray** if unused. The Market Metrics gray/white/green trigger-color policy is unchanged. Monitor-only UI change published; the last reported 71/71 ConfigurationLifecycle PASS and solution build predate this color adjustment. Local build/browser verification of the new source is pending.

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
- Preserve the existing DashboardTop jQuery `.load()` request and callback; the authorized correction is **scheduling-only in `Monitor/Pages/Index.cshtml`**.
- Do not reintroduce the experimental PBL count endpoint, async count cache, or custom AJAX replacement. Do not change PBL/Positions retrieval or calculations, DashboardTop rendering, DashboardBottom, ticker refresh, tooltip behavior or profit coloring.
- Do not alter the separate ticker tooltip-preservation code as a side effect.
- Preserve existing PBL/Positions calculations and profit coloring.
- **Explain the exact proposed change, files, and scope before editing any files.** The owner specifically corrected the workflow after an attempted premature update.
- No implementation for this refresh correction has been agreed or committed. The current source remains the exact rollback state above.

**Next dashboard action:** review the November 2 callback-dependent polling path and propose a scheduling-only change in `Monitor/Pages/Index.cshtml`. Preserve the original `.load()` request and callback. Explain the exact change, files and scope before editing; wait for owner review. Continue Phase 2 ratio-metric development in parallel.


## November 11 — Latest Monitor formatting focused validation PASS

User-executed `.NET 10` solution build **PASS (15.7 seconds)** for Core, PTMagic and Monitor, with **75/75 ConfigurationLifecycle checks PASS** and no warnings/errors reported. Includes the latest Market-Wide Metrics page-local uppercase/gray/centering source check, plus PBL-count, compact ticker and SOM checks. `git pull` reported "Already up to date" but **the local run did not print a source SHA**. At documentation review the existing PTMagic branch head was `44dd757e29808eaa8662fbdf8a63835efb02378a`; do not treat this as a locally stamped test SHA. Previous unverified-build statements for this change are superseded by this evidence.

**Offline build and focused validation are complete.** Live Monitor browser appearance, actual ProfitTrailer PBL count agreement and external PT/Binance integration remain unverified. No need to repeat these focused tests absent relevant source changes. [Evidence](updates/2026-11-11-monitor-market-wide-formatting-validation.md).

## November 10 — Market-Wide Metrics display correction (validation pending)

Corrected the reported left-aligned, white metric labels by adding **page-local, scoped rendering rules** in `Monitor/Pages/MarketMetrics.cshtml`. Seven group titles are now emitted **uppercase white**, metric subheadings are **muted gray**, and **all columns and stacked content are centered**. This avoids stale cached external `custom.css` overriding the new presentation. No analytics, Per-Market Metrics, or PT behavior changed. Extended one focused source regression check. Published on existing `phase1/market-data-foundation` branch; local solution build and browser verification are **pending** for this change. Prior **75/75 PASS** applies to earlier source.

## November 10 — Market Metrics and PT PBL focused validation PASS

The user's local `.NET` solution build passed for Core, PTMagic and Monitor (15.3 seconds); **ConfigurationLifecycle 75/75 PASS**, including the two new checks for centered/two-row Market-Wide Metrics headings and for retrieving PT's complete PBL even when `MaxDashboardBuyEntries=0`. No errors or warnings were reported. The `git pull` output showed "Already up to date" without a printed source SHA. At review the application branch head was `33c7a1ef80811677e5cc3559f561cfe773f31961`; do not claim this is an independently local-reported SHA.

The previous "build pending" statements for this batch are superseded by these passing results. **Browser layout verification and actual PT PBL count agreement remain unverified**; this was an offline source-level regression harness, not PT live API acceptance. Do not repeat these passed focused checks without another relevant code change. [Validation evidence](updates/2026-11-10-monitor-pbl-metrics-75-validation.md).

## November 10 — Market Metrics header alignment and accurate PBL count (build pending)

**Market-Wide Metrics:** seven grouped columns now use a separate **upper heading row** for uppercase white group names and **lower heading row** for muted-gray individual metric names. Trend/Timeframe/Markets headings span both rows. Every header and value column is centered, including group stacks; the Per-Market Metrics table and analytics computations are unchanged. Source check added for header structure and styling.

**Dashboard Possible Buys:** identified and removed an early return in `ProfitTrailerData.BuyLog` that prevented the native PT `/api/v2/data/pbl` refresh whenever `MaxDashboardBuyEntries=0`. Now the heading always uses the full cached PT PBL count independent of `Take(MaxDashboardBuyEntries)`, while the list stays hidden at zero and Positions occupies the full width below. The existing cache interval still bounds PT requests. Source regression added; allowing PBL fetches with a zero display limit changes PT API traffic compared with the former early return.

**Validation:** changes committed to existing PTMagic `phase1/market-data-foundation`. No local build, focused tests, or browser verification has yet been supplied for the newest changes. Previous 73/73 focused PASS predates these changes. Run `git pull --ff-only`, `dotnet build .\\PTMagic.sln` and `dotnet run --project .\\Tests\\ConfigurationLifecycle\\ConfigurationLifecycle.csproj`.

## November 10 — Monitor focused build/validation evidence (PASS)

**User-local evidence:** three `.NET` solution builds passed (14.5s at explicit `438acbe`; 12.1s at explicit `3bd6eb5`; 11.0s on a later invocation without a printed SHA). The last two focused `ConfigurationLifecycle` runs passed **72/72** and **73/73**, respectively. The final pass includes the new zero-limit dashboard count/full-width Positions assertion, the compact global ticker tooltip, and SOM lifecycle checks. No compiler warnings appeared in these outputs.

**Source identity:** latest inspected PTMagic development branch head `16cfebced666bff3203ce3bea44f1bacd15a1ce2`; however, the final local invocation did not print its SHA, so do not claim it was independently SHA-stamped. Previous 337/337 all-harness acceptance at `fb94373` remains separate.

**Acceptance:** current Monitor changes **built successfully and passed focused regression checks**; live Monitor/browser layout (zero and positive buy limits, tooltip and metric table rendering) remains unverified. The earlier “build pending” language for these Monitor changes is superseded by this note. No need to repeat already passed checks without an additional source change. [Detailed evidence](updates/2026-11-10-monitor-focused-validation-73.md).

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

## November 10 — SOM and Monitor validation accepted (latest evidence)

**Exact verified application source:** `fb94373d8928b681e3ebe1f7209bd1439db42e72`. The user ran the existing full validation script twice: .NET SDK 10.0.403 solution builds **PASS** in 15.6s and 10.3s; **all 16 offline harnesses and 337/337 test groups PASS in both runs**. This includes 71 ConfigurationLifecycle checks (SOM enable-only, startup manual-release notice, new metric snapshots), 28 Monitor settings roundtrip checks and 13 DecisionHistory checks. The first build reported eight nonfatal pre-existing nullable test-source warnings; the second reported no warnings, consistent with incremental compilation. No live exchange, PT API or browser acceptance is claimed.

The Market Metrics History Requirements **UI panel** is removed; its diagnostic calculations remain active. Global Settings Log captures all available **market-wide** metrics across configured trends at entry creation and highlights a metric in white when referenced by any selected-setting trigger (even if FALSE/UNAVAILABLE); other metrics are gray. Existing history must not be fabricated from later snapshots. The red startup `PT: SOM` notice lasts only the first two raids; PTMagic never automatically requests global SOM OFF and the user releases it manually. **Do not rerun this completed offline suite as a prerequisite for new Phase 2 work.** Next development: distinct Futures global account, top-trader account and top-trader position long/short ratios. Configured runtime and Monitor browser verification remain separately open.

**Evidence:** [November 10 — 337-group offline validation](updates/2026-11-10-som-monitor-offline-validation.md).

## Latest full offline validation — November 11

The user executed `Tests/Phase2OpenInterestIncremental/Run-Phase2Validation.ps1` at exact source `875b4feb71104fbc609bd07dc3120405218d325f`. The .NET 10.0.403 solution build succeeded in 17.4 seconds and all **17/17 harnesses passed**. The runner compiles Core, PTMagic and Monitor. It does not make live Binance requests, execute configured raids, write to ProfitTrailer, or verify browser rendering.

**Standard local command for future code changes:**

```powershell
$ErrorActionPreference = "Stop"

git switch phase1/market-data-foundation
if ($LASTEXITCODE -ne 0) { throw "Branch switch failed" }

git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Git pull failed" }

git log -1 --format="%H"

& ".\Tests\Phase2OpenInterestIncremental\Run-Phase2Validation.ps1"
if ($LASTEXITCODE -ne 0) { throw "Phase 2 validation failed" }
```

Do not repeat the full suite absent a new code change that warrants it. The service-level complete-restart, partial-resume and corrupt-cache repair regressions are now authored. Next: have the user execute the existing runner at the current branch head and record the exact source SHA, build result, harness counts and warnings.

## Phase 2 — Binance Futures derivatives and persistence (D-051 current scope)

The current approved ratio scope is one public, opt-in, asset-scoped metric: `GlobalLongShortAccountRatio`. It uses exact five-minute observations over each enabled MarketTrend's `TrendMinutes`; all expected timestamps are required and missing data remains UNAVAILABLE. The calculation averages implied long-side shares `r/(1+r)` and converts the mean back to a ratio; neutral is 1.0.

The two top-trader metrics, their endpoints, authentication-specific handling and optional API-key requirement are removed from current scope by D-051. No additional Binance Futures API key is required for the retained public global-account metric.

The three per-raid request-budget properties are also removed from the user-facing PTMagic analyzer configuration. PTMagic must manage derivative acquisition dynamically through its shared Binance rate-limit state, endpoint request weights, response headers and 429/418 cooldowns. Preserve internal pagination, per-symbol progress safeguards, fair scheduling, incremental coverage, disk persistence, cancellation and UNAVAILABLE semantics. Do not replace the removed settings with other arbitrary user-configurable static limits.

**Implementation status (November 11 update):** D-051 source is published and offline validated at `5a21a482711c8026b50fce10c55b3fb76f4075c3`. Core, PTMagic and Monitor build PASS in 13.9s; 18/18 harnesses and 386 checks PASS, including 9 adaptive acquisition checks. Eight nonfatal nullable warnings remain. No configured Binance/PT/Monitor acceptance is established.

Funding and the retained global-account ratio use versioned compressed disk caches with raw observations and verified query-coverage intervals. OI retains its separate cache. The five Unicode COIN perpetual symbols have passed application-side normalization, service/cache and URL-encoding offline tests; live Binance endpoint acceptance and a configured raid with those symbols remain pending. See [Unicode validation evidence](../updates/2026-11-11-unicode-futures-symbol-validation.md).

## Current owner-approved SOM contract — D-047 (supersedes prior auto-release)

- With `Application.StartupSellOnlyMode=true`, PTMagic may send global SOM **ON** through native `POST /api/v2/globalSellOnlyMode?enabled=true` before long initial startup analysis. Currently the live code requests ON at the first process startup when enabled; it does **not** independently determine whether initialization will be prolonged.
- PTMagic must **NEVER** send `enabled=false` automatically, even after fresh analysis, acknowledged normal configuration delivery, restart or opt-out. The **user manually disables SOM in ProfitTrailer when ready**. While ON, new buys and DCA buys are blocked; sells remain allowed.
- The boolean API does **not** report authoritative prior user ownership or live SOM state. A checkpoint/ticker cannot prove SOM remains ON or is OFF.
- No temporary PAIRS/DCA/INDICATORS overlay. Normal setting/SMS publication and startup global SOM control remain separate.
- TestMode never sends native SOM commands or replaces live checkpoint state. `StartupSellOnlyMode=false` prevents a new automatic enable but does not release a previously enabled PT global flag.
- The global SOM API adapter rejects disable calls. Old v1 `PendingRelease` checkpoints migrate to schema v2 manual review. Save enable intent before posting; a failed/uncertain enable must not silently count as safe protection. Each configured PT target requires acknowledgement; partial multi-target failure cannot be reported as a complete success.

## Required two-raid warning and Monitor UI

- **Raid 1 and raid 2**: RAID SUMMARY logs a warning that PTMagic requested global SOM ON and the user must turn it OFF manually in ProfitTrailer.
- The Monitor header adds a **red `PT: SOM` ticker** alongside selected Global Setting, SMS and PT health, with a small `(i)` tooltip explaining enable-only startup protection, manual release, and the fact that this is **not a live global SOM status readback**.
- **Raid 3 onward**: both temporary warnings stop. Disappearance must NEVER disable global SOM or imply that PT is trading again. The underlying manual-review details remain in Status Summary.
- The ticker uses existing `_get/TickerWidgets` output and `_Layout.cshtml` AJAX insertion/removal, not a separate persistent notification mechanism.

## Source reference

| Area | File |
|---|---|
| Enable-only lifecycle, notice count, raid warning | `Core/Main/PTMagic.cs` |
| Reject global SOM OFF requests | `Core/ProfitTrailer/GlobalSellOnlyModeAPI.cs` |
| Versioned manual-review checkpoint | `Core/ProfitTrailer/StartupSellOnlyModeState.cs` |
| Summary flags | `Core/DataObjects/PTMagicData.cs` |
| Red header ticker and tooltip | `Monitor/Pages/_get/TickerWidgets.cshtml` |
| Insert/remove ticker on AJAX refresh | `Monitor/Pages/_Layout.cshtml` |
| Setting help | `Monitor/Pages/SettingsGeneral.cshtml` |
| Revised lifecycle, migration, ticker assertions | `Tests/ConfigurationLifecycle/Program.cs` |
| Full fail-fast offline verification | `Tests/Phase2OpenInterestIncremental/Run-Phase2Validation.ps1` |

**Priority test topics:** no `false` SOM request under any lifecycle path; migrated v1 release intent never causes OFF; uncertain/failed enable blocks unsafe bootstrap; no repeated enable within one startup; restart behavior; two-raid warning/ticker visibility then removal; TestMode isolation; multi-target partial failures. Existing ticker source assertion assumes the runner starts in repository root (which the checked-in runner does). These are validation targets, **not confirmed failures**.

**Current acceptance (updated November 11):** latest user-executed build and all 17 offline harnesses passed at `875b4feb71104fbc609bd07dc3120405218d325f`. Current branch head is `c35cc9f3ac180e241d240f6c2c06a00c2d887d8f`; later Monitor UI changes and derivative cache/restart-test changes are not yet covered by a user-run build or harness execution. Dashboard rollback is part of the previously tested application source, but live DashboardTop browser refresh is not established. Live PT/Binance API and configured two-startup cache acceptance remain separate.

## Immediate handoff and next development order

1. Implement D-051 in the PTMagic application: retain only public `GlobalLongShortAccountRatio`; remove both top-trader metric feeds and their API-key-only request path; remove the three user-configurable per-raid request-budget properties.
2. Implement application-managed adaptive derivative acquisition using shared Binance rate-limit state, endpoint request weights, response headers and 429/418 cooldowns. Preserve internal pagination, per-symbol progress safeguards, fair scheduling, incremental coverage, persistence and UNAVAILABLE semantics. Do not add replacement user-configurable static limits.
3. Build and run the existing offline validation suite. Add focused tests for global-account-only ratio behavior, absence of top-trader/API-key paths, adaptive capacity, fairness, cooldowns and cross-family shared rate-limit coordination.
4. Perform configured runtime acceptance with the five Unicode COIN perpetual symbols, then configured two-startup derivative persistence acceptance. Record exact running binary/source, live request counts, cache restoration, metric availability/values and Monitor output.
5. Only after configured derivative persistence acceptance, continue with taker-flow metrics and then Phase 2B aggregates.

Maintain D-047: PTMagic never sends global SOM OFF; the user manually releases PT global SOM. Dashboard PBL/Positions refresh remains a separate open task. Preserve the original jQuery `.load()` path and restrict any approved correction to scheduling in `Monitor/Pages/Index.cshtml`, after explaining the exact change and waiting for owner review.

Work directly on existing branches. **Ask before creating a new branch or duplicate candidate path.**

## Copy to the new chat

> Continue PTMagic 2.10 from this [active handoff](https://github.com/HojouFotytu/PTM_2.10_Roadmaps_Handoffs/blob/main/handoffs/2026-11-10-som-enable-only.md). Work on the existing `phase1/market-data-foundation` branch; do not create branches or duplicate candidate paths without asking. Last user-tested source `875b4feb71104fbc609bd07dc3120405218d325f`: .NET 10 solution build PASS and all 17 offline harnesses PASS. Current application branch head `320ad5adee314c0ac59208556612ef8ca099e5e8` includes later Monitor UI, cache-throttle corrections and service-level complete/partial restart regressions. The first run at `c35cc9f` built successfully but stopped in Phase2Funding on an incorrect corrupt-cache assertion; both funding and ratio recovery assertions have since been corrected and need rerunning. Next: local validation, configured two-startup cache acceptance, then live Binance/Monitor checks. Taker flow follows persistence acceptance. Keep startup SOM enable-only with manual PT release. Dashboard refresh remains separate: preserve the original `.load()` path and restrict any approved fix to scheduling in `Monitor/Pages/Index.cshtml`; explain exact changes before editing.

[Status](../STATUS.md) · [Current roadmap](../roadmaps/CURRENT.md) · [D-045/D-047 decisions](../DECISIONS.md) · [Funding handoff](2026-11-10-phase2-funding.md) · [332-check evidence](../updates/2026-11-10-phase2-funding-offline-validation.md).

## Additional November 10 change — Monitor metric display (NOT YET TESTED)

**Latest application source:** `f95ace1a0d8300cb63becf04e6a774439b505f71` on existing `phase1/market-data-foundation`. The SOM enable-only source remains present; its pending validation has not been superseded. The Monitor Market Metrics **History Requirements** section has been removed completely **from the page only**; source history calculations, warning diagnostics, retention and availability policies are unchanged.

The Status Summary Global Settings Log now persists all configured market-wide trend metrics **at activation time**. Gray means the metric was not part of the selected setting's activation trigger set; bright white means it was referenced, regardless of TRUE/FALSE/UNAVAILABLE outcome. The existing Activation Triggers column retains condition results; missing/unavailable metrics stay explicitly unavailable. Earlier entries are not backfilled using later values, and asset-only metrics are not presented as global results. A retained DEFAULT has no white items when no trigger expression selected it.

**Authored tests:** two ConfigurationLifecycle groups for referenced/unreferenced/unavailable metrics and activation-time immutability. **No local .NET compile, harness execution or browser rendering has yet been recorded.** The old 332/332 PASS predates both this change and SOM changes.

**Run locally from the existing application clone:**

```powershell
git switch phase1/market-data-foundation
if ($LASTEXITCODE -ne 0) { throw "Branch switch failed" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Git pull failed" }
git log -1 --format="%H"
& ".\\Tests\\Phase2OpenInterestIncremental\\Run-Phase2Validation.ps1"
if ($LASTEXITCODE -ne 0) { throw "Full validation failed" }
```

After the run, inspect the Status Summary Global Settings Log for all configured trends/metrics and white highlights on referenced FALSE as well as TRUE conditions. Verify the separate Market Metrics page has no history requirements panel. Keep startup SOM enable-only and user manually released. If an actual build/test fails, fix directly on the existing development branch, then re-run; record the actual SHA, counts and warnings.


## November 10 — Corrected Global Settings Log layout (pending local build)

**Owner-directed UI:** exactly two market-data columns, **Market Trends** and **Market Metrics**, following Activation Time / Setting / Active Time. The separate Activation Triggers column, expression, and TRUE/FALSE labels have been removed from the page. All configured MarketTrends are listed gray unless referenced by the selected setting (white). All configured metrics are listed gray unless referenced (white); a condition whose recorded trigger result is TRUE is **green**. Asset-only metric names are included without a fabricated global value. A selected setting's own recorded trigger set determines colors, not later analytics. No changes to trading logic, metric calculations, SOM, or provider acquisition. Historical entries lacking full metric snapshots cannot be reconstructed reliably.

**Implementation:** committed to the existing PTMagic `phase1/market-data-foundation` branch. **Validation:** newest change not yet locally compiled or browser-tested; the earlier full 337/337 PASS belongs to source `fb94373` before the UI correction. Focused command after `git pull --ff-only`: `dotnet build .\\PTMagic.sln` and `dotnet run --project .\\Tests\\ConfigurationLifecycle\\ConfigurationLifecycle.csproj`. Visually check two columns and white/gray/green logic.



## November 11 — Top-trader removal validation update

The active Phase 2 status is now: only public `GlobalLongShortAccountRatio` remains. Both top-trader feeds and their API-key path were physically removed and user-validated at `1a1f1804237288433ed046b30fb7d9b780a32066` (17/17 offline harnesses, 377 checks PASS; solution build PASS in 18.2s). Eight nonfatal nullable warnings remain.

**Superseded:** request-budget removal was validated at `6606712`; adaptive acquisition is now offline validated at `5a21a48` (18/18 harnesses, 386 checks). Configured Unicode-market raid and two-startup persistence acceptance remain pending. See [adaptive acceptance record](../updates/2026-11-11-derivative-adaptive-acquisition-implementation.md).


## November 11 — Adaptive acquisition implementation handoff (latest)

**Application source:** [`5a21a48`](https://github.com/HojouFotytu/PTMagic/commit/5a21a482711c8026b50fce10c55b3fb76f4075c3), existing `phase1/market-data-foundation` branch. **Offline validated:** .NET 10.0.403 build PASS in 13.9s, 18/18 harnesses and 386 checks PASS (8 nonfatal nullable warnings).

**Implementation:** Removed all three internal `DefaultRequestsPerRaid=60` constants. Production passes an unbounded page-count sentinel, while service-level bounded parameters remain for deterministic tests and internal pagination/correctness safeguards. `BinanceRateLimitTracker` now coordinates shared Futures IP weights, the OI/global-account historical endpoint allowance and the separate funding allowance, 429/418 Retry-After cooldowns, and cancellation-aware HTTP admission. The three families execute concurrently through `BinanceDerivativeAcquisitionScheduler`, granting fair per-page access until `Application.MaxAnalysisAgeSeconds` expires; partial histories remain UNAVAILABLE and persist for later raids. Existing SOM, PT writes, Monitor and LONG/SHORT strategy development are untouched.

**Local acceptance complete:** the user ran `Tests/Phase2OpenInterestIncremental/Run-Phase2Validation.ps1` at exact `5a21a482711c8026b50fce10c55b3fb76f4075c3`; all 18 harnesses and 386 checks passed. **Next:** configured Unicode-market raid, two-startup persistence/request reduction, live Binance and Monitor verification. Do not treat offline tests as live runtime evidence. See [detailed implementation and validation record](../updates/2026-11-11-derivative-adaptive-acquisition-implementation.md).
