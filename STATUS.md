# PTMagic 2.10 — Current Development Status

## 2026-11-04 — Verbose metric warnings: four-raid Binance Futures TestMode verified

**Application source branch HEAD inspected:** [`efa7b5f`](https://github.com/HojouFotytu/PTMagic/commit/efa7b5ff1a99606395c1b1b9636c828600a55353). Uploaded runtime identifies version 2.10.0 but not Git SHA; new diagnostic strings confirm the implementation is running.

**User local TestMode log (23:19–23:24 KST):** four analyzer raids; metric warning groups **31 → 7 → 7 → 7**; zero ERROR/FATAL; all raids report **no PT configuration updates**. First cold raid (2m) had 142/250 valid global returns and 296/519 valid asset returns due 223 missing latest 5-minute closed endpoints, despite 756/756 successful fetches and 872,424 candles. Data refreshed on the next raid (373/756 updated, 1,119 candles), then recovered to **250/250 global and 519/519 asset** coverage. Following two raids needed no Binance candle requests.

**New warning trace confirmed:** `FILTERED_1h / PriceTrend` originated in SMS activation setting `DIAG_SMS_SOL_FilteredOut`, market `SOLUSDT`, trigger #1, explicit PriceTrend, relation Absolute. This market is explicitly excluded by `IgnoredMarkets="SOL"`. Remaining six groups: asset-only `ATRP` used in a GlobalSetting, explicit `PriceTrend` not enabled on IMPLICIT_1h, and four intentionally insufficient 8h ATRP/volume metrics. Warning source, setting, symbol, relation, reason, counts and coverage diagnostics are operational.

**Export checks:** `MarketTrendAnalytics(6).json` captured second raid at 14:22:14 UTC; eight MarketTrends, all intended fully funded PriceTrend values valid; DEFAULT_1h vs IMPLICIT_1h and BLANK_2h vs FULL_2h match exactly over 519 assets. All **3,116** valid per-asset PriceTrend values match `LastRuntimeSummary(6).json`. Thirteen SMS snapshots across BTC/ETH/SOL, zero cross-setting descriptions; ten activation timestamps from the second raid, three retained historical snapshots. GlobalSetting was initially Default (second raid flood-protected), switched to `DIAG_Global_All15AndImplicit` in third raid, and remained unchanged/reapplication-free in fourth.

**Follow-up issue (new):** Cold startup exchange polling spanned the 14:20 UTC 5m candle close; metrics used `DateTimeOffset.UtcNow` after refresh and demanded the newly closed candle even for symbols fetched before the boundary. This appears to explain temporary false data-coverage gating. Review synchronization of refresh snapshot time and evaluation as-of time, or targeted refresh after boundary. **Hypothesized root cause based on timing and code inspection; not yet patched or regression-tested.** Do not mark cross-boundary consistency fixed.

**Status:** Verbose diagnostic *runtime behavior* verified on Futures. No user-supplied `dotnet build` or 75/75 local harness output, so local build/test status remains **unverified**. Binance Spot and Binance US remain pending. [Detailed findings](updates/2026-11-04-verbose-warning-four-raid-testmode.md).


## 2026-11-04 — Diagnostic expansion for all normalized metric warnings (unverified source)

Application commit: [`efa7b5f`](https://github.com/HojouFotytu/PTMagic/commit/efa7b5ff1a99606395c1b1b9636c828600a55353), branch `phase1/market-data-foundation`.

- Expanded the end-of-raid grouped metric-warning collector. Each trend/metric group now retains total failed requests, distinct requested markets, source counts and reason categories, plus up to five concrete trigger examples with setting name, market, tag/index, relation, implicit/explicit metric and resolver reason.
- Invalid global metric snapshots now include validation flags, sample/eligible counts, coverage, endpoint and invalid reason. Asset-wide failures report grouped reasons, counts and example markets; expected endpoint and global/asset population sizes are included.
- A missing per-asset value distinguishes intentionally ignored markets, markets outside AllowedMarkets, markets absent from the eligible selection and missing published metric values. The `FILTERED_1h / PriceTrend` warning should identify the requesting SMS/market on the next local TestMode run.
- Coverage now includes Binance Futures, Binance Spot and Binance US; metrics and trigger truth logic were not intentionally changed.
- Added **five** deterministic warning tests, raising expected test count from **70 to 75** across the existing six harnesses. **NO new local build/tests/TestMode run yet**. Do not mark this change verified until user supplies results.
- Removed the previously added automatic GitHub Actions workflow under accepted D-021 local-testing responsibilities.
- Prior Binance Futures three-raid acceptance still applies to prior source, not this new diagnostics commit.

[Detailed implementation record](updates/2026-11-04-verbose-metric-warning-diagnostics.md). Phase 1D remains unstarted.


## 2026-11-04 — Unified normalized PriceTrend migration: Binance Futures TestMode verified

**Latest application branch HEAD checked:** [`8ff8c87`](https://github.com/HojouFotytu/PTMagic/commit/8ff8c87900aa6f56c8721444dd11f0885c99ac3d). Latest uploaded running binary says version 2.10.0 but does not embed git SHA.

**Earlier offline build/test result:** .NET 10 Release build succeeded and all **70/70 deterministic tests** passed in GitHub Actions run [41836826883](https://github.com/HojouFotytu/PTMagic/actions/runs/41836826883), before local-testing policy D-021. The present upload is runtime TestMode evidence, not another local build report.

**User-run Binance Futures TestMode (22:47–22:51 KST):** Three raids, 756 fetched markets / 519 eligible COIN, eight configured normalized MarketTrends, correct omitted/blank/default and implicit PriceTrend, global setting 15 explicit + 3 implicit checks matched; no PT writes; no ERROR/FATAL. All **3,116** per-asset PriceTrend fields in LastRuntimeSummary match MarketTrendAnalytics exactly. **13 SMS snapshots, 0 foreign descriptions**, 10 freshly activated. The GlobalSetting remained active without switch or reapplication on raids 2 and 3.

**Warning handling:** Four intentionally insufficient 8h metrics correctly unavailable, asset-only ATRP rejected in a global trigger, explicit disabled PriceTrend rejected, and FILTERED_1h uncalculated-value warning requires diagnostic trigger attribution. No confirmed source defect.

**Status:** Unified migration's Binance Futures TestMode portion **VERIFIED**; overall three-exchange acceptance **PARTIAL (1/3)**. Binance Spot and Binance US TestMode, browser Monitor rendering, Fiat conversion parity, and positive OffTrigger deactivation are **NOT VERIFIED**. Phase1D not started by this follow-up. [Full evidence](updates/2026-11-04-unified-pricetrend-futures-testmode.md) · [New handoff](handoffs/2026-11-04-unified-pricetrend-validation-handoff.md).


**As of:** 2026-11-04 — **PHASE 1C DONE** (build + 58/58 deterministic tests + deployed TestMode + Monitor content + fresh SMS isolation confirmed); **Phase 1D NEXT**. D-016 timeframe rule applies.
**Source:** [HojouFotytu/PTMagic](https://github.com/HojouFotytu/PTMagic), `phase1/market-data-foundation`.
**Latest application code HEAD verified:** [`0e8ab7056d32f16d1095a519ac4a1e87a29a4188`](https://github.com/HojouFotytu/PTMagic/commit/0e8ab7056d32f16d1095a519ac4a1e87a29a4188) on `phase1/market-data-foundation` (2026-11-04; recheck before development).

| ID | Deliverable | Status | Evidence / next step |
|---|---|---|---|
| P0-AUDIT | Architecture audit | DONE | [Audit](audits/phase-0-architecture-audit.txt) |
| P1A-STORE | Shared normalized 5m OHLCV, incremental ingestion and Phase 0 universe | DONE | Cold-start, cleanup and idle raids verified |
| P1A-READY | Cold-start coverage, fail-closed normalized metrics and settings safeguard | **DONE — CONTAINED** | [Issue 001](issues/001-cold-start-readiness.md) closed; root cause not proven |
| P1B-RET | PriceTrend / MedianPriceTrend / MeanMedianSpread | DONE | Runtime exercised |
| P1B-BREADTH | Breadth / Dispersion | DONE | Coverage gated |
| P1B-RS | RelativeStrengthMarket / RelativeStrengthBTC | DONE | Scope preserved |
| P1B-CONC | Top10 return advantage Concentration | DONE | Current ranking uses fixed trailing 24h quote volume; 100% required |
| P1B-CONC-WINDOW | Align existing concentration-ranking window with MarketTrend.TrendMinutes | FOLLOW-UP | Known current 24h fixed-window exception; separate compatible code change/test |
| P1C-01 | Per-asset ATRP on MarketTrend.TrendMinutes candles | **DONE** | Source `64d063c`; .NET 10 build, 58/58 tests, deployed TestMode and Monitor content verified |
| P1C-02 | MedianATRP on the same configured MarketTrend timeframe | **DONE** | Source `64d063c`; .NET 10 build, 58/58 tests, deployed TestMode and Monitor content verified |
| P1C-03 | Volatility breadth | **DONE** | Source `64d063c`; .NET 10 build, 58/58 tests, deployed TestMode and Monitor content verified |
| P1C-04 | Recent quote-volume expansion | **DONE** | Source `64d063c`; .NET 10 build, 58/58 tests, deployed TestMode and Monitor content verified |
| P1C-05 | Volume-expansion breadth | **DONE** | Source `64d063c`; .NET 10 build, 58/58 tests, deployed TestMode and Monitor content verified |
| P1C-06 | Volume concentration | **DONE** | Source `64d063c`; .NET 10 build, 58/58 tests, deployed TestMode and Monitor content verified |
| P1C-07 | Registry/Monitor/trigger/test integration | **DONE** | Source `64d063c`; .NET 10 build, 58/58 tests, deployed TestMode and Monitor content verified; SMS snapshot fix `0e8ab70` live-confirmed |
| P1-COMPAT-LEGACY-SELECTIVE | Skip unneeded legacy price-trend calculations for explicit Metrics | **CODE COMMITTED — BUILD/TESTMODE PENDING** | 14 new deterministic fixtures; preserve implicit legacy trigger and market quote volume/price; Phase 1C remains verified at previous baseline |
| P1-PERF-SNAPSHOT | Reuse unchanged historical snapshots between raids | **OPTION / PLANNED** | Avoid redundant full-series copy/sort/gap validation; preserve invalidation, staleness and thread safety; benchmark before/after (roadmap §12.7) |
| P1D-CORR | Synchronized return correlation | **NEXT — NOT STARTED** | Use synchronized complete MarketTrend.TrendMinutes return vectors; define invalidity, minimum sample count, statistics and test plan in Phase1D handoff |
| P1E-INSPECT | Inspection and additional fault tests | PARTIAL | Carry non-blocking checks below |
| P2-RAW | Futures funding/OI/positioning/flow ingestion | PLANNED | Later |
| P2B-AGG | Futures market-wide aggregation | PLANNED | Later |
| P3-STATE | Deterministic higher-order states | PLANNED | Later |
| P4-TRIG | GlobalSetting / SMS / OffTrigger normalized metric routing | **PHASE 1B/1C TRIGGER ROUTING VERIFIED** | 29/29 tri-state tests; deployed GlobalSetting and BTC/ETH/SOL diagnostic SMS/OffTrigger TestMode checks; later phase integration remains scheduled |
| P5-LIQ | Liquidity/depth/stress | PLANNED | Later |
| P6-HIST | Feature history and validation | PLANNED | Later |

## CURRENT: Phase 1C accepted and closed — 2026-11-04

**Acceptance:** All Phase1C tasks P1C-01–P1C-07 **DONE**. Source `64d063c`, SMS snapshot-list isolation fix `0e8ab70`, user-run .NET 10 build passed, all five test suites **58/58**, Binance Futures Phase1C TestMode analytics/triggers, Monitor Market Metrics content, and final fresh SMS export isolation.

**Final uploaded evidence (19:10–19:33 KST):** `2026-11-04(3).txt`, `LastRuntimeSummary(4).json`, `MarketTrendAnalytics(4).json`, `SingleMarketSettingSummary(4).json`. The latter contains **8 fresh SMS summaries**, activation timestamps **19:25:12–19:26:09 KST**, across BTCUSDT (4), ETHUSDT (2), SOLUSDT (2). Every snapshot's `MatchedTriggersContent` contains **zero descriptions from other settings**: **0/8 contaminated**. New snapshots were created after the fix, rather than simply reserializing the 18:32 historical data. This closes **P1C-SMS-SNAPSHOT-ALIAS**. Multiple active settings per market remain supported.

**10 RAID SUMMARY checkpoints:** First cold-start raid took 14m21s with transient readiness warnings (39 distinct) as historical observations were still being recovered. Second raid had only the **two expected 8h MedianATRP and MedianVolumeExpansion** insufficient-history warnings with `StoreDataMaxHours=96`. Subsequent raids retained exactly those two warnings; later steady-state raids took 1s. No ERROR/FATAL exceptions found in the supplied log. GlobalSetting `DIAG_Global_P1C_All15Global` became active after flood-protection conditions cleared; later raids showed no reapplication. `TESTMODE` prevented outbound PT configuration updates.

**Scope distinction:** This completes the agreed Phase1C functionality and live acceptance, not every optional feature from Phase1E or later phases. Previous notes below are historical observations superseded by this status. **Phase 1D is next**, not yet implemented. [Final evidence](updates/2026-11-04-phase1c-final-closeout.md) · [Phase1D handoff](handoffs/2026-11-04-phase1d-correlation-ready.md).

## Phase 1A closeout

**Code commits:** `3a2ba02` (90% global gate, 100% Concentration exception, coverage metadata and diagnostics); `c038a11` (unavailable normalized triggers fail closed, active GlobalSetting held on indeterminate fallback, SMS negation protection); `e002801` (four deterministic tests); `11d6e28` (raid summary distinguishes GlobalSetting switch from same-setting reapplication). All appear in the latest inspected branch.

**User-run tests:** `dotnet build` succeeded for Core/PTMagic/Monitor on .NET 10. `dotnet run --project Tests/Phase1AReadiness/Phase1AReadiness.csproj`: **4 tests passed**.

**User-supplied Binance Futures TestMode:** First raid fetched 756/756 normalized series (654,696 candles), but 4h global coverage was 32/250 (12.8%), with 218 MissingEndpoint; all dependent global features were unavailable and GlobalSetting triggers rejected. Second raid incrementally fetched 2,115 candles for 705 markets, recovered global coverage 249/249 and asset metrics 1,434/1,434. Third raid required **zero** normalized kline requests. After flood protection, `Default` switched to `DIAG_Global_AllMetrics` at 13:33 KST, with subsequent stable operation. Five-minute boundary raids downloaded ~2,268 incremental candles. TestMode sent no settings to PT.

**Policy:** Exact eligible GlobalSetting trend population is denominator; required valid count `ceil(0.9 * eligible)`, nonempty population. Existing `Concentration` requires 100% quote-volume-ranked population. Invalid, missing and stale metrics never substitute zero. Independent valid and legacy triggers may still operate; no forced cleanup raid, ingestion redesign or trading suspension.

**Root cause distinction:** A long cold-start fetch crossing 5m candle boundaries is plausible, **not proved**. The defect's *consequences* are contained and normal scheduled refresh repairs incompleteness. This is why P1A-READY is closed; it is not a claim that the first raid always has full data.

**Non-blocking follow-ups (P1E):** Verify retention of an already-active non-default GlobalSetting when coverage later falls below 90%; validate the revised raid summary wording in a new build/runtime; further partial-coverage, stale, sparse and boundary fault tests. The logs preceding the summary patch still say `Global setting changed`. Tested executable reported 2.9.1, whereas active product roadmap is 2.10.

## Accepted metric timeframe rule (D-016)

All derived metric analysis timeframes come from the configured `MarketTrend.TrendMinutes`. Normalized 5m is the source-data resolution only. P1C-01 `ATRP` and P1C-02 `MedianATRP` use complete, UTC-aligned trend-sized candles; 5m-fixed ATR/15m-fixed participation metrics are not valid Phase 1C designs. ATR(14) needs at least 15 complete trend candles; if `StoreDataMaxHours` is too short, metric is unavailable. This decision is **implemented in the Phase 1C metrics**; the text above records the original design rationale. Existing return `Concentration` still uses fixed trailing 24h ranking and is recorded as a separate follow-up.

**Current next phase:** [Phase 1D correlation handoff](handoffs/2026-11-04-phase1d-correlation-ready.md). The earlier Phase 1C handoff is retained as historical context.

## 2026-11-04 trigger-logic refinement: code committed, not yet tested

The user clarified that an unavailable normalized metric must be **unknown**, not a blanket veto. A fully evaluable `true OR unknown` is true, `false AND unknown` is false, and negated unknown remains unknown. This applies to GlobalSetting activation, SMS activation, and SMS OffTriggers. A final unknown result never activates/deactivates a setting. For GlobalSetting selection, only *indeterminate* candidate expressions contribute to the existing active-setting retention condition; valid independent matching candidates remain eligible. An already-active long-term SMS may continue under existing OffTrigger persistence semantics.

Source commits: [`eeffc05`](https://github.com/HojouFotytu/PTMagic/commit/eeffc05d0146ac31f355db31881250d9f93cfbc5) (new shared evaluator and 29-case harness), [`9f18095`](https://github.com/HojouFotytu/PTMagic/commit/9f180952db853659cd94c7b2a26341f972b47fca) (global/SMS/off-trigger integration).

**Evidence level:** Code inspected / committed. No C# build or executable tests performed by the assistant: `.NET` SDK unavailable in execution environment. User or CI must run `dotnet build`, `dotnet run --project Tests/Phase1TriggerLogic/Phase1TriggerLogic.csproj`, existing `Tests/Phase1AReadiness`, and TestMode raids before declaring runtime completion. Phase 1C ATRP remains unimplemented.

**Compatibility follow-up commit:** [`fbc4b35`](https://github.com/HojouFotytu/PTMagic/commit/fbc4b35bdd65abcf1252cbcf99e7d2aa8c10ac3b) preserves the existing AND/OR-only `OffTriggerConnection` contract (unsupported connection strings do not deactivate SMS). Latest application HEAD: `fbc4b35bdd65abcf1252cbcf99e7d2aa8c10ac3b`. Build and runtime tests still pending.

**Follow-up 2026-11-04 build evidence:** User reported `dotnet build` succeeded for Core/PTMagic/Monitor (14.1s), and `Phase1AReadiness` reported 4 passed. The separate `Phase1TriggerLogic` test project failed compilation with 13 CS0121 overload ambiguities from target-typed `new()` dictionary literals. Application branch commit [`c66b9f3`](https://github.com/HojouFotytu/PTMagic/commit/c66b9f3a2572b0bd9ebf1c737bd98b4f9f8e6953) replaces all 13 with explicit `new Dictionary<string, TriggerTruthValue>`. **Rebuild and execution of the trigger test project remain pending**; do not record the 29 tests as passed. Latest verified application branch HEAD: `c66b9f3a2572b0bd9ebf1c737bd98b4f9f8e6953`.

## 2026-11-04 D-017 post-fix verification (user-executed)

Against application branch `phase1/market-data-foundation` at verified remote HEAD `c66b9f3a2572b0bd9ebf1c737bd98b4f9f8e6953`, user reported `git pull --ff-only` returned “Already up to date”; `dotnet build` succeeded in 15.1s (Core net10.0 3.5s; PTMagic 0.7s; Monitor 9.4s). `dotnet run --project Tests/Phase1TriggerLogic/Phase1TriggerLogic.csproj` reported **29 tests passed** and `Tests/Phase1AReadiness/Phase1AReadiness.csproj` reported **4 tests passed**. Total **33 deterministic tests passed**. This closes the reported CS0121 test-harness compilation blocker.

**Evidence boundary:** No new TestMode raid has been provided to validate end-to-end settings switching, SMS activation or OffTrigger persistence. D-017 is build/deterministic-test verified, not yet runtime-verified. Phase 1A remains DONE—CONTAINED; P1C-01 ATRP is still NEXT. See [dated verification update](updates/2026-11-04-tristate-test-results.md).

## 2026-11-04 — Compact raid metric warnings (source committed; tests pending)

Source branch `HojouFotytu/PTMagic:phase1/market-data-foundation` commit [`34c30aa`](https://github.com/HojouFotytu/PTMagic/commit/34c30aa08918252d2976d6fabd7dddb1589acfd9) implements a **Metric warnings** section inside the existing RAID SUMMARY for Binance Futures. It groups invalid global/asset metrics and unresolved normalized trigger references by MarketTrend + metric; limits detail output to five lines with an overflow count; surfaces indeterminate GlobalSetting retention; and moves repetitive normalized trigger warnings from inline logs to the summary. It has **no changes to tri-state evaluation or PT settings execution**.

Seven new deterministic checks under `Tests/Phase1MetricWarnings` were added, but no build or test was executed in the assistant environment (no .NET SDK). Verify with `dotnet build`, `dotnet run --project Tests/Phase1MetricWarnings/Phase1MetricWarnings.csproj`, existing tri-state/readiness tests, and a TestMode raid. This does not implement P1C-01 ATRP, and does not yet add Monitor dashboard alerts.

## 2026-11-04 — D-018 deterministic verification passed

User-executed `git pull --ff-only` fast-forwarded `c66b9f3` to application HEAD `34c30aa08918252d2976d6fabd7dddb1589acfd9`. `dotnet build` succeeded in 15.2s (Core .NET 10, PTMagic .NET 10, Monitor .NET 10). `Tests/Phase1MetricWarnings` passed **7/7**, `Tests/Phase1TriggerLogic` passed **29/29**, and `Tests/Phase1AReadiness` passed **4/4**, totaling **40/40 deterministic tests passed**. The compact raid-summary diagnostic implementation is **build/unit-test verified**, but live TestMode RAID SUMMARY output and notification behavior are **not yet runtime-verified**. Phase 1C-01 ATRP remains next. See [verification update](updates/2026-11-04-raid-metric-warnings-verification.md).

## 2026-11-04 — D-018 warning output cap removed

Application commit [`64e05e7`](https://github.com/HojouFotytu/PTMagic/commit/64e05e7e2a93aa23828890ef5e4708f002c696b8) removes the previous five-detail limit and `... and N more` indicator. The RAID SUMMARY now lists **every distinct** MarketTrend/metric warning, retaining duplicate grouping and deterministic sorting. The seven-case `Phase1MetricWarnings` harness was updated to check all nine synthetic warning rows. **Code committed; build/TestMode re-verification pending.** This supersedes the earlier five-detail cap in D-018. No change to metric validity or trigger behavior.

## 2026-11-04 — All metric warnings display: build and regression verified

User-run `git pull --ff-only` returned **Already up to date** at application branch HEAD `64e05e7e2a93aa23828890ef5e4708f002c696b8`. `dotnet build` succeeded in **14.1s** (Core net10.0 3.3s, PTMagic net10.0 0.7s, Monitor net10.0 8.6s). `dotnet run --project Tests/Phase1MetricWarnings/Phase1MetricWarnings.csproj` reported **7 tests passed**, including the new all-warnings display check. **D-018 amendment: BUILD / DETERMINISTIC TESTS PASSED.** A live TestMode RAID SUMMARY showing all distinct warnings remains unverified. [Verification record](updates/2026-11-04-all-metric-warnings-verified.md).

## 2026-11-04 — Phase 1C source implementation checkpoint

Application branch HEAD: [`64d063c`](https://github.com/HojouFotytu/PTMagic/commit/64d063c1c9bc8886fb456cae97921780449f5cce). **P1C-01 through P1C-07 code authored and committed**: trend-sized OHLCV, Wilder ATRP, cross-sectional medians/breadth, quote-volume expansion, HHI/share concentration, metric registry, configuration, triggers, Monitor and a 13-case regression harness. Separate D-017 refinement fixes untagged AND/OR GlobalSetting evaluation as part of this integration.

**Not verified:** This assistant environment has no .NET SDK; no new `dotnet build`, test execution or TestMode evidence for Phase1C. Status is **CODE IMPLEMENTED — BUILD/TEST/TESTMODE PENDING**, NOT Phase1C DONE. The prior 40/40 passing Phase1A/tri-state/metric-warning results predate the Phase1C changes; rerun them. See [dated update](updates/2026-11-04-phase1c-source-implementation.md) and [verification handoff](handoffs/2026-11-04-phase1c-implementation-verification.md).

## Phase 1C build and deterministic test verification — 2026-11-04

At source HEAD `64d063c1c9bc8886fb456cae97921780449f5cce`, user reported `git pull --ff-only` already up to date, and `dotnet build` succeeded in 14.8s for Core, PTMagic and Monitor (.NET 10). Phase1COhlcv passed **13/13**, Phase1MetricWarnings **7/7**, Phase1TriggerLogic **29/29**, Phase1AReadiness **4/4**, total **53/53 tests passed**. The Phase 1C source is implemented and build/deterministic-test verified. **Not yet done**: live TestMode raid, GlobalSetting/SMS/OffTrigger checks, and Monitor/export confirmation. Phase 1D remains pending.

## 2026-11-04 — SMS matched-trigger snapshot aliasing fix committed

**Application HEAD:** `0e8ab7056d32f16d1095a519ac4a1e87a29a4188`. Fixed `P1C-SMS-SNAPSHOT-ALIAS`: market-level trigger comment aggregation previously reused the same mutable `List<string>` assigned to the first SMS `TriggerSnapshot.MatchedTriggersContent`, causing later settings' descriptions to contaminate its persisted JSON. Production `Core/Main/PTMagic.cs` now calls `Core.Helper.MatchedMarketTriggerContent.Append`, which copies the initial market-level list, and `CopyForSnapshot`, which copies each saved setting's list. The market-level comment aggregation retains all activated setting descriptions in order; trigger decisions and PT writes are unchanged.

Five deterministic cases under `Tests/Phase1SmsSummaryIsolation` cover contamination, ordered aggregation, different markets, independent mutable list references and serialized snapshot isolation. **Source committed, not yet build/test/TestMode verified.** Run `dotnet build`, new 5-case harness, existing four test suites (previously 53/53), then a TestMode raid with at least two active SMS per market. Inspect the first SMS summary entry for BTC/ETH/SOL; it should contain only that setting's own descriptions. No Phase 1C DONE declaration until accepted verification.

## 2026-11-04 — SMS summary alias fix: build and regression verification passed

User reported `git pull --ff-only` **Already up to date** on the application branch after SMS list-isolation fix `0e8ab7056d32f16d1095a519ac4a1e87a29a4188`. `dotnet build` for Core, PTMagic, and Monitor net10.0 **succeeded in 5.9s** (Core 0.3s, PTMagic 0.1s, Monitor 4.3s). Tests passed: `Phase1SmsSummaryIsolation` **5/5**, `Phase1COhlcv` **13/13**, `Phase1MetricWarnings` **7/7**, `Phase1TriggerLogic` **29/29**, `Phase1AReadiness` **4/4**; **58/58 total**. The defect is now **source-fixed + build/regression verified**. **Still pending:** rerun a deployed TestMode raid with multiple active SMS on the same market and inspect `_data/SingleMarketSettingSummary.json` to verify first SMS descriptions are not contaminated. Do not claim this particular post-fix export behavior runtime-verified or mark Phase 1C completely closed until confirmed. [Verification update](updates/2026-11-04-sms-summary-test-verification.md).

## 2026-11-04 — Post-fix TestMode: reused SMS history, fresh-snapshot test pending

User uploaded a 19:05–19:07 KST deployed TestMode log, `LastRuntimeSummary(3).json`, `MarketTrendAnalytics(3).json` and `SingleMarketSettingSummary(3).json`.

- PTMagic 2.10.0 loaded existing SMS summaries at 19:05:24, refreshed 756/756 Binance Futures normalized series, calculated 1h/2h/4h metrics, matched all 15 diagnostic global 2h triggers, activated 8 diagnostic SMS across BTC/ETH/SOL and saved the summary. No errors/fatals; TestMode made no PT updates.
- The SMS export still contains **foreign messages** in the first setting per market: BTC **6** (9 total vs 3 own), ETH **1** (5 vs 4), SOL **1** (4 vs 3).
- Critically, **all eight** saved SMS activation timestamps remain at **2026-11-04 09:32:23Z (18:32 KST)**, over 30 minutes before this raid. Their `RefreshOffTriggers` properties are **false**. The run loaded and reserialized existing pre-fix snapshots; it did **not** demonstrate freshly generated SMS trigger snapshots after fix `0e8ab70`. The retained foreign descriptions are therefore **not evidence of failure of the patched list-copy behavior**.
- Existing 58/58 deterministic tests remain the current compile/test evidence. For an end-to-end verification, temporarily set `RefreshOffTriggers=true` for the active *diagnostic* SMS settings (at least the first and second BTC settings), perform one new TestMode raid with all those triggers true, then inspect the new activation timestamps and `MatchedTriggersContent`. Each SMS must contain only lines starting with its own `SettingName + ":"`. Revert `RefreshOffTriggers` afterward. Do not delete `SingleMarketSettingSummary.json` or reset real OffTrigger duration state unnecessarily.
- A subsequent re-save or update to `LastRuntimeSummary.json` alone is insufficient: the original snapshots must be regenerated to validate this specific fix.

**Status:** P1C-SMS-SNAPSHOT-ALIAS build+unit-test verified; *fresh deployed SMS snapshot test still pending*. Phase 1C not yet marked DONE.


## 2026-11-04 — Selective legacy PriceTrend follow-up: source committed, verification pending

**Task P1-COMPAT-LEGACY-SELECTIVE:** The post-Phase1C cleanup ensures a nonempty `MarketTrend.Metrics` does not automatically calculate the old per-asset PriceTrend or legacy global mean. Existing legacy-only MarketTrends (empty/omitted `Metrics`), legacy GlobalSetting PriceTrend triggers and legacy SMS/OffTriggers retain their required calculations. Non-Binance-Futures and CoinMarketCap behavior remains unchanged. Explicit normalized `PriceTrend` is calculated by the normalized analytics engine, not duplicated by the old engine.

Application source HEAD: [`1a6b9aa401fac74842e4d53ddbbfb2b2a4c5dc11`](https://github.com/HojouFotytu/PTMagic/commit/1a6b9aa401fac74842e4d53ddbbfb2b2a4c5dc11). `LegacyMarketTrendPlanner` identifies legacy dependencies; `BaseAnalyzer.BuildMarketTrends` and `BuildGlobalMarketTrends` accept an optional required-name set; `MarketTrendPopulationSelector` independently selects per-trend eligible normalized metric populations from current market snapshots and frozen Phase0 eligibility, with MaxMarkets/AllowedMarkets/IgnoredMarkets and configured TrendThreshold rules. Current market price and 24h volume used by SMS triggers, SMS activation snapshots, and `LastRuntimeSummary` no longer depend on `SingleMarketTrendChanges.Keys.Last()`. The old Market Analyzer will leave uncalculated legacy trend columns blank; eventual consolidation with the new Market Metrics page remains planned separately.

Added `Tests/Phase1SelectiveLegacy` **14 deterministic cases** (legacy/normalized trigger compatibility, independence of volume-only/age/time triggers, population/cap/filter behavior and no synthetic fallback data). **Build and tests not yet run.** Previous Phase1C 58/58 result predates this refactor; a fresh pass requires `dotnet build`, new 14-case suite and five existing suites (target **72/72 total**). TestMode must compare configured normalized metrics and 1h/2h/4h populations with baseline, legacy-only market/global PriceTrend, global and SMS normalized/legacy triggers, 24h volume/price snapshots, RAID SUMMARY and no PT writes. Until verified, do not claim the selective legacy optimization complete.


## 2026-11-04 — Selective legacy follow-up, final source hardening

Current source HEAD: [`40e546cb149bac0fca99e0aa257e7673453b7c8e`](https://github.com/HojouFotytu/PTMagic/commit/40e546cb149bac0fca99e0aa257e7673453b7c8e) on `phase1/market-data-foundation`. Subsequent commits after `1a6b9aa` hardened the old Monitor view: each skipped legacy trend now renders a blank cell in the appropriate absolute/relative table column (no shifted/misattributed values); relative columns require an actually calculated legacy global average; old persisted global graph trend history is not reloaded for skipped trends. The live current price/24h-volume fields remain available independent of legacy returns.

**Verification remains pending:** No new local .NET 10 build, test execution, Razor render or TestMode raid has been performed. Run the new 14 selective-planner tests + prior 58 regression checks (72 total), validate the old Market Analyzer column alignment, and verify that unchanged normalized analytics, legacy explicit/implicit triggers and 24h-volume SMS still work. The accepted Phase1C state refers to earlier tested source; this additional optimization is not yet accepted. [Updated implementation record](updates/2026-11-04-selective-legacy-price-trend.md).
