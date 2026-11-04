# 2026-11-04 — Phase 1A closeout and Phase 1C start gate

**Task IDs:** P1A-READY, P1A-STORE, P1C-01, P1C-02, P4-TRIG
**Application repository:** `HojouFotytu/PTMagic`; working branch `phase1/market-data-foundation`
**Latest source HEAD reviewed:** `89324bc5c8c5ea19ceb543b6ab5130899f2675dc`
**State:** Phase 1A **DONE — CONTAINED**, Phase 1C **NEXT**.

## Before and after

**Before:** First cold-start raid could calculate normalized global values using only a minority of exact eligible markets. A 756-series initial fetch might finish across multiple 5m boundaries; the first historical diagnostic reported only 259/1434 valid 4h per-asset metrics, then full recovery during the next raid.

**After:** Global normalized aggregates fail closed below 90% of eligible aligned series, including eligible markets with missing data in the denominator; existing return-based `Concentration` requires 100%. `FeatureValueSnapshot` records sample/eligible counts and coverage. Runtime and Monitor expose expected common closed endpoint and invalid-reason counts. Unavailable normalized triggers cannot activate GlobalSettings/SMS; active setting is retained when no independent fully evaluable setting matches. Scheduled next raid repairs gaps naturally; no forced extra Binance requests or trading suspension.

## Relevant code commits

- [3a2ba02](https://github.com/HojouFotytu/PTMagic/commit/3a2ba0227246ea4bcad91205273575ae04fa4f8e) — coverage, diagnostics and Monitor metadata.
- [c038a11](https://github.com/HojouFotytu/PTMagic/commit/c038a11baff881285317f07f393084624b6bd3ca) — GlobalSetting retention/normalized trigger safeguards.
- [e002801](https://github.com/HojouFotytu/PTMagic/commit/e002801555ffb98e8169e1943aa4a13b05956b52) — deterministic regression harness.
- [11d6e28](https://github.com/HojouFotytu/PTMagic/commit/11d6e286b0ed6474d730eb2eba1b6ecb0158a26d) — raid summary switched/reapplied distinction.

## Actual build and tests

User reported `dotnet build` succeeded for **Core**, **PTMagic**, **Monitor** on net10.0; `dotnet run --project Tests/Phase1AReadiness/Phase1AReadiness.csproj` yielded **4 passed**.

| TestMode raid | Normalized refresh | Global 4h coverage | Asset metrics |
|---|---|---|---|
| First (~13:30 KST) | 756/756, 654696 candles | 32/250 (12.8%); 218 MissingEndpoint | 0/1434 |
| Next (~13:31 KST) | 705/756, 2115 candles | 249/249 (100%) | 1434/1434 |
| Idle (~13:32 KST) | 0 kline requests | 249/249 (100%) | 1434/1434 |
| 5m boundary (~13:35 KST) | 756/756, 2268 candles | 249/249 (100%) | 1434/1434 |

First raid rejected normalized dependent GlobalSettings, retained `Default`; after recovery, normal `DIAG_Global_AllMetrics` activation occurred at 13:33 KST after flood protection expired, and subsequent raids were stable. BTC/ETH normalized SMS and SOL legacy SMS exercised. **No PT settings were sent because TestMode was enabled.**

## Important limitations

This is verified **containment**, not proof that the root ingestion mechanism was identified or the first cold-start raid will always be complete. Tests did not exercise retaining a previously active *non-default* GlobalSetting when coverage later fails. Log output precedes the separate summary wording change `11d6e28`; that change needs a targeted build/runtime confirmation. Expanded partial/stale/sparse/fault checks remain under P1E, not blockers for 1C. Tested binary identified itself as 2.9.1; development belongs to 2.10.

## Roadmap and handoff

Updated [authoritative 2.10 roadmap](../roadmaps/revised-2.10-2026-11-04.txt), [STATUS.md](../STATUS.md), [decisions D-010–D-015](../DECISIONS.md), [closed issue 001](../issues/001-cold-start-readiness.md). Begin [Phase 1C P1C-01 ATRP5m](../handoffs/2026-11-04-phase-1c-ready.md) then `MedianATRP5m`; existing history, time alignment, valid-sample gating and legacy compatibility must remain intact.
