# PTMagic 2.10 — Market Analysis Expansion

**Dedicated documentation repository for the PTMagic 2.10 development roadmap, implementation status, decisions, revisions and handoffs.**

- Product version: **2.10** (2.9 modernization release is finished).
- Application repository: [HojouFotytu/PTMagic](https://github.com/HojouFotytu/PTMagic).
- Active development branch: `phase1/market-data-foundation`.
- Latest application source HEAD checked: [`0e8ab7056d32f16d1095a519ac4a1e87a29a4188`](https://github.com/HojouFotytu/PTMagic/commit/0e8ab7056d32f16d1095a519ac4a1e87a29a4188) on 2026-11-04. Original roadmap baseline `9e00a1f` remains historical.
- Framework: .NET 10; normalized analytics target: Binance Futures USDT perpetuals.

## Canonical technical plan and historical sources

| Document | Role |
|---|---|
| [Revised PTMagic 2.10 roadmap](roadmaps/revised-2.10-2026-11-04-markettrend-timeframe.txt) | **Authoritative technical roadmap**; detailed requirements, phase definitions and 2026-11-04 observations |
| [Previous 2.10 roadmap (superseded timeframe assumptions)](roadmaps/revised-2.10-2026-11-04.txt) | Historical 2026-11-04 Phase 1A closeout revision; contains static ATRP5m proposals, now superseded by D-016 |
| [Original roadmap](roadmaps/original.txt) | Immutable historical baseline for comparison |
| [Previous 2.9.1-labeled revision](roadmaps/revised-2.9.1-2026-11-04.txt) | Historical revision retained for provenance; **not the current project/version designation** |
| [Phase 0 architecture audit](audits/phase-0-architecture-audit.txt) | Completed baseline architecture findings |
| [Current status](STATUS.md) | **Operational source of truth for tracked tasks and blockers**, updated as work proceeds |
| [Change log](CHANGELOG.md) | Chronological record of roadmap/documentation revisions |
| [Decisions](DECISIONS.md) | Accepted decisions and explicit open design choices |
| [Dated updates](updates/README.md) | Evidence-oriented implementation and roadmap update notes |
| [Handoffs](handoffs/README.md) | Dated session handoffs, starting with Phase 1C |
| [Closed Phase 1A readiness issue](issues/001-cold-start-readiness.md) | DONE by verified correctness containment; non-blocking follow-ups recorded |
| [Phase 1D-ready handoff](handoffs/2026-11-04-phase1d-correlation-ready.md) | **Current starting point: Phase 1C DONE, synchronized TrendMinutes return correlation NEXT** |
| [Latest Phase 1C closeout evidence](updates/2026-11-04-phase1c-final-closeout.md) | Verified TestMode and isolated SMS snapshots |
| [Corrected Phase 1C handoff (historical)](handoffs/2026-11-04-phase-1c-markettrend-timeframe-correction.md) | D-016 timeframe decision and Phase 1C planning, now complete |
| [Earlier Phase 1C-ready handoff](handoffs/2026-11-04-phase-1c-ready.md) | Historical; proposed fixed ATRP5m incorrectly |

## Precedence

1. **Actual repository source and verified runtime results** decide what is implemented and working.
2. **Accepted dated decisions** govern intent and supersede incompatible historical wording.
3. **The revised 2.10 roadmap** governs feature scope and technical constraints.
4. **STATUS.md** records the latest *evidence-backed* implementation status, without silently rewriting the underlying roadmap.
5. Earlier revisions, handoffs and audits remain historical records. Never silently overwrite history.

A task marked [DONE] must identify the relevant commit and test evidence when available. Unverified claims remain [PARTIAL], [ISSUE] or [PLANNED].

## Update protocol

1. Read the actual code-branch HEAD and relevant code before any development claim.
2. Refer to stable task IDs in [STATUS.md](STATUS.md).
3. Update the status, issue and decision records affected by a change.
4. Add a dated entry under [updates/](updates/) using [the template](updates/TEMPLATE.md), citing commits, evidence, limitations and next steps.
5. When a new handoff is supplied, archive it as a dated file under [handoffs/](handoffs/) and update its index. Do **not** rewrite an earlier handoff in place.
6. When the roadmap itself changes materially, update the authoritative roadmap **with an explicit review** and document what changed and why in CHANGELOG.md; retain historical copies in Git history.
7. Never label proposed fixes as verified. Never treat successful download or successful build as proof of analytics correctness.
8. Avoid application code changes in documentation-only commits. Do not merge or alter release branches without explicit authorization.

## D-017 trigger semantics update (2026-11-04)

GlobalSetting, SMS and OffTrigger now have a source-code implementation of complete-expression three-valued evaluation. `true OR unavailable` is true; a final unknown remains ineligible. See [update](updates/2026-11-04-three-valued-trigger-logic.md) and [verification handoff](handoffs/2026-11-04-tristate-trigger-logic-verification.md). **Build/tests/TestMode are pending**, not claimed completed. Source branch HEAD for this code change: `fbc4b35bdd65abcf1252cbcf99e7d2aa8c10ac3b` (compatibility follow-up after initial two commits).

## Current gate

**Phase 1A: DONE — CONTAINED (2026-11-04).** The 90% cross-sectional readiness gate and GlobalSetting safety behavior were implemented, tested and observed in live TestMode. A first-raid incomplete global population is rejected, the next scheduled incremental raid restores coverage and idle raids make no redundant normalized kline requests. The exact original long-bootstrap cause is not proven. See [dated closeout](updates/2026-11-04-phase-1a-closeout.md).

**Next:** [Phase 1C P1C-01 `ATRP`, then P1C-02 `MedianATRP`](handoffs/2026-11-04-phase-1c-markettrend-timeframe-correction.md), using complete `MarketTrend.TrendMinutes`-duration candles aggregated from normalized 5m data. All derived metric timeframes follow the user's MarketTrend definition; volatility breadth and quote-volume expansion/concentration follow the same policy. See D-016.

**Trigger harness follow-up (2026-11-04):** User reported separate test-project CS0121 errors after a successful Core/PTMagic/Monitor build and passing Phase 1A tests. Fix committed as [`c66b9f3`](https://github.com/HojouFotytu/PTMagic/commit/c66b9f3a2572b0bd9ebf1c737bd98b4f9f8e6953); trigger harness must still be rerun.

**Latest D-017 verification (2026-11-04):** User-run Core/PTMagic/Monitor .NET 10 build succeeded; `Tests/Phase1TriggerLogic` **29/29 passed** and `Tests/Phase1AReadiness` **4/4 passed**, at source HEAD `c66b9f3`. The earlier CS0121 failure and pending rerun above are historical. End-to-end TestMode verification remains outstanding. [Verification update](updates/2026-11-04-tristate-test-results.md).

**2026-11-04 raid metric diagnostics (D-018):** Commit [`34c30aa`](https://github.com/HojouFotytu/PTMagic/commit/34c30aa08918252d2976d6fabd7dddb1589acfd9) groups missing/unavailable normalized metrics into a compact RAID SUMMARY section and removes repeated per-pair trigger warnings. Seven metric-warning tests are authored but not yet run. Phase 1C ATRP remains next. [Details](updates/2026-11-04-raid-metric-warnings.md).

**D-018 verification (2026-11-04):** User reports `dotnet build` passed and all **40 deterministic tests** passed at application HEAD `34c30aa`: metric warning 7/7, tri-state 29/29, Phase1A 4/4. Actual TestMode RAID SUMMARY output remains pending. [Evidence](updates/2026-11-04-raid-metric-warnings-verification.md).

**D-018 amendment (2026-11-04):** The five-line RAID SUMMARY metric-warning cap was removed at application commit [`64e05e7`](https://github.com/HojouFotytu/PTMagic/commit/64e05e7e2a93aa23828890ef5e4708f002c696b8). All distinct grouped warnings now appear; build/test re-verification pending. [Update](updates/2026-11-04-all-metric-warnings.md).

**Phase 1C implementation checkpoint (2026-11-04):** P1C-01 through P1C-07 source was committed at [`64d063c`](https://github.com/HojouFotytu/PTMagic/commit/64d063c1c9bc8886fb456cae97921780449f5cce) with 13 synthetic tests. **Do not treat Phase 1C as verified or complete yet**: a new .NET 10 build, test suite, TestMode run and Monitor inspection are required. [Latest handoff](handoffs/2026-11-04-phase1c-implementation-verification.md).

**Phase 1C closeout (2026-11-04):** Source and post-fix snapshot tests passed **58/58**; deployed TestMode and Monitor content verified; final fresh BTC/ETH/SOL export had **8/8 isolated SMS snapshots**. **Phase 1D is the next development task.** [Closeout](updates/2026-11-04-phase1c-final-closeout.md) · [Handoff](handoffs/2026-11-04-phase1d-correlation-ready.md).

**Selective legacy PriceTrend follow-up (2026-11-04):** Opt-in `Metrics` trends no longer require duplicate legacy return calculations unless legacy triggers reference them. [Code `1a6b9aa`](https://github.com/HojouFotytu/PTMagic/commit/1a6b9aa401fac74842e4d53ddbbfb2b2a4c5dc11) · [tracking and verification](updates/2026-11-04-selective-legacy-price-trend.md). New test suite **not executed**; original Phase1C accepted state is a prior baseline, not evidence for this refactor.
