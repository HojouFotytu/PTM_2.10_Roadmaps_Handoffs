# PTMagic 2.10 — ACTIVE NEW-CHAT HANDOFF: SOM safety and Phase 2

**Updated:** November 10, 2026 (KST)  
**Application:** [HojouFotytu/PTMagic](https://github.com/HojouFotytu/PTMagic), existing branch `phase1/market-data-foundation`  
**Latest published SOM/Monitor source:** `fb94373d8928b681e3ebe1f7209bd1439db42e72` — **offline ACCEPTED**  
**Last tested source:** `fb94373d8928b681e3ebe1f7209bd1439db42e72` — .NET SDK 10.0.403, Core/PTMagic/Monitor build PASS (15.6s and 10.3s), **16/16 harnesses and 337/337 groups PASS twice**  
**Documentation:** [PTM_2.10_Roadmaps_Handoffs](https://github.com/HojouFotytu/PTM_2.10_Roadmaps_Handoffs), existing `main`  
**Scope:** PTMagic 2.10 application, APIs, analytics and Monitor; *not* personal LONG/SHORT ProfitTrailer trading strategies or property-trio development.

**November 10 — Market Trends positive color:** The existing Market Trends column displays its activation-time PriceTrend percentage when available. Positive values (>0%) are **green**, regardless of setting-trigger membership; nonpositive/unknown trends remain **white** if referenced by the selected setting, **gray** if unused. The Market Metrics gray/white/green trigger-color policy is unchanged. Monitor-only UI change published; the last reported 71/71 ConfigurationLifecycle PASS and solution build predate this color adjustment. Local build/browser verification of the new source is pending.

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

## Historical validation instructions — already completed

The previous chat was marked **HIGH RISK** for context complexity. Continue here rather than reconstructing old iterations.

**Completed:** the following validation procedure was run successfully twice at `fb94373d8928b681e3ebe1f7209bd1439db42e72` (337/337 PASS). Do not repeat it for this source unless new changes require revalidation. Use the existing PTMagic clone:

```powershell
git switch phase1/market-data-foundation
if ($LASTEXITCODE -ne 0) { throw "Branch switch failed" }

git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Git pull failed" }

& ".\Tests\Phase2OpenInterestIncremental\Run-Phase2Validation.ps1"
```

The checked-in runner records the SHA, builds `PTMagic.sln`, and runs all **16 offline test harnesses**, including `ConfigurationLifecycle`, `MonitorSettingsRoundTrip`, `DecisionHistory`, and funding/OI tests. No real PT writes or live exchange requests are part of this suite.

**When the user provides the output:** diagnose failed builds/tests; fix production code and assertions in the existing paths; commit directly to the existing branch and re-run the affected/full tests. Record *actual* test counts, exact source SHA and warnings before declaring acceptance. Do not repeat previously passed older tests unless the new source requires regression verification.

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

**Current acceptance:** New SOM source `891f709010c867259a6cde3df8e9c82781091b7f` has **NOT** received a local .NET build or updated test output in this conversation. Live PT endpoint behavior, Monitor browser display and the older configured integration cases remain separately unverified. Only the previously discussed *specific remaining Phase 1 configured integration checks* were deferred, **not normal development builds/tests** (D-045).

## After SOM acceptance — Phase 2 queue

The prior verified source `49f2aab66592b6e2922097ca5242b5a614090602` passed **332/332**, including **17 funding**, **18 raw OI**, **17 incremental OI**, and **280 other** offline groups. The opt-in per-asset Binance Futures metrics are `OpenInterestChange`, `OpenInterestValueChange`, `FundingRate`, and `FundingSum`. Their history derives from enabled user `MarketTrend.TrendMinutes` and relevant lookbacks, not separate fixed OI/funding retention-hour defaults. Binance Spot and Binance US continue to use normalized price/volume/etc. metrics, but do not receive these Futures derivatives families.

**Next development family:** distinct Binance Futures global account long/short ratio, top-trader account ratio, and top-trader **position** ratio; do not conflate accounts with positions. Then taker flow, Phase 2B aggregates and subsequent higher-order features. Each batch requires source-specific calculations, availability semantics, and mandatory offline tests. General performance optimization remains later.

**Workflow preference:** Direct commits to the **existing branches**. **Always ask before creating a new branch or duplicate candidate path.** No repeated approval questions for routine publishing. Keep both repositories' `CHANGELOG-2.10.md` content identical, provide complete fail-fast PowerShell testing commands, and proactively flag conversation CAUTION/HIGH RISK.

## Copy to the new chat

> Continue PTMagic 2.10 from [the active SOM handoff](https://github.com/HojouFotytu/PTM_2.10_Roadmaps_Handoffs/blob/main/handoffs/2026-11-10-som-enable-only.md). Work directly in `phase1/market-data-foundation`; do not make new branches/duplicate candidates without asking. Current SOM source `891f709010c867259a6cde3df8e9c82781091b7f` is **UNTESTED**; last verified `49f2aab66592b6e2922097ca5242b5a614090602` passed 332/332 before SOM changes. Review my next full PowerShell regression output, fix failures, re-run and record exact source SHA. Maintain global SOM **enable-only**, user manual release, and the first-two-raid red `PT: SOM` ticker/warnings. Only after tests pass, continue Phase 2 distinct account/position ratio metrics.

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

