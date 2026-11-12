# PTMagic 2.10 — Development Handoffs

**D-053 implementation and removal-audit checkpoint — November 12, 2026:** PTMagic source [`892a5f1f4729a3fccd3cb477ba6ad22fbbe0918d`](https://github.com/HojouFotytu/PTMagic/commit/892a5f1f4729a3fccd3cb477ba6ad22fbbe0918d) contains the completed removal of `OpenInterestChange`, `OpenInterestValueChange` and `GlobalLongShortAccountRatio`, including their acquisition/services/active caches/registry/Monitor integrations. The source audit compared the **22-metric pre-introduction baseline** [`66629347`](https://github.com/HojouFotytu/PTMagic/commit/66629347f0dc9c7b68ea9f1c3f5bf536f3d7c427), **27-metric pre-removal** `d101b5a0` and current **24-metric** code: all 22 original metric identities and scopes survive; `FundingRate` and `FundingSum` also survive. A real shared Unicode symbol-validator dependency was temporarily broken by deleting OI, then repaired by [`02820822`](https://github.com/HojouFotytu/PTMagic/commit/02820822b9bb) and [`d7847c46`](https://github.com/HojouFotytu/PTMagic/commit/d7847c46190b). No further major/critical removal-related defect was established by source inspection; **current-revision local build, 15-harness test execution and configured runtime acceptance remain unverified**. The earlier 18-harness PASS at `d101b5a0` is strictly **pre-removal evidence**. [Full read-only audit](../updates/2026-11-12-d053-removal-code-audit.md) (links relative to repository root). **This checkpoint supersedes all contradictory claims below that removal is pending, that retired OI/positioning is active, or that its tests/feature work remain required. Dated implementation evidence is retained as history.** No rollback and no strategy-settings work.


## Current scope — November 12 D-053

D-053 removes OI and all long/short positioning metrics and their planned market aggregates/higher-order dependencies. The implemented 24-metric catalogue and pending post-removal execution status are in [current roadmap](../roadmaps/CURRENT.md) and the [active project handoff](2026-11-10-som-enable-only.md). Earlier dated handoffs about OI or ratios are historical, **not future development instructions**.

## Current handoffs

### Monitor-only handoff

**[2026-11-11 — DashboardTop refresh resolved; Monitor interface state](2026-11-11-monitor-dashboard-refresh-resolved.md)**

Use this handoff for Monitor interface work. It records the recent Market Analyzer, Global Settings Log, metric-status legend, native NVD3 legend positioning and DashboardTop refresh changes. The user confirmed that DashboardTop is refreshing properly. It also records the strict requirement to explain the exact change and affected files before any GitHub edit, and to make no unrequested additions.

### Overall PTMagic 2.10 handoff

**[2026-11-10 — SOM safety, Phase 2 derivatives and persistence](2026-11-10-som-enable-only.md)**

Use this handoff for the broader PTMagic 2.10 startup-SOM and Phase 2 derivative work. The Monitor-specific handoff above does not replace this project-wide context.

## Historical handoffs

The following dated files are retained unchanged. Their “current,” “next,” and “pending” statements describe the date on which they were written.

| Handoff | Historical context |
|---|---|
| [2026-11-04 unified PriceTrend validation](2026-11-04-unified-pricetrend-validation-handoff.md) | Initial normalized migration runtime checks |
| [2026-11-04 Phase 1D correlation design](2026-11-04-phase1d-correlation-ready.md) | Pre-implementation design brief, based on the 58-test Phase 1C baseline |
| [2026-11-04 Phase 1C implementation verification](2026-11-04-phase1c-implementation-verification.md) | Phase 1C source awaiting its first validation |
| [2026-11-04 tri-state verification](2026-11-04-tristate-trigger-logic-verification.md) | Three-valued expression integration |
| [2026-11-04 Phase 1C timeframe correction](2026-11-04-phase-1c-markettrend-timeframe-correction.md) | Adoption of the TrendMinutes analytical-period contract |
| [2026-11-04 Phase 1C ready](2026-11-04-phase-1c-ready.md) | Earlier planning with subsequently corrected timeframe assumptions |
| [2026-11-04 original Phase 1C handoff](2026-11-04-phase-1c.md) | Earlier readiness-dependent planning |

## Handoff rules

- Recheck the application branch and HEAD at the start of a session.
- Record source implementation, source inspection, deterministic execution, and runtime acceptance separately.
- Preserve user decisions, scope exclusions, and known limits.
- Link the new dated handoff here as the sole current starting point.
- Update [STATUS](../STATUS.md), [DECISIONS](../DECISIONS.md), and current roadmap when the contract or sequence changes.
- Preserve previous dated handoffs. Do not revise their historical evidence to make it match later outcomes.
- Follow D-021: assistant authors and fixes; user runs local builds, harnesses, and configured runtime checks. Automatic GitHub Actions are opt-in.
- Follow D-022: supply fail-fast PowerShell with exact existing and new project paths; include runtime checks for behavior the deterministic tests do not establish.
- Personal trading-strategy development is outside the PTMagic 2.10 handoff.

Use [TEMPLATE.md](TEMPLATE.md) for subsequent sessions.
