# PTMagic 2.10 — Roadmap Revision History

This log tracks **roadmap and documentation changes**, not software releases. Software implementation claims require evidence in STATUS.md and dated update notes.

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
