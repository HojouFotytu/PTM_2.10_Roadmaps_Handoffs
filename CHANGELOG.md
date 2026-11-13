# PTMagic 2.10 — Change log


## November 14 — PT Data date-range pagination implementation

**November 14, 2026 — PT Data Export handoff:** PTMagic [`618b628`](https://github.com/HojouFotytu/PTMagic/commit/618b6285d18e3c655139ae675bce389b72034ee5) replaces historical record limits with **7 days / 1 month / 3 months / 6 months / all available**, requests sorted descending buys/sales across page-zero-based `perPage=25` batches, and writes schema-1.1 manifests while preserving historical `extraInfo -- CV:` values. Application HEAD [`bda2394`](https://github.com/HojouFotytu/PTMagic/commit/bda2394eccd0e0439a8578bf7c7b1c4287e15382) does not further change the PT Data source. The November 13 **schema-1.0** ZIP showed 23 buys, 25 sales, eight PAIRS and two DCA; it does **not** validate the new multi-page exporter. Current live date-cutoff, multi-page and security acceptance remain open. The manifest's `range_coverage_complete` means only no duplicates were detected; it does **not** prove lifetime completeness. See [current PT Data handoff](handoffs/2026-11-13-monitor-performance-export-design.md).

**D-053 implementation and removal-audit checkpoint — November 12, 2026:** PTMagic source [`892a5f1f4729a3fccd3cb477ba6ad22fbbe0918d`](https://github.com/HojouFotytu/PTMagic/commit/892a5f1f4729a3fccd3cb477ba6ad22fbbe0918d) contains the completed removal of `OpenInterestChange`, `OpenInterestValueChange` and `GlobalLongShortAccountRatio`, including their acquisition/services/active caches/registry/Monitor integrations. The source audit compared the **22-metric pre-introduction baseline** [`66629347`](https://github.com/HojouFotytu/PTMagic/commit/66629347f0dc9c7b68ea9f1c3f5bf536f3d7c427), **27-metric pre-removal** `d101b5a0` and current **24-metric** code: all 22 original metric identities and scopes survive; `FundingRate` and `FundingSum` also survive. A real shared Unicode symbol-validator dependency was temporarily broken by deleting OI, then repaired by [`02820822`](https://github.com/HojouFotytu/PTMagic/commit/02820822b9bb) and [`d7847c46`](https://github.com/HojouFotytu/PTMagic/commit/d7847c46190b). No further major/critical removal-related defect was established by source inspection; **current-revision local build, 15-harness test execution and configured runtime acceptance remain unverified**. The earlier 18-harness PASS at `d101b5a0` is strictly **pre-removal evidence**. [Full read-only audit](updates/2026-11-12-d053-removal-code-audit.md) (links relative to repository root). **This checkpoint supersedes all contradictory claims below that removal is pending, that retired OI/positioning is active, or that its tests/feature work remain required. Dated implementation evidence is retained as history.** No rollback and no strategy-settings work.

> **November 12, 2026 scope supersession:** D-053 withdraws OI and long/short positioning metrics from the approved PTMagic 2.10 roadmap. Earlier change-log entries remain historical implementation records; source removal is complete and source-audited, with current-revision local execution pending. See [active decisions](DECISIONS.md) and [current roadmap](roadmaps/CURRENT.md).

For the cumulative changes that remain in effect and must accompany PRs/merges, use [CHANGELOG-2.10.md](CHANGELOG-2.10.md). This file retains chronological project history.

**Current application source checkpoint:** `87b9eaa1c865e39d8fff6a657e1b332012be8c16`

## 2026-11-09 — Highlight all TestMode console messages in magenta

- Application source `87b9eaa1c865e39d8fff6a657e1b332012be8c16` configures the same NLog `ColoredConsole` `highlight-row` for case-insensitive `TestMode` text in PTMagic, Monitor and packaged default `nlog.config` files.
- This matches the purple startup TESTMODE WARN display for subsequent INFO-level preview and RAID SUMMARY messages without changing severity or file-log contents.
- **User-local validation PASS November 9:** .NET SDK 10 `dotnet build` succeeded for Core/PTMagic/Monitor in 15.1s. The three XML/rule checks each printed `PASS`. The user's `git pull --ff-only` reported `Already up to date` but did not print HEAD. The actual console color, live `nlog.config` deployment, and NLog runtime interpretation of the rule remain unverified.

## 2026-11-09 — Native focused cache validation passed

- User reported exact `925db7c153ee4d53cfe3b7bf736318e7a30bccf1` after `git pull --ff-only` and .NET SDK 10.0.403.
- `dotnet build .\\PTMagic.sln` succeeded for Core/PTMagic/Monitor in 18.3 seconds.
- New NormalizedWarmStartCache harness **8/8 PASS**; Phase1AnalyticsReliability **16/16 PASS**; Phase1COhlcv **13/13 PASS**. **37/37 focused checks** completed.
- No native exchange restart/cold-vs-warm traffic or metric-parity results supplied yet. Those remain open.
- Published application `87b9eaa1c865e39d8fff6a657e1b332012be8c16` records the evidence in the test README and cumulative release record; executable files unchanged.

## 2026-11-09 — Persistent normalized OHLCV warm-start cache

- Published PTMagic `925db7c153ee4d53cfe3b7bf736318e7a30bccf1`: a versioned compressed per-market/per-exchange cache under `_data/NormalizedOhlcvCache`, restored before the pinned normal kline refresh. The cache is data only; gaps, missing history and stale observations still require exchange backfill.
- Added seven offline regression groups at `Tests/NormalizedWarmStartCache`. **Tests authored but not yet executed; old 272 passing results remain attached to their previous exact revisions.**
- This targeted restart optimization is authorized now, notwithstanding the earlier deferral of the broader performance program. It does not alter legacy one-minute market reconstruction or first-seen-date collection.
- Updated cumulative effective-change record, decision D-040, roadmap/status and handoff with fail-fast local commands and two-startup acceptance.

## 2026-11-07 — Establish the cumulative release record and surface startup SOM

- Published application `a0b375cc9b2db469a48a31b713385f35500cc763` with [CHANGELOG-2.10.md](CHANGELOG-2.10.md), mirrored in this repository, covering only surviving 2.10 changes from the November 2 foundation. README, contributor rules, the handoff template and D-039 require maintenance with PRs and merges.
- Both supplied general-settings templates explicitly contain StartupSellOnlyMode=true; only the development template needed the field added. The existing General Settings APPLICATION toggle already saved on/off values and now has associated label/help text explaining TestMode.
- Reviewed source, parsed the existing comment/trailing-comma settings format, checked preservation of other values, verified source references and synchronized the two release records. No .NET build, harness, live API or browser execution was performed. Existing 272-check evidence remains attached to its actual sources.
- Updated current source pins and launch commands. Preserve the user-reported ongoing long run; collect its result before requesting another launch. TestMode does not activate native SOM.

## 2026-11-07 — Complete deterministic validation and advance to configured runtime

- The user built Core, PTMagic, and Monitor at exact source `d331fbd059041241069646c3bb82ac6549423a70` with SDK 10.0.403 in 10.9 seconds. ConfigurationLifecycle passed all 66 checks, and DecisionHistory passed all 13.
- Combined with the earlier 193 passes in ten harnesses at `86c2ea3`, all 272 current checks now have passing results across twelve projects. The record preserves both execution revisions; it is not a claim of one complete twelve-project run at `d331fbd`.
- The two Telegram fixture corrections are verified. Production source and assertions were unchanged between the runs. Published `fac346c88b2c634439083e7515193d756ac3d186` updates five application harness READMEs to record these results without new executable changes or additional test requirements.
- The current handoff advances to a configured TestMode run. Real PT API acknowledgement/native SOM behavior, browser integration, and remaining exchange/quote cases retain their separate acceptance requirements.
- A subsequent runtime log repeats the old bare-USDT failure and lacks the current source/main-market logs, establishing pre-fix Core behavior. Exact running SHA and loaded DLL path remain unknown; its runtime working directory is separate from the checkout. The next handoff explicitly launches the built DLL with that existing directory and TestMode configuration, then verifies identity. This selects current binaries for validation without claiming a permanent installed-launcher update. Passing checkout tests retain their recorded evidence.
- [Completed validation evidence](updates/2026-11-07-completed-harness-validation.md) · [Current verification handoff](handoffs/2026-11-07-stabilization-correlation-validation.md).

## 2026-11-07 — Record 193 passing checks and correct two fixture type references

- The user built Core, PTMagic, and Monitor at exact source `86c2ea3ff430b62e654f929a222935ec53ea8fa6` with SDK 10.0.403 in 15.8 seconds. Ten harnesses passed 193 checks, including all 40 TriggerConfigurationValidation and 28 MonitorSettingsRoundTrip checks.
- ConfigurationLifecycle failed compilation at Program.cs line 686 with CS0118 because its fixture used `Telegram` as an unqualified type name. No lifecycle cases executed; DecisionHistory did not run because the sequence stopped.
- Source review found the same constructor reference in the still-unrun DecisionHistory harness. Published `d331fbd059041241069646c3bb82ac6549423a70` fully qualifies both settings types as `Core.Main.DataObjects.PTMagicData.Telegram`; production source and the 272-group authored inventory are unchanged.
- The next local verification builds the pinned source and runs the two remaining harnesses. The complete twelve-project sequence remains in the handoff for a required full rerun. Earlier passes retain their actual source identity; configured runtime acceptance remains separate.
- [Exact-source evidence](updates/2026-11-07-193-check-validation.md) · [Current verification handoff](handoffs/2026-11-07-stabilization-correlation-validation.md).

## 2026-11-07 — Publish the follow-up fixes and record standing authorization

- Published the reviewed fixture and main-market corrections on `phase1/market-data-foundation`; the current handoff pins the published source. Native build, full harness execution, and configured runtime acceptance of these corrections remain pending.
- Recorded [D-038](DECISIONS.md#d-038--standing-authorization-to-publish-ptm-210-development): the user authorizes continued publication of PTM 2.10 development changes to the named application and documentation branches without renewed conversational approval. Actual tool restrictions remain binding; personal strategy and live PT actions remain outside this authorization.

## 2026-11-07 — Correct the volume-cap fixture and main-market bootstrap

- Replaced the invalid `double.MaxValue - 1` volume-cap fixture with 1,000 and added checks for the adjacent representable value and the exact sentinel. Production trigger validation is unchanged; the revised validator harness has 40 authored checks.
- Preserved default-file assignments when PAIRS/DCA/INDICATORS property groups are null. Main-market resolution now reads the exact property key, normalizes its asset code, and produces a clear configuration error before exchange I/O for missing or malformed values.
- Validated direct adapter inputs before network access, retained USDT identity pricing at 1 without a ticker call, and added the resolved main market and selected GlobalSetting to startup logging.
- Added ten lifecycle groups for property inheritance, main-market parsing, bootstrap/acknowledgement boundaries, owned-guard retention on invalid bootstrap, and adapter identity/invalid-input behavior. ConfigurationLifecycle now has 66 authored groups; the current total is **272 across twelve projects**.
- A new user-local build and complete regression run remain required for the published follow-up source. Runtime acceptance also requires restarting the updated configured instance and capturing its Source revision. [Current handoff](handoffs/2026-11-07-stabilization-correlation-validation.md).

## 2026-11-07 — Confirm the build and record partial regression results

- User-local validation identifies exact source `78967a7703ab9f57fece40d488fc538b1caf393b` and .NET SDK 10.0.403. Core, PTMagic, and Monitor built successfully in 9.6 seconds, confirming the Razor compilation correction.
- Eight harnesses completed with 125 passing checks. TriggerConfigurationValidation printed 23 PASS results, then failed case 24, “timed and volume off-triggers need no trend,” for OffTrigger #2 with an empty MarketTrend name.
- The fail-fast sequence stopped before MonitorSettingsRoundTrip, ConfigurationLifecycle, and DecisionHistory. Nullable warnings in two passing harnesses did not cause the failure. Full regression acceptance remains open.
- A separate runtime excerpt showed a Binance Futures ticker request with `symbol=USDT`, blank MainMarket, and an aborted raid. Its version 2.10.0 banner did not identify a source SHA; the runtime failure cannot be assigned to the exact-source build.
- [Build and partial regression evidence](updates/2026-11-07-build-and-partial-harness-validation.md) records the results and their limits. Follow-up fixes and a complete rerun remain required.

The two preparation entries below describe earlier checkpoints. This user-local run resolves their build-pending statements and records partial regression progress, while configured runtime acceptance remains open.

## 2026-11-07 — Correct Monitor Razor rendering after a reported build failure

- User-supplied build output shows Core net10.0 succeeded and Monitor failed with 27 Razor compile errors across nine row-render expressions. The log did not include an exact source SHA, so it is not exact-revision acceptance.
- Explicitly delimited `Html.Raw` expressions in `Monitor/Pages/_get/SettingsGlobalSettings.cshtml` and `Monitor/Pages/_get/SettingsSingleMarketSettings.cshtml` as `@(Html.Raw(...))`; the following `.map(...)` and `.join(...)` remain JavaScript.
- The corrected build and full regression rerun remain pending under D-021. No harness cases were added; the inventory remains 260 authored check groups across 12 projects.
- Updated the [current handoff](handoffs/2026-11-07-stabilization-correlation-validation.md) and [implementation evidence](updates/2026-11-07-stabilization-correlation-implementation.md) for the correction and required rerun.

## 2026-11-07 — Stabilization, correlation, history, and current-contract reconciliation

- Recorded source corrections for final SMS removal, desired/pending/confirmed delivery with retry, startup global SOM, Monitor row preservation, and structural reference validation.
- Replaced the initial unpublished startup-preset overlay at the user's direction with `POST /api/v2/globalSellOnlyMode` (`token`, `enabled` query parameters). Startup protection no longer sends PAIRS/DCA/INDICATORS; normal configuration delivery and global SOM release have separate acknowledgements.
- Added pinned acquisition-window and decision-age contracts, per-metric history requirements, the TrendMinutes Concentration ranking window, Phase 1D BTC correlation, and bounded native decision history.
- At this preparation checkpoint, the corrected application build, harness execution, and configured runtime acceptance were pending. Later results are recorded above.
- Consolidated one [current technical roadmap](roadmaps/CURRENT.md), [status](STATUS.md), [decision register](DECISIONS.md), and [verification handoff](handoffs/2026-11-07-stabilization-correlation-validation.md), retaining the full future derivatives, market-state, liquidity, and historical-analysis scope.
- Explicitly superseded the legacy/selective PriceTrend architecture, stale “next phase” instructions, removed harness instructions, and early-performance ordering. Dedicated performance work follows completion of **all approved new metrics**.
- Excluded independent personal strategy development from application scope and acceptance.
- Preserved earlier mutable current documents in [history](history/README.md) and left all original dated roadmap/handoff/update/issue files intact.
- [Implementation update](updates/2026-11-07-stabilization-correlation-implementation.md) · [Issue 003](issues/003-configuration-lifecycle-and-data-reliability.md).

The entries below are historical. An old statement that an automatic workflow remained present or that an obsolete roadmap was current describes that earlier date; use the current documents for active instructions.

## 2026-11-05 — Shorten the public 2.10 roadmap

- Condensed [ROADMAP.md](ROADMAP.md) without changing phase scope or implementation status.
- Retained completed features, pending compatibility/runtime verification, and planned Phase 1D–6 work.
- Documentation only; application code and test status unchanged.

## 2026-11-05 — Publish a concise user-facing PTMagic 2.10 roadmap

- Added [ROADMAP.md](ROADMAP.md): accessible summary of completed Phase 0/1A/1B/1C changes, unified PriceTrend/exchange cleanup still under validation, and upcoming Phase 1D–6 work.
- Separated implemented and locally/runtime-tested functionality from pending cross-exchange checks and longer-term planned features; no release date asserted.
- Linked the overview from the repository README. The technical roadmap, accepted decisions and STATUS remain authoritative.
- Documentation-only commit; no PTMagic source changes, builds or tests.

## 2026-11-04 — D-022: Mandatory copy-paste PowerShell test commands

- Accepted a recurring requirement to include an executable PowerShell script in every PTMagic development/testing handoff requiring local verification.
- Commands start with `git pull --ff-only` and `dotnet build`, followed by exact `.csproj` paths for relevant regression suites and any new tests; distinguish required versus optional test runs.
- Separate additional runtime/TestMode checks where applicable, and report pass/fail **only after reviewing the user's local output**.
- Updated README, handoff template and D-022 decision register. **Documentation-only change; no application code, build or tests run.**
## 2026-11-04 — D-021: Local testing and development responsibility policy

- Accepted explicit division of responsibility: assistant implements/reviews code and authors regression tests; user performs local builds, regression runs, and TestMode.
- Test failures, output, and runtime logs are reviewed jointly: user provides evidence and assistant corrects source defects.
- GitHub is for commits and roadmap/handoff tracking, **not automatic builds/tests unless specifically requested**.
- Updated authoritative roadmap, handoff template/procedure, repository README and decision register. Historical handoffs are preserved.
- **Existing application GitHub Actions workflow still exists** and requires separate removal/disablement to stop automatic runs.

## 2026-11-04 — Selective legacy Monitor hardening

- Completed follow-up source hardening through [`40e546c`](https://github.com/HojouFotytu/PTMagic/commit/40e546cb149bac0fca99e0aa257e7673453b7c8e).
- Old Market Analyzer absolute/relative rows preserve one correctly positioned blank cell per skipped legacy trend; relative values require a calculated global legacy average.
- Persisted old graph history is no longer shown for trends whose legacy averages were intentionally skipped. Current market prices/volumes are independently populated.
- **New build, 72/72 expected test run and TestMode verification are still pending.**

## 2026-11-04 — Selective legacy price-trend calculations (unverified source)

- Application [`1a6b9aa401fac74842e4d53ddbbfb2b2a4c5dc11`](https://github.com/HojouFotytu/PTMagic/commit/1a6b9aa401fac74842e4d53ddbbfb2b2a4c5dc11): only compute legacy asset/global PriceTrend for legacy-only trends or legacy trigger dependencies; normalized Metrics-only trends skip old historical price snapshots and mean.
- Frozen Phase0 eligible population now feeds normalized market/asset metric selection independently from legacy trend arrays, with current 24h volume ranking and configured MarketTrend selection filters.
- SMS price/24h-volume triggers and summary fields read current market snapshots even when there is no legacy trend; old Market Analyzer intentionally shows no value where legacy trend was skipped.
- Added 14-case selective-routing and population regression suite. **.NET build, 72-test full suite and TestMode not run yet.**
- [Implementation/update](updates/2026-11-04-selective-legacy-price-trend.md).

## 2026-11-04 — Close Phase 1C and authorize Phase 1D handoff

- Final user-supplied TestMode export has **8 freshly generated SMS snapshots (BTC 4, ETH 2, SOL 2) with 0 cross-setting trigger descriptions**, closing the SMS summary alias defect after code commit `0e8ab70`.
- Initial 14m21s cold-start raid had 39 transient incomplete-data warnings; later runs stabilized at two expected 8h history warnings. Ten RAID SUMMARY checkpoints, no ERROR/FATAL exceptions, no PT writes in TestMode, and stable GlobalSetting after flood protection.
- Earlier 58/58 deterministic test pass, live Phase1C metrics/trigger behavior and Monitor content evidence remain valid. **P1C-01–P1C-07: DONE**.
- Phase1D synchronized return correlation is **NEXT — not started**. Created [Phase 1D handoff](handoffs/2026-11-04-phase1d-correlation-ready.md) and [final Phase1C evidence record](updates/2026-11-04-phase1c-final-closeout.md).

## 2026-11-04 — Post-fix SMS TestMode uses retained historical snapshots

- New 19:05–19:07 TestMode log: analyzer and triggers healthy; previous saved SMS entries still contain 6 BTC, 1 ETH, 1 SOL foreign descriptions.
- All eight SMS activation timestamps remain 18:32 KST with `RefreshOffTriggers=false`: the original snapshots were reserialized, not regenerated.
- **Not evidence of a failed source fix**; focused fresh-snapshot test remains pending. See [evidence record](updates/2026-11-04-sms-postfix-retained-snapshots.md).

## 2026-11-04 — Verify SMS summary isolation fix (58/58 tests)

- User-run `git pull --ff-only` already up to date at application fix commit `0e8ab70`; `dotnet build` succeeded in **5.9s** for Core/PTMagic/Monitor (.NET 10).
- New SMS summary isolation suite **5/5 passed**; existing Phase1COhlcv **13/13**, warning **7/7**, trigger **29/29**, readiness **4/4**: **58/58 passed**.
- The SMS summary alias defect is now build/unit-test verified; deployed TestMode multi-SMS JSON export verification remains pending.
- [Verification record](updates/2026-11-04-sms-summary-test-verification.md).

## 2026-11-04 — Fix SMS summary matched-trigger list aliasing

- Isolated market-level PT comment aggregation from persisted per-setting SMS trigger descriptions using defensive copies.
- Added five deterministic regression checks, including JSON snapshot round-trip and cross-market isolation.
- Application commit [`0e8ab70`](https://github.com/HojouFotytu/PTMagic/commit/0e8ab7056d32f16d1095a519ac4a1e87a29a4188); **build, tests and TestMode revalidation pending**.
- No change to metric computation, trigger logic or PT settings behavior.
- [Dated update](updates/2026-11-04-sms-summary-alias-fix.md).

## 2026-11-04 — Phase 1C build and tests verified

- User-run application .NET 10 build succeeded in 14.8s at `64d063c`.
- Phase1COhlcv 13/13, metric warnings 7/7, tri-state triggers 29/29, Phase1A 4/4: **53/53 passed**.
- TestMode raid and Monitor/export acceptance remain pending; Phase 1C not yet closed.

# PTMagic 2.10 — Roadmap Revision History

This log tracks **roadmap and documentation changes**, not software releases. Software implementation claims require evidence in STATUS.md and dated update notes.

## 2026-11-04 — Phase 1C source implementation (P1C-01 through P1C-07)

- Implemented complete UTC-aligned MarketTrend-duration OHLCV aggregation, Wilder ATRP and quote-volume expansion.
- Added market-wide medians, volatility/volume breadth, HHI concentration, TopN/BTC/BTC+ETH volume shares, and configurable per-trend parameters.
- Integrated metric registry, normalized trigger unit labels, Monitor table/tooltip and snapshot export; fixed simple AND/OR GlobalSettings with omitted trigger tags.
- Added 13 synthetic Phase1COhlcv test cases; **build, tests and TestMode pending**.
- Current application source HEAD [`64d063c`](https://github.com/HojouFotytu/PTMagic/commit/64d063c1c9bc8886fb456cae97921780449f5cce). [Implementation update](updates/2026-11-04-phase1c-source-implementation.md) / [verification handoff](handoffs/2026-11-04-phase1c-implementation-verification.md).

## 2026-11-04 — Verify all RAID SUMMARY metric warnings display

- User-run `git pull --ff-only`: already up to date at application HEAD `64e05e7`.
- `dotnet build` succeeded for Core/PTMagic/Monitor in 14.1s; metric-warning regression harness passed **7/7**.
- All-distinct-warnings display behavior is build/unit-test verified; end-to-end TestMode log output remains pending.
- [Verification record](updates/2026-11-04-all-metric-warnings-verified.md).

## 2026-11-04 — Remove RAID SUMMARY metric warning display cap

- Show all distinct grouped metric warnings; remove `... and N more` truncation.
- Updated seven-case deterministic test harness to check all nine synthetic warnings are displayed.
- Application commit [`64e05e7`](https://github.com/HojouFotytu/PTMagic/commit/64e05e7e2a93aa23828890ef5e4708f002c696b8); build/TestMode checks pending.
- Amends D-018; earlier five-detail cap was superseded by user request. [Dated update](updates/2026-11-04-all-metric-warnings.md).

## 2026-11-04 — Add optional cross-raid historical snapshot reuse optimization

- Added roadmap §12.7 and tracked task `P1-PERF-SNAPSHOT`.
- Proposed reusing unchanged immutable per-market historical snapshots across raids, avoiding redundant candle-array copying, sorting and gap validation.
- Requires correct invalidation on data changes and fresh per-raid as-of/staleness evaluation; benchmark CPU, allocations and retained-history performance.
- **Future optimization only**: no application source changes, no performance improvement claimed. [Dated update](updates/2026-11-04-snapshot-reuse-optimization.md).

## 2026-11-04 — Validate D-018 compact raid warnings

- User-run application `dotnet build` passed in 15.2s at `34c30aa`.
- Metric warning tests **7/7 passed**, tri-state trigger tests **29/29 passed**, Phase1A readiness tests **4/4 passed** — **40/40 total**.
- Actual TestMode raid summary output still unverified; the earlier “testing pending” status is historical.
- [Verification update](updates/2026-11-04-raid-metric-warnings-verification.md).

## 2026-11-04 — Compact metric-warning section in RAID SUMMARY (D-018)

- Implemented grouped unavailable metric warnings in the existing analyzer RAID SUMMARY (up to five details, then overflow).
- Consolidated GlobalSetting/SMS normalized trigger warnings and surfaced active GlobalSetting retention when selection is indeterminate.
- Added seven deterministic formatter checks; **build, tests and TestMode raid remain unverified**.
- Code commit [`34c30aa`](https://github.com/HojouFotytu/PTMagic/commit/34c30aa08918252d2976d6fabd7dddb1589acfd9); [dated update](updates/2026-11-04-raid-metric-warnings.md).
- No change to D-017 tri-state logic, D-016 MarketTrend timeframes or Phase 1C implementation status.

## 2026-11-04 — Verify tri-state regression harness after CS0121 fix

- User reports `git pull --ff-only` “Already up to date” against latest source branch HEAD `c66b9f3`.
- `dotnet build` succeeded for Core, PTMagic and Monitor (.NET 10); **15.1s**.
- Independent test projects: **Phase1TriggerLogic 29/29**, **Phase1AReadiness 4/4**, 33 tests total.
- D-017 is build- and deterministic-test verified; no end-to-end TestMode validation yet. P1C-01 still next.
- Evidence: [dated test update](updates/2026-11-04-tristate-test-results.md).

## 2026-11-04 — Fix regression harness compilation ambiguity

- User-run `dotnet build`: Core/PTMagic/Monitor succeeded; separate `Tests/Phase1TriggerLogic` compilation failed with 13 CS0121 ambiguous constructor overloads. Existing Phase1AReadiness tests passed (4/4).
- Fixed the 13 ambiguous target-typed `new()` dictionary arguments with explicit `new Dictionary<string, TriggerTruthValue>`.
- Application commit [`c66b9f3`](https://github.com/HojouFotytu/PTMagic/commit/c66b9f3a2572b0bd9ebf1c737bd98b4f9f8e6953).
- Trigger tests and TestMode verification still pending: the assistant has no local .NET SDK.

## 2026-11-04 — Tri-state trigger evaluation refinement (D-017)

- Accepted complete-expression semantics for unavailable normalized metrics: `true OR unavailable` activates; a final indeterminate expression does not.
- Applied the same evaluator to GlobalSetting, SMS and SMS OffTrigger source paths, plus 29 deterministic test cases.
- Code commits `eeffc05`, `9f18095`; **verification pending** (SDK unavailable to assistant).
- Updated decision register and status; archived a [dated update](updates/2026-11-04-three-valued-trigger-logic.md) and [verification handoff](handoffs/2026-11-04-tristate-trigger-logic-verification.md).
- No change to completed Phase 1A containment or to Phase 1C MarketTrend timeframe D-016.

## 2026-11-04 — Correct Phase 1C/1D metric timeframe inheritance (D-016)

- **User decision:** all derived metric analytical timeframes are determined by each `MarketTrend.TrendMinutes`; normalized 5m candles are storage/input resolution, not a fixed metric period.
- **Previously incorrect:** `ATRP5m`, `MedianATRP5m`, separate 15m quote-volume metrics and roadmap language allowing independent metric intervals.
- **Corrected:** trend-duration `ATRP`/`MedianATRP`, aligned complete trend-sized ATR, volume, volatility breadth, concentration and correlation windows; explicit retention requirements for ATR(14); fail-closed unsupported/missing periods.
- **Existing exception:** Phase 1B return `Concentration` still ranks Top10 by fixed trailing 24h quote volume. A separate compatibility-sensitive tested code change is needed to meet the universal D-016 rule.
- **Documents:** added [new authoritative roadmap](roadmaps/revised-2.10-2026-11-04-markettrend-timeframe.txt) and [superseding handoff](handoffs/2026-11-04-phase-1c-markettrend-timeframe-correction.md); updated README, STATUS and DECISIONS; preserved previous roadmap and handoffs unchanged as historical records.
- **Source verification:** branch `phase1/market-data-foundation` HEAD `89324bc5c8c5ea19ceb543b6ab5130899f2675dc`. **No application code, build or runtime validation is claimed for this documentation-only correction.** See [dated update](updates/2026-11-04-phase-1c-timeframe-correction.md).

## 2026-11-04 — Close Phase 1A readiness and hand off Phase 1C

- **Code branch:** `HojouFotytu/PTMagic:phase1/market-data-foundation`, latest inspected HEAD `89324bc5c8c5ea19ceb543b6ab5130899f2675dc`.
- **Previous status:** Phase 1A [PARTIAL], P1A-READY blocking, Phase 1C deferred; original roadmap and earlier handoff record that historical state.
- **New accepted status:** Phase 1A **DONE — CONTAINED**, issue 001 closed for progression, Phase 1C **NEXT**, starting `ATRP5m` and `MedianATRP5m`.
- **Implementation:** `3a2ba02` (90% exact eligible-population global coverage, 100% Concentration exception, diagnostic fields), `c038a11` (normalized GlobalSetting/SMS fail-closed safeguards), `e002801` (deterministic tests), `11d6e28` (switch vs reapply raid-summary log wording).
- **Verification:** user-reported net10.0 build for Core/PTMagic/Monitor successful, 4/4 deterministic tests passed. Live TestMode first raid 32/250 global aligned returns rejected; next normal raid recovered 249/249; third raid zero normalized kline requests; standard GlobalSetting switch after flood protection, subsequent stable raids.
- **Explicit limitation:** this is containment, not a proven fix of the exact ingest/candle-boundary root cause. Holding a non-default setting across subsequent coverage failure and new log-field runtime verification remain non-blocking Phase 1E checks.
- **Documentation:** updated [roadmap](roadmaps/revised-2.10-2026-11-04.txt), [STATUS](STATUS.md), [DECISIONS](DECISIONS.md), [issue 001](issues/001-cold-start-readiness.md); added [dated closeout update](updates/2026-11-04-phase-1a-closeout.md) and [standalone Phase 1C handoff](handoffs/2026-11-04-phase-1c-ready.md). Original historical handoff retained.

## 2026-11-04 — Documentation tracker initialized

- Established tracking under `docs/roadmaps/2.10/` on `phase1/market-data-foundation` in `HojouFotytu/PTMagic`.
- Preserved the original market-analysis roadmap, 2026-11-04 2.9.1-labeled revision and revised **2.10** authoritative roadmap as separate documents.
- Preserved the completed Phase 0 audit.
- Added task-level status, known issues, decisions, date-stamped updates and a session-handoff archive.
- Accepted the clarified release boundary: 2.9 completed; Phase 0–6 market analytics belongs to 2.10.
- Set P1A-READY as the blocking initial-raid correctness issue. Root cause is unverified.
- No application source code changes were made as part of this documentation initialization.

See [2026-11-04 initial import](updates/2026-11-04-initial-import.md).

## Policy for later revisions

Every substantive change must record date, source branch + commit, impacted task IDs, previous wording, new wording, reason/evidence, accepted or proposed status, and tests when applicable. Historical handoffs and the original roadmap remain immutable.
