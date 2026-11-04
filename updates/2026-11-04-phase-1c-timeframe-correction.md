# 2026-11-04 — Phase 1C timeframe design correction

**Tasks:** P1C-01, P1C-02, P1C-03–07, P1D-CORR, P1B-CONC-WINDOW.  
**Source branch checked:** `HojouFotytu/PTMagic:phase1/market-data-foundation` at `89324bc5c8c5ea19ceb543b6ab5130899f2675dc`.  
**Change class:** Documentation / accepted user requirement; **no application source changes**.

## Before
The previous roadmap and handoff proposed `ATRP5m`, `MedianATRP5m` and 15m/1h volume metrics separately from `MarketTrend.TrendMinutes`. The previous roadmap explicitly allowed features to choose independent fixed metric intervals.

## After — D-016
All derived MarketTrend metrics inherit the user-defined `MarketTrend.TrendMinutes` as their analytical timeframe. Normalized 5-minute candles remain only the ingested storage resolution; window-based metrics aggregate consecutive, valid, fully closed 5m observations into complete trend-duration candles. Proposed metric names `ATRP` and `MedianATRP` carry no fixed suffix. Volume expansion, participation breadth, volume concentration and correlation must use the same configured trend duration. No silent fallback or auto-expanded retention.

ATRP(14) proposed warm-up is at least 15 complete trend candles (2h=30h, 4h=60h, 8h=120h, 12h=180h, 24h=360h); calculation convention and validation remain the next implementation task. The 90% global coverage rule and Phase 1A containment are unchanged.

**Existing discrepancy:** Phase 1B return `Concentration` uses fixed trailing 24h quote-volume ranking in current source, contrary to the general new timeframe rule. It needs a separately scoped, tested migration; not silently rewritten by this docs change.

## Repository updates
Added [corrected authoritative roadmap](../roadmaps/revised-2.10-2026-11-04-markettrend-timeframe.txt) and [superseding handoff](../handoffs/2026-11-04-phase-1c-markettrend-timeframe-correction.md); updated README pointers, status, decision register and changelog. Previous handoff and roadmap remain intact as historical snapshots.

**Verification:** Documentation cross-check against inspected source files. No build, unit test or TestMode result is claimed for this documentation-only change.
