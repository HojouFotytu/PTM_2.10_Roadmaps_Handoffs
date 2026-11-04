# PTMagic 2.10 — Current Development Status

**As of:** 2026-11-04 — Phase 1A DONE (containment); Phase 1C NEXT; user-accepted MarketTrend timeframe rule D-016.
**Source:** [HojouFotytu/PTMagic](https://github.com/HojouFotytu/PTMagic), `phase1/market-data-foundation`.
**Last code HEAD verified for this update:** `89324bc5c8c5ea19ceb543b6ab5130899f2675dc` (merge commit; recheck before development).

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
| P1C-01 | Per-asset ATRP on MarketTrend.TrendMinutes candles | **BUILD/TEST VERIFIED — TESTMODE PENDING** | Source commit 64d063c; 53/53 deterministic tests passed; TestMode and Monitor checks pending |
| P1C-02 | MedianATRP on the same configured MarketTrend timeframe | **BUILD/TEST VERIFIED — TESTMODE PENDING** | Source commit 64d063c; 53/53 deterministic tests passed; TestMode and Monitor checks pending |
| P1C-03 | Volatility breadth | **BUILD/TEST VERIFIED — TESTMODE PENDING** | Source commit 64d063c; 53/53 deterministic tests passed; TestMode and Monitor checks pending |
| P1C-04 | Recent quote-volume expansion | **BUILD/TEST VERIFIED — TESTMODE PENDING** | Source commit 64d063c; 53/53 deterministic tests passed; TestMode and Monitor checks pending |
| P1C-05 | Volume-expansion breadth | **BUILD/TEST VERIFIED — TESTMODE PENDING** | Source commit 64d063c; 53/53 deterministic tests passed; TestMode and Monitor checks pending |
| P1C-06 | Volume concentration | **BUILD/TEST VERIFIED — TESTMODE PENDING** | Source commit 64d063c; 53/53 deterministic tests passed; TestMode and Monitor checks pending |
| P1C-07 | Registry/Monitor/trigger/test integration | **IMPLEMENTED; SMS REGRESSION VERIFICATION PENDING** | 53/53 existing tests and deployed Phase 1C runtime/Monitor content verified; SMS list-alias fix `0e8ab70` committed; new 5-case test, build, focused TestMode pending |
| P1-PERF-SNAPSHOT | Reuse unchanged historical snapshots between raids | **OPTION / PLANNED** | Avoid redundant full-series copy/sort/gap validation; preserve invalidation, staleness and thread safety; benchmark before/after (roadmap §12.7) |
| P1D-CORR | Synchronized return correlation | PLANNED | TrendMinutes-based return cadence, not independent 5m/15m |
| P1E-INSPECT | Inspection and additional fault tests | PARTIAL | Carry non-blocking checks below |
| P2-RAW | Futures funding/OI/positioning/flow ingestion | PLANNED | Later |
| P2B-AGG | Futures market-wide aggregation | PLANNED | Later |
| P3-STATE | Deterministic higher-order states | PLANNED | Later |
| P4-TRIG | GlobalSetting / SMS / OffTrigger normalized metric routing | **BUILD + DETERMINISTIC TESTS PASSED** | D-017: Core/PTMagic/Monitor build passed; tri-state 29/29 and Phase1A 4/4 passed at `c66b9f3`; TestMode integration remains pending |
| P5-LIQ | Liquidity/depth/stress | PLANNED | Later |
| P6-HIST | Feature history and validation | PLANNED | Later |

## Phase 1A closeout

**Code commits:** `3a2ba02` (90% global gate, 100% Concentration exception, coverage metadata and diagnostics); `c038a11` (unavailable normalized triggers fail closed, active GlobalSetting held on indeterminate fallback, SMS negation protection); `e002801` (four deterministic tests); `11d6e28` (raid summary distinguishes GlobalSetting switch from same-setting reapplication). All appear in the latest inspected branch.

**User-run tests:** `dotnet build` succeeded for Core/PTMagic/Monitor on .NET 10. `dotnet run --project Tests/Phase1AReadiness/Phase1AReadiness.csproj`: **4 tests passed**.

**User-supplied Binance Futures TestMode:** First raid fetched 756/756 normalized series (654,696 candles), but 4h global coverage was 32/250 (12.8%), with 218 MissingEndpoint; all dependent global features were unavailable and GlobalSetting triggers rejected. Second raid incrementally fetched 2,115 candles for 705 markets, recovered global coverage 249/249 and asset metrics 1,434/1,434. Third raid required **zero** normalized kline requests. After flood protection, `Default` switched to `DIAG_Global_AllMetrics` at 13:33 KST, with subsequent stable operation. Five-minute boundary raids downloaded ~2,268 incremental candles. TestMode sent no settings to PT.

**Policy:** Exact eligible GlobalSetting trend population is denominator; required valid count `ceil(0.9 * eligible)`, nonempty population. Existing `Concentration` requires 100% quote-volume-ranked population. Invalid, missing and stale metrics never substitute zero. Independent valid and legacy triggers may still operate; no forced cleanup raid, ingestion redesign or trading suspension.

**Root cause distinction:** A long cold-start fetch crossing 5m candle boundaries is plausible, **not proved**. The defect's *consequences* are contained and normal scheduled refresh repairs incompleteness. This is why P1A-READY is closed; it is not a claim that the first raid always has full data.

**Non-blocking follow-ups (P1E):** Verify retention of an already-active non-default GlobalSetting when coverage later falls below 90%; validate the revised raid summary wording in a new build/runtime; further partial-coverage, stale, sparse and boundary fault tests. The logs preceding the summary patch still say `Global setting changed`. Tested executable reported 2.9.1, whereas active product roadmap is 2.10.

## Accepted metric timeframe rule (D-016)

All derived metric analysis timeframes come from the configured `MarketTrend.TrendMinutes`. Normalized 5m is the source-data resolution only. P1C-01 `ATRP` and P1C-02 `MedianATRP` use complete, UTC-aligned trend-sized candles; 5m-fixed ATR/15m-fixed participation metrics are not valid Phase 1C designs. ATR(14) needs at least 15 complete trend candles; if `StoreDataMaxHours` is too short, metric is unavailable. This is an accepted **design requirement, not an implemented code change**. Existing return `Concentration` still uses fixed trailing 24h ranking and is recorded as a separate follow-up.

**Next:** [Corrected Phase 1C handoff](handoffs/2026-11-04-phase-1c-markettrend-timeframe-correction.md), starting with dynamic `ATRP` then `MedianATRP`.

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
