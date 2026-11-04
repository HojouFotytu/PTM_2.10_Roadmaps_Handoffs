# PTMagic 2.10 — Roadmap Revision History

This log tracks **roadmap and documentation changes**, not software releases. Software implementation claims require evidence in STATUS.md and dated update notes.

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
