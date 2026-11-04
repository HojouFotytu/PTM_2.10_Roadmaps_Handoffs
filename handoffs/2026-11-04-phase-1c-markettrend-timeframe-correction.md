# PTMagic 2.10 — Phase 1C handoff, corrected MarketTrend timeframe

**Date:** 2026-11-04  
**Status:** ACTIVE / supersedes [the earlier Phase 1C-ready handoff](2026-11-04-phase-1c-ready.md) only on timeframe design. Earlier handoffs remain historical.  
**Application repository:** [HojouFotytu/PTMagic](https://github.com/HojouFotytu/PTMagic)  
**Working branch:** `phase1/market-data-foundation`  
**Application HEAD verified when preparing this handoff:** `89324bc5c8c5ea19ceb543b6ab5130899f2675dc` — recheck before development.  
**Canonical roadmap:** [Revised 2.10 roadmap — MarketTrend timeframe correction](../roadmaps/revised-2.10-2026-11-04-markettrend-timeframe.txt)  
**Operational tracker:** [STATUS.md](../STATUS.md) • [Decisions](../DECISIONS.md), especially D-016.

## Correction accepted by the user

**ALL derived metric analytical timeframes are determined by each user-defined `MarketTrend.TrendMinutes`.** The prior proposed hardcoded `ATRP5m`, `MedianATRP5m` and 15m/1h volume-expansion examples were incorrect as designs for Phase 1C. Their names and fixed analytical intervals must not be carried into code.

Five-minute closed OHLCV candles remain the *shared normalized input resolution* because that is what the current source ingests. This does not force any calculated metric to use a 5-minute measurement interval. Source observations are grouped into complete, UTC-aligned `MarketTrend.TrendMinutes` windows where the feature requires OHLC or quote-volume bars. A `MarketTrend` of 4h uses complete 4h bars for ATR and participation metrics; a 12h trend uses complete 12h bars. Other supported user-defined periods follow the same rule. No implicit fallback to 5m if the trend window is unsupported or lacks sufficient history.

Any native cadence of Binance funding/depth/other exchange events is separate from the user's *derived calculation timeframe*. Indicators must state how native observations map to the configured trend horizon. Lookback counts such as ATR period 14 or volume previous N are numbers of *trend-sized* periods, not independent hardcoded timeframes.

## Current implementation state

- **Phase 1A:** DONE by accepted correctness containment, not proof of the first-raid ingestion root cause. Existing 90% eligible global coverage and fail-closed trigger handling remain mandatory.
- **Phase 1B:** Eight metrics implemented. `PriceTrend`, `MedianPriceTrend`, `MeanMedianSpread`, `Breadth`, `Dispersion`, `RelativeStrengthMarket`, `RelativeStrengthBTC`, return-based `Concentration`.
- **Phase 1C:** No implementation or verification claimed by this handoff. Start with P1C-01 `ATRP`, then P1C-02 `MedianATRP` (proposed registry spellings without interval suffix).
- **Source limitation:** The *existing* `Concentration` ranks Top10 using trailing 24h quote volume rather than `TrendMinutes`. Preserve current behavior until an explicit, tested follow-up corrects this D-016 exception. The documentation edit does not fix running code.

## P1C-01 — dynamic per-asset ATRP

1. Read the latest source, particularly `Core/MarketAnalyzer/MarketData/MarketTrendAnalyticsEngine.cs`, `MarketDataStore.cs`, `MarketDataSeriesSnapshot.cs`, `MarketTrendMetrics.cs` and runtime. The existing analyzer supplies exact trend-specific global and SMS asset universes. Do not rebuild them.
2. Group consecutive, fully closed normalized 5m OHLCV into **complete** candles of the configured `MarketTrend.TrendMinutes`, aligned on UTC interval boundaries. Aggregated open=first source open, high=max high, low=min low, close=last source close; quote volume=sum when needed. Never include an incomplete target interval.
3. Proposed TR: `max(high-low, abs(high-previousClose), abs(low-previousClose))` across consecutive completed *trend-sized* candles. Proposed initial ATR(14): arithmetic average of first 14 **defined** TRs, requiring 15 complete consecutive trend bars; thereafter Wilder `ATR=(13*priorATR+TR)/14`. Formally settle seed location vs retained-history length and test it independently.
4. `ATRP=100*ATR(14)/close` of the **latest complete MarketTrend candle**, not the last closed raw 5m candle from the still-forming higher-timeframe bar. Preserve actual source-data endpoint in `FeatureValueSnapshot`. Existing 5m diagnostic endpoint is not a substitute for a trend-duration endpoint.
5. Reject nonpositive or unrepresentable `TrendMinutes`, non-divisible by 5m source periods, absent exact endpoint, discontinuities, invalid OHLC, stale data, insufficient history, zero/nonfinite denominator and nonfinite results. Missing values stay unavailable, never zero.
6. **History minimum (ATR 14):** 2h=30h; 4h=60h; 8h=120h; 12h=180h; 24h=360h of *fully completed* trend candles. Check `StoreDataMaxHours`; do not silently extend retention, force refresh or substitute a shorter timeframe.
7. Keep implementation isolated and deterministic, using the current normalized `MarketDataStore` and existing feature registry/Monitor/trigger system. No new Binance API or parallel store. Maintain omitted-`Metric` legacy behavior.

## P1C-02 — trend-matched market MedianATRP

Calculate each asset ATRP at the *same MarketTrend timeframe and exact complete trend endpoint*, then compute the arithmetic median of valid per-asset ATRP values in the **actual Phase 0-resolved global universe** of that MarketTrend (not the SMS universe). Apply existing `MarketMetricCoverage`: at least `ceil(0.90*eligible)` valid assets, eligible population nonempty; missing/invalid/stale assets remain in the denominator. Correct odd/even median, sample counts, invalid reasons and source timestamp. No cross-trend mixing.

## Subsequent Phase 1C/1D metrics

`VolumeExpansion`, `MedianVolumeExpansion`, volatility breadth, volume-expansion breadth, volume concentration and correlations all derive their analytical windows from `MarketTrend.TrendMinutes`. For volume expansion compare the last fully closed trend window to the prior N **same-duration** closed trend windows; N is a count, not a second timeframe. Quote-volume concentration uses a complete current trend-sized window and exact eligible population. Correlation samples synchronized trend-sized returns, not a fixed 5m/15m indicator. Thresholds, N, precise registry names and native futures observation mapping remain open until explicitly specified.

## Verification and delivery

Use synthetic 5m data that forms multiple distinct user-defined MarketTrend intervals. Verify aggregation, 14-TR/Wilder expected values, insufficient history, gaps, stale data, boundary transitions, forming higher-timeframe candles, exact completed-bar denominator, alternate TrendMinutes, even/odd median, 90% coverage, and universe correctness. Run `dotnet build`, existing `Tests/Phase1AReadiness`, new Phase 1C tests, then initial/normal/idle TestMode raids before declaring runtime validation. The documentation-only correction itself has **no new code commit, build or runtime result**.

Application code changes, when undertaken, belong **only** on `phase1/market-data-foundation`. Further documents belong in this dedicated repository; preserve the prior roadmap and handoff for provenance.
