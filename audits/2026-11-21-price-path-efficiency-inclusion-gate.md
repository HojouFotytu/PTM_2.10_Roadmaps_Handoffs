# PTMagic 2.10 — Price-path efficiency: final regime-information inclusion gate

**Date:** November 21, 2026. **Status:** **PASS design inclusion** for one measurement family, with an asset output and a global-median output. **Design-gate status at audit creation:** this document alone did not authorize implementation. **Subsequent implementation:** source commit [49dd01f](https://github.com/HojouFotytu/PTMagic/commit/49dd01f438f1c75f88a8873ff8e86bc1738f8d9b), **build and LONG/SHORT TestMode runtime acceptance have now PASSED**; see the [2026-11-22 acceptance record](2026-11-22-price-path-efficiency-runtime-acceptance.md).

**Scope:** accurate **market-regime characterization** for arbitrary user-configured MarketTrend durations and retention. **Excluded:** ProfitTrailer performance, trading entries/exits, future-price prediction, profitability and forecasting scores. This audit supersedes only the *pending-inclusion status* for the two proposed path-efficiency names in the [earlier catalogue review](2026-11-21-metric-catalogue-dispositions.md).

## Decision

| Proposed registered metric | Scope | Disposition | Distinct market characteristic |
|---|---|---|---|
| **PricePathEfficiency** | Asset | **INCLUDE** | How directly an asset's **closed-candle price path** progressed from its first to last endpoint, regardless of bullish/bearish direction |
| **MedianPricePathEfficiency** | Global | **INCLUDE** | Typical path directness across the same fixed eligible market cohort; separately triggerable as a global regime characteristic |

These are **two outputs from one measurement family**, not two new data sources. They do **not** replace PriceTrend, ATRP, Breadth, Dispersion, taker flow or concentration.

### Measurement definition

For any eligible user-configured TrendMinutes T and source candle interval delta with N=T/delta full intervals, use **N+1 contiguous, fully closed, exactly timestamp-aligned and valid source closes** ending at the raid-pinned rolling endpoint, which is also the endpoint of current PriceTrend. Define:

E = abs( ln(C_N/C_0) ) / sum(i=1..N) abs( ln(C_i/C_(i-1)) ).

E is dimensionless in [0,1], ignoring rounding noise. It describes **path directness**, not trend strength or direction. Interpret alongside already existing signed PriceTrend and volatility context. E can be high for a tiny monotonic change, and low for a large net movement with substantial reversal travel.

**Validity:** N=1 yields E=1 whenever the endpoint changes and therefore has no path-discrimination value: return UNAVAILABLE with an explicit *insufficient independent path steps* explanation. N>=2 is a mathematical sufficiency requirement, **not a hardcoded MarketTrend duration**. All-zero movement produces 0/0 and is UNAVAILABLE (not fabricated zero). A return to the exact starting price after nonzero travel is valid E=0. Gaps, bad numbers, incomplete bars or missing timestamps are UNAVAILABLE, never interpolated.

**Fiat configuration:** where current PriceTrend converts quote prices into the configured Fiat units, evaluate the corresponding **time-aligned converted close path** or keep the result unavailable if the required conversion path is incomplete. Do not silently mix native-quote efficiency with Fiat price-direction context.

**Global result:** median of individually valid E over the actual configured frozen eligible cohort; retain numerator/eligible coverage and use the existing global minimum coverage contract. Flat/invalid assets cannot become invented zeros. Do not claim that a median describes turnover-weighted market leaders. Product must not assume any preselected T, history duration, universal E threshold, fixed number of market trends or external history database.

## Structural proof of non-redundancy

Consider two 60-minute sequences of **13 consecutive five-minute closes**, both beginning at 100 and ending at 103:

- Path A: monotonically increasing closes from 100 to 103. E=1.0000.
- Path B: 100, 106, 98, 105, 97, 103, 99, 102, 98, 104, 96, 102, 103. E=0.0445.

Set source-bar highs/lows so both sequences have the **same aggregate 60-minute OHLC** (open=100, high=108, low=95, close=103), quote/taker totals, completed-bar ATR inputs and identical earlier trend-bar endpoints. The existing return, completed-trend ATRP, relative/BTC measurements, price/flow sign classifications and turnover aggregates are then identical at that configured trend duration, **but E differs drastically**.

The distinction is a real descriptive dimension that the existing same-duration catalogue cannot reconstruct. A user may also configure shorter trends, but product availability cannot depend on assuming those trends exist or on doing arithmetic across metric triggers.

## Real-source verification (no future-return labels)

- **Archive:** PTMagic-_data-GeorgeLong-2026-11-19T15-41-47Z.zip, user-provided, 725 native v2 five-minute normalized symbol caches. This original ZIP is a user artifact, **not stored in this public documentation repository**.
- **Historical application source:** 55395eb55f940f6cbe0d5530051ae2a648373d, BinanceFutures TestMode, first recorded raid pinned at 2026-11-19 15:22:20.5042064 UTC. Latest required closed price endpoint: 15:19:59.999 UTC.
- **Audit implementation reference:** subsequent PTMagic branch source 146f56f80601b5ab34b06790d7f311872f037b7f, with the same metric calculation contracts cited below.
- Independent completed-period **ATRP reconstruction matched 2,163** existing first-raid diagnostic inputs; maximum absolute numerical deviation **1.07e-14**. The path metric was *not* present in PTMagic and was computed offline from the original source candles.
- Source-matched comparisons of **existing absolute return and ATRP** versus E (all simultaneously observed, no forward prices):

| Configured example | Symbols | Signed PriceTrend (%) | ATRP (%) | Path efficiency |
|---|---|---|---|---|
| 30 min | ENSO / ALAB | -1.2063 / -1.1452 | 1.2266 / 1.1630 | **1.0000 / 0.2068** |
| 60 min | IBM / TRX | -0.5464 / -0.6112 | 0.4776 / 0.3433 | **0.1062 / 0.7859** |

Within this one contemporaneous cross-section, Spearman rank correlations of E with |PriceTrend| were **0.744 at 30m, 0.701 at 60m and 0.861 at 240m**. These show **substantial overlap** with movement magnitude, especially for longer paths; E is not independent of return. Against existing ATRP the corresponding correlations were **-0.033, -0.089 and -0.048**. Similar price movement and ATRP can still conceal very different path directness.

### Separate global-median test

Using **49 hourly diagnostic snapshots** within the already archived period for each cited configured horizon, compare pairs with similar market-wide average PriceTrend, Breadth and Dispersion. For each pair, values below were recalculated on the **fixed intersection of valid markets**, to avoid attributing population changes to the new measurement:

| Configured example | Shared markets | Global median E at first / second time | Mean return (%) at first / second | Breadth (%) at first / second | Dispersion at first / second |
|---|---:|---|---|---|---|
| 30 min | 719 | **0.6332 / 0.3609** | -0.4855 / -0.4297 | 12.52 / 19.19 | 0.7426 / 0.7371 |
| 60 min | 724 | **0.1206 / 0.2499** | +0.2635 / +0.1875 | 60.50 / 64.92 | 1.0231 / 1.1537 |
| 240 min | 719 | **0.1697 / 0.2718** | -2.1650 / -2.2723 | 11.68 / 9.32 | 2.5925 / 2.5820 |

These are **descriptive contemporaneous contrasts**, not statistical proof of superior future regime selection. Neighboring snapshots overlap in time, the archive represents one market episode, and historical cohort membership was inferred from the available final population. Nevertheless, they demonstrate that the global median is **not simply a replacement for existing market-wide return, breadth or dispersion**. It is also necessary as a separate global output because PTMagic's GlobalSettings cannot perform a dynamic median of individual SMS metric values.

### Critical interpretation limits

1. **Source resolution:** this is efficiency of consecutive **closed candle prices**. It cannot see price reversals entirely hidden within a source candle. ATRP separately captures high/low excursions.
2. **Variable horizon:** E distributions change substantially with N; no universal comparison threshold across arbitrary MarketTrends. In this *diagnostic sample only*, median E was 1.000 at M15 and 0.0206 at H72. This does not prescribe either horizon or retention.
3. **Short paths:** with only a few close changes, E can saturate at 1. It describes measured close-to-close movement only, not exhaustive intrabar trend quality.
4. **Missing/flat sources:** preserve current three-valued UNAVAILABLE and global cohort/coverage behavior.
5. **Empirical scope:** one 2026-11-19 archive, not a multi-regime longitudinal acceptance study. Measurement correctness, source validity and nondeterministic runtime costs still require implementation-time checks.

## Next metric-development gate

**The question of whether to include these two metric names is resolved in favor of inclusion.** The next work item, if separately authorized, is focused product implementation: source-valid close-path calculation and median global aggregation using configured trends, Fiat alignment, exact validity, dependency selection, registry/GlobalSettings/SMS/Monitor/export support, and source-validity tests. Benchmark acquisition/CPU cost across both instances before source changes.

**No PTMagic code, existing metric, configuration, market rule, retention setting, or execution behavior was modified by this documentation-only result.**

## Evidence and reproducibility

- [Contemporaneous per-horizon statistical profile](evidence/2026-11-21-path-efficiency-inclusion-profile.csv) — horizon values describe only the archived user's configured diagnostic trends.
- [Matched asset examples](evidence/2026-11-21-path-efficiency-matched-assets.csv)
- [Market-wide controlled-cohort comparisons](evidence/2026-11-21-path-efficiency-global-comparisons.csv)
- [Reproducer for closed-candle path efficiency and global median](evidence/2026-11-21-price-path-reproducer.py) — accepts an original PTMagic _data ZIP; uses configured trend names and lengths from its snapshot.
- [Technical code reference: existing normalized return endpoint](https://github.com/HojouFotytu/PTMagic/blob/phase1/market-data-foundation/Core/MarketAnalyzer/MarketData/MarketTrendAnalyticsEngine.cs), [current ATRP calculation](https://github.com/HojouFotytu/PTMagic/blob/phase1/market-data-foundation/Core/MarketAnalyzer/MarketData/TrendPeriodMetricsCalculator.cs), [Fiat conversion](https://github.com/HojouFotytu/PTMagic/blob/phase1/market-data-foundation/Core/MarketAnalyzer/MarketData/MarketTrendFiatConversion.cs).
