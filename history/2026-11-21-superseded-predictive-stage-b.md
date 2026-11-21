> **SUPERSEDED — REFERENCE ONLY. NOT A PTMAGIC METRIC-DEVELOPMENT GATE.**
> This previous report scored future-price prediction and LONG/SHORT trading proxies, which the project owner explicitly rejected as criteria for PTMagic. Its **NO-GO conclusions are withdrawn** and cannot approve or reject metrics. PTMagic metric development concerns accurate market-regime characterization only. This file is retained solely to preserve the earlier work and explain why it was rejected. Current authority: [November 21 metric catalogue disposition](../audits/2026-11-21-metric-catalogue-dispositions.md).

---

# PTMagic 2.10 — Stage B empirical incremental-value gate
**Date:** 2026-11-21. **Status:** Offline probe completed; not an authorization for any feature or repository change.

## Executive decision
**NO-GO for new path-efficiency and metric-history signals on present evidence.** This is an evidence-insufficiency decision, not proof that the information can never help trading. Do not implement a new metric, retention system, or trade rule based on these results.

- Native cache: 725 markets, **725/725 byte-identical** across GeorgeLong and GeorgeShort archives (the two files are not independent market samples).
- Observation source: four days of archived normalized closed five-minute candles, November 15–19, 2026. The length is the available diagnostic archive, **not an architectural retention target**.
- 10 user-configured MarketTrends discovered from the archive. 4 had enough chronological observations for the test; all others were explicitly marked insufficient.
- Addition of path efficiency improved held-out log loss in **3/8** tested side/horizon comparisons. Adding changes in existing market metrics improved **2/8** comparisons.
- The baseline classifier itself was close to chance or unstable (held-out AUC generally near or below 0.5), so no actual trading benefit or alpha is established.

## Falsifiable experiment
For each user-configured MarketTrend, use only completed native-source periods and only the existing metrics actually enabled in the archived configuration. The reference baseline includes relevant available returns, market breadth, dispersion, relative performance, volatility, quote-volume expansion and taker flow. These are reconstructed from the archive rather than replayed through the entire production engine.
Compare the baseline with (A) changes in prior already-calculated market metrics, (B) directional closed-candle path efficiency, and (C) both. Evaluate separately for LONG conditions with positive preceding return and SHORT conditions with negative preceding return.
The proxy target is the sign of the following same-length price return (LONG: positive, SHORT: negative), **not actual PT trades, realized PnL, or strategy invalidations**. Use expanding chronological forward-only holdouts, purge preceding uncompleted outcomes, a fixed regularized classifier and no parameter search. Compare **out-of-sample log loss**; negative Δ is improvement, positive Δ is deterioration. Correlated assets and shared events greatly reduce independent information.

## Recorded results
| Configured horizon | Side | Decision periods | Baseline AUC | Δ loss: path | Δ loss: prior metric changes |
|---|---|---:|---:|---:|---:|
| M15 (15m) | LONG | 381 | 0.509 | -0.00184 | +0.00867 |
| M15 (15m) | SHORT | 381 | 0.502 | -0.00058 | +0.00105 |
| M30 (30m) | LONG | 170 | 0.457 | +0.00108 | +0.00140 |
| M30 (30m) | SHORT | 170 | 0.498 | +0.00004 | +0.01157 |
| H1 (60m) | LONG | 74 | 0.412 | +0.00038 | +0.04404 |
| H1 (60m) | SHORT | 74 | 0.514 | +0.00115 | -0.00698 |
| H2 (120m) | LONG | 45 | 0.442 | +0.00028 | +0.03916 |
| H2 (120m) | SHORT | 45 | 0.431 | -0.00041 | -0.01245 |
| H4 (240m) | LONG | 2 | — | — | — |
| H4 (240m) | SHORT | 2 | — | — | — |
| H6 (360m) | LONG | 4 | — | — | — |
| H6 (360m) | SHORT | 4 | — | — | — |
| H12 (720m) | LONG | 1 | — | — | — |
| H12 (720m) | SHORT | 1 | — | — | — |
| H24 (1440m) | LONG | 0 | — | — | — |
| H24 (1440m) | SHORT | 0 | — | — | — |
| H48 (2880m) | LONG | 0 | — | — | — |
| H48 (2880m) | SHORT | 0 | — | — | — |
| H72 (4320m) | LONG | 0 | — | — | — |
| H72 (4320m) | SHORT | 0 | — | — | — |

The higher-duration rows lack sufficient source history and/or mature target observations under this **specific four-day archive**. This does not constrain possible user-defined MarketTrend durations, indicator lookbacks, or retention settings.

## Gate decision and next work
1. **Path efficiency:** mathematically distinct from endpoint returns, but not demonstrated to improve the directional continuation surrogate consistently. Do not create a production metric now.
2. **History of existing metrics:** valid for reconstructing past decision context, but the proposed prior-value deltas did not consistently improve this forward proxy. Do not build a general metric-history store on a speculative predictive claim.
3. **Executable liquidity:** remains a true source-information gap (spread, opposing depth, notional-specific impact). It cannot be measured from the OHLCV cache. This deserves a separately justified trading-decision and native-source feasibility test, not an automatic Phase 5 implementation.
4. **Actual trading usefulness:** would require independently defined LONG/SHORT entry, invalidation and execution tests; the present output is not evidence of strategy profitability. The next gate should be a specific trading need and a measurement that changes an actual entry/exit/risk decision.

## Reproduction and evidence limits
- Read-only inputs: `PTMagic-_data-GeorgeLong-2026-11-19T15-41-47Z.zip` and `PTMagic-_data-GeorgeShort-2026-11-19T15-41-48Z.zip`.
- Script: `stage_b_incremental_value.py`; machine-readable result: `stage_b_incremental_value_results.json`; compact table: `stage_b_gate_results.csv`.
- The script reads the archived `MarketTrendAnalytics.json` list of actual `TrendMinutes`, selected metric names and available history requirements; **no durations or retention targets are chosen as system defaults**.
- Model ingredients replicate relevant price/volume/taker calculations as a research approximation, **not a production exact-configuration replay of all 43 registered metrics**. No live Binance requests, database modifications, PT writes or GitHub updates occur.
- Very limited days, time-correlated symbols, one shared market sample, variation in sample completeness and surrogate outcome prevent a statistically reliable production recommendation. No confidence interval or claim of significance is inferred from the raw symbol count.