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
