# PTMagic 2.10 — Decision Register

Accepted decisions are not inferred from a merely proposed feature. Add a dated entry whenever an actual design decision is made.

| ID | Date | Decision | State |
|---|---|---|---|
| D-001 | 2026-11-04 | All Phase 0–6 market-analysis work is for **PTMagic 2.10**; 2.9 modernization is finished. | Accepted |
| D-002 | Phase 0 | Keep the legacy `MarketData_*.json` and legacy trend/settings pipeline intact; normalized 5m OHLCV is a parallel new layer. | Accepted |
| D-003 | 2026-11-04 | Each normalized metric uses the *actual* Phase 0-resolved per-trend universe; do not independently rebuild its own universe. | Accepted |
| D-004 | 2026-11-04 | Omitted `Trigger.Metric` uses legacy trigger behavior; optional normalized metrics are enabled by comma-separated `MarketTrend.Metrics`. | Accepted |
| D-005 | 2026-11-04 | Missing/invalid/stale normalized metrics fail closed, never substitute zero. | Accepted |
| D-006 | 2026-11-04 | `Concentration` remains Top10 **return advantage** (pp); volume share gets a separate metric name. | Accepted |
| D-007 | 2026-11-04 | Phase 4 = trigger integration, Phase 5 = liquidity, correcting earlier conflicting numbering. | Accepted |
| D-008 | 2026-11-04 | Cold-start completeness must be resolved or explicitly contained before new Phase 1C metrics. Disk warm-start cache is a separate optional performance project. | Accepted |
| D-009 | 2026-11-04 | Preserve historical roadmap revisions and handoff messages; edit current status/update log rather than overwriting source history. | Accepted |

## Phase 1A closeout decisions (2026-11-04)

| ID | Decision | State |
|---|---|---|
| D-010 | Enforce global normalized cross-sectional readiness at **90%** of exact eligible Phase 0 trend population; require `ceil(0.90 * N)` valid markets, with nonempty population; do not remove missing samples from denominator. | Accepted / implemented |
| D-011 | Existing return-based `Concentration` requires **100%** of eligible ranked assets with valid complete trailing quote-volume data. This is stricter than the general 90% policy. | Accepted / implemented |
| D-012 | Do not force a cleanup raid or redesign ingestion. Let the next normally scheduled incremental refresh repair incomplete closed-candle alignment; dependent normalized metrics must fail closed, independent/legacy metrics remain available. | Accepted / verified |
| D-013 | When normalized GlobalSetting selection is indeterminate and no fully evaluated independent setting matches, retain the active setting rather than switching to `default`. Prevent unavailable metrics from satisfying negated custom trigger expressions. | Accepted / implemented |
| D-014 | No automatic trading suspension for transient insufficient coverage. Reapplying the same GlobalSetting is permitted; distinguish setting *switched* from *reapplied* in raid logging. | Accepted / code committed, new logging untested |
| D-015 | Close Phase 1A as **DONE — CONTAINED**, not a proven root-cause ingestion repair; record non-default-setting retention and updated logging runtime checks as non-blocking Phase 1E items. Phase 1C may start. | Accepted |

## Phase 1C timeframe correction (2026-11-04)

| ID | Decision | State |
|---|---|---|
| D-016 | **All derived MarketTrend metrics inherit their analytical timeframe from user-defined `MarketTrend.TrendMinutes`.** Normalized 5m candles are source resolution only. Window-based ATR, quote-volume metrics and correlation must use complete trend-duration periods built from closed input observations. Never hardcode a separate 5m/15m/1h metric timeframe or silently fall back; an N-period lookback counts trend-sized periods. No application code update is implied by this decision. | **Accepted; Phase 1C implementation and TestMode verified** |

**Known current exception:** already implemented return `Concentration` ranks Top10 by trailing 24h quote volume, even for other configured TrendMinutes. Its existing runtime and 100% coverage behavior remain unchanged until a separately tested correction is made (P1B-CONC-WINDOW). The universal policy is the target; this exception is **not** claimed fixed.

## Open decisions for Phase 1C

- OD-001: **Resolved for phase progression by D-010–D-015.** Original ingestion cause remains an unproven hypothesis; sparse listings and further fault injection remain non-blocking validation.
- OD-002: ATRP: TR formula, Wilder vs alternative smoothing, ATR seed/warm-up, period (initial proposal 14) and closing-price denominator, calculated from complete MarketTrend-sized bars aggregated from normalized 5m source candles.
- OD-003: **Resolved by D-016:** the ATR, volume and correlation analytical timeframe is `MarketTrend.TrendMinutes`. Lookback counts can differ by metric, but each counted period has the configured trend duration. Exact UTC aggregation/endpoint and sufficient retention are Phase 1C implementation checks.
- OD-004: Exact metric names and registration/config schema for volatility breadth and volume families.
- OD-005: Quote-volume expansion baseline count N (each interval equals `MarketTrend.TrendMinutes`), zero baseline and minimum-history policy.

Do not treat open decisions as already configured in application code.

## Phase 1A trigger refinement — D-017 (2026-11-04)

| ID | Decision | State |
|---|---|---|
| D-017 | Evaluate configured GlobalSetting, SMS activation and SMS OffTrigger expressions using **three-valued logic**: true, false, unavailable. `true OR unavailable=true`; `false OR unavailable=unavailable`; `false AND unavailable=false`; `true AND unavailable=unavailable`; `NOT unavailable=unavailable`. A conclusively true complete expression may match even if an unused branch is unavailable. An indeterminate result may not activate a setting or trigger SMS removal. Existing active-setting retention applies when GlobalSetting selection remains indeterminate; existing SMS long-term OffTrigger persistence is preserved. | **Accepted; 29/29 tests and GlobalSetting/SMS live TestMode verified** |

D-017 refines earlier D-013 fail-closed policy. Fail-closed means **do not activate on an indeterminate final expression**, not “discard the whole setting whenever any input is unknown.” D-016 (metric timeframe inheritance) is unchanged.

## Raid metric diagnostics — D-018 (2026-11-04)

| ID | Decision | State |
|---|---|---|
| D-018 | Put a **short, deduplicated Metric warnings section** in the analyzer raid summary, grouping unavailable normalized metrics by MarketTrend/metric with all distinct grouped warnings displayed (no limit). Include indeterminate GlobalSetting retention information. Eliminate repetitive per-pair normalized trigger warnings, but do not change tri-state semantics or legacy setting behavior. A Monitor notification may be considered separately. | **Accepted; 7/7 tests and full grouped RAID SUMMARY verified live** |

**2026-11-04 D-018 amendment:** The user superseded the earlier five-detail display limit. List **all distinct grouped metric warnings** in the raid summary; do not truncate with `... and N more`. Duplicate grouping remains, with no change to trigger logic. Application commit `64e05e7`; re-verification pending.

**2026-11-04 D-018 amended-policy verification:** User-run .NET 10 Core/PTMagic/Monitor build succeeded (14.1s) and Phase1MetricWarnings regression passed **7/7** at application HEAD `64e05e7`. TestMode raid presentation remains pending. The decision-row wording above now reflects the final accepted no-truncation policy; earlier dated records retain the superseded limit for history.

## Phase 1C metric calculation contracts — D-019 (2026-11-04)

| ID | Decision | State |
|---|---|---|
| D-019 | Implement ATRP and volume metrics exclusively on complete `MarketTrend.TrendMinutes` periods assembled from 5m source OHLCV. Per-trend parameters default ATRPeriod=14, VolumeExpansionLookback=20, ATRPBreadthThreshold=0.5%, VolumeExpansionBreadthThreshold=1.0x, StrongVolumeExpansionThreshold=1.5x, TopNVolumeCount=10. Global medians and breadth require 90% coverage. `VolumeConcentration` is HHI ×100 (*index*), while TopN/BTC/BTC+ETH are volume **percentage shares** requiring 100% complete eligible volume population. No short-data fallback or extra exchange calls. | **Accepted; source, numerical fixtures, and live TestMode verified** |

D-019 instantiates D-016's universal trend-duration rule. Defaults are configurable; no legacy setting changes merely because metrics remain disabled. Existing return `Concentration` remains a separately tracked fixed-24h ranking exception, P1B-CONC-WINDOW.

**2026-11-04 D-019 verification:** User-run .NET 10 build passed at `64d063c`, with 53/53 deterministic checks passing (13 Phase1C). This verifies source fixtures, not Binance Futures TestMode behavior or Monitor presentation. No calculation-contract change.

## Phase 1C final acceptance — 2026-11-04

The D-016/D-017/D-018/D-019 contracts used in Phase 1C were confirmed by the user-run **58/58 deterministic tests** and deployed TestMode. An isolated `MatchedTriggersContent` defect in the per-SMS JSON summary was corrected at application `0e8ab70`, and the 19:10–19:33 KST final run produced **8 newly activated BTC/ETH/SOL snapshots with zero foreign descriptions**, closing `P1C-SMS-SNAPSHOT-ALIAS`. Phase 1C is **DONE** and Phase 1D is **NEXT (not implemented)**. Existing return `Concentration` fixed trailing 24h rank window remains a separate P1B follow-up; no changes to D-016 for new features.

Correlation Phase1D decisions remain open: Pearson vs alternatives (Pearson intended first), simple versus log returns, synchronized bar count/window, treatment of missing candles and zero variance, 90% market coverage, and optional pairwise measures. No new independent 5m/15m analysis cadence is permitted; use `MarketTrend.TrendMinutes` (D-016).
