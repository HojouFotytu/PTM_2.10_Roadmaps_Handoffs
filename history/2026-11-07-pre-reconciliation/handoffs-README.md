- **[2026-11-04 — Unified PriceTrend Binance Futures TestMode handoff](2026-11-04-unified-pricetrend-validation-handoff.md)** (**CURRENT validation**; Futures verified, Spot/US and positive OffTrigger checks pending)
- **[2026-11-04 — Phase 1D correlation implementation handoff](2026-11-04-phase1d-correlation-ready.md)** (**CURRENT**; Phase 1C DONE, 1D NEXT)
- **[2026-11-04 — Phase 1C implementation verification handoff](2026-11-04-phase1c-implementation-verification.md)** (newest; 1C source committed, tests pending)
# PTMagic 2.10 — Development Handoffs

**[2026-11-04 — Tri-state trigger evaluation verification handoff](2026-11-04-tristate-trigger-logic-verification.md)** (latest source commits; testing pending). Continue with the [timeframe-corrected Phase 1C handoff](2026-11-04-phase-1c-markettrend-timeframe-correction.md) after accounting for these changes.

Date-stamped handoffs preserve what was known, done and planned **at the time of writing**. They are not automatically authoritative over later code or accepted decisions.

- **[2026-11-04 — Corrected Phase 1C: all metric timeframes from MarketTrend](2026-11-04-phase-1c-markettrend-timeframe-correction.md)** (**latest; use this handoff**)
- [2026-11-04 — Phase 1C-ready handoff after Phase 1A closeout](2026-11-04-phase-1c-ready.md) (historical; incorrect fixed ATRP5m timeframe superseded by D-016)
- [2026-11-04 — Original Phase 1C development handoff](2026-11-04-phase-1c.md) (archived; readiness was then blocking)
- [Handoff template](TEMPLATE.md)

## Handoff procedure

At the end of a working session: add a dated handoff file, reference current branch HEAD and implemented commits, state evidence separately from hypotheses, update [STATUS.md](../STATUS.md), and link any new issues and [updates](../updates/README.md). In the next session: read current HEAD and latest status first, then consult prior handoff. Never assume a handoff snapshot is still current.

## Required development and validation workflow (D-021)

Every new development handoff must preserve this ownership contract:

- **Assistant:** source implementation, code review, regression-test development, and fixes for user-reported errors.
- **User:** local builds, regression harness execution, and PTMagic TestMode for Binance Futures, Binance Spot, and Binance US as applicable.
- **Review together:** user provides actual logs, build/test outputs, and runtime summaries; assistant investigates failures and makes fixes.
- **GitHub:** source control and roadmap/handoff documentation only; automatic CI/GitHub Actions build or testing is **opt-in by explicit user request**.

Mark build, deterministic test and live TestMode results individually as *passed*, *failed*, or *not run*. Never infer a run from test code or a commit. Use the [handoff template](TEMPLATE.md) so this agreement carries into every new chat.

