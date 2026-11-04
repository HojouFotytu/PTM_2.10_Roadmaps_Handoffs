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
| D-016 | **All derived MarketTrend metrics inherit their analytical timeframe from user-defined `MarketTrend.TrendMinutes`.** Normalized 5m candles are source resolution only. Window-based ATR, quote-volume metrics and correlation must use complete trend-duration periods built from closed input observations. Never hardcode a separate 5m/15m/1h metric timeframe or silently fall back; an N-period lookback counts trend-sized periods. No application code update is implied by this decision. | **Accepted / documentation corrected; implementation pending** |

**Known current exception:** already implemented return `Concentration` ranks Top10 by trailing 24h quote volume, even for other configured TrendMinutes. Its existing runtime and 100% coverage behavior remain unchanged until a separately tested correction is made (P1B-CONC-WINDOW). The universal policy is the target; this exception is **not** claimed fixed.

## Open decisions for Phase 1C

- OD-001: **Resolved for phase progression by D-010–D-015.** Original ingestion cause remains an unproven hypothesis; sparse listings and further fault injection remain non-blocking validation.
- OD-002: ATRP: TR formula, Wilder vs alternative smoothing, ATR seed/warm-up, period (initial proposal 14) and closing-price denominator, calculated from complete MarketTrend-sized bars aggregated from normalized 5m source candles.
- OD-003: **Resolved by D-016:** the ATR, volume and correlation analytical timeframe is `MarketTrend.TrendMinutes`. Lookback counts can differ by metric, but each counted period has the configured trend duration. Exact UTC aggregation/endpoint and sufficient retention are Phase 1C implementation checks.
- OD-004: Exact metric names and registration/config schema for volatility breadth and volume families.
- OD-005: Quote-volume expansion baseline count N (each interval equals `MarketTrend.TrendMinutes`), zero baseline and minimum-history policy.

Do not treat open decisions as already configured in application code.
