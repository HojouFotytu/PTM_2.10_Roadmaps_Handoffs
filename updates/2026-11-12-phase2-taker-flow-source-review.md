# PTMagic 2.10 — Phase 2 taker-flow source and architecture review

**Date:** November 12, 2026 (KST)  
**Status:** Source inspection completed; implementation design prepared. **No taker-flow source changes have been published, compiled, or validated.**  
**Baseline application:** `phase1/market-data-foundation` at `5938337e48196b0ee781db9de9709b23bee0c007` (documentation-only commits after the verified `e31635a1` runtime).  
**Scope:** PTMagic application only. Do not change, depend on, or cross over to personal LONG/SHORT analyzer/strategy/settings repositories.

## Confirmed existing code path

1. `Core/MarketAnalyzer/MarketData/BinanceKlineClient.cs` fetches existing 5m Binance klines and maps positions 0–8 into `MarketCandle`; source already contains `QuoteVolume` (kline index 7) and `TradeCount` (index 8). It currently **does not read kline index 9 (taker-buy base volume) or index 10 (taker-buy quote volume)**.
2. `MarketCandle` has OHLC, `BaseVolume`, `QuoteVolume`, `TradeCount`, timestamps and `IsClosed`; **no taker volume field**.
3. `MarketDataStore`, `MarketDataSeriesSnapshot`, and `MarketDataService` already enforce pinned timestamps, stored normalized candle snapshots, rolling retention, missing/gap checks and refresh overlap. These contracts should remain the only normalized source pipeline.
4. `TrendPeriodMetricsCalculator` aggregates closed 5m source candles into complete UTC-aligned `MarketTrend.TrendMinutes` bars for the existing volume indicators. It currently sums only total quote volume. Taker metrics must use exactly the same completed-period boundary and reject any missing required source candle.
5. `MarketDataWarmStartCache` uses binary schema **version 1**, serializing only OHLCV/trade count. Its restored records cannot establish historical taker-buy volume. This is the **main persistence/migration issue**; old cached OHLCV must not silently acquire fabricated taker values or appear fully valid for new metrics.
6. `MarketTrendMetrics` currently has 24 registered names; `MarketTrendAnalyticsEngine` merges independent per-asset feature results, `MarketTrendHistoryRequirements` describes OHLCV-backed retention, and the standard snapshot/trigger/export/Monitor pipeline already supports additional named asset metrics without a new Monitor or API subsystem.

**Consequence:** An economical, accurate taker-flow implementation is feasible from the **existing kline responses, with no new Binance requests per raid once the necessary source fields have been retained**. No separate taker-history client, quota allocator or independently scheduled collector is warranted.

## Proposed metric contracts — asset-scoped; only when explicitly enabled

For each **latest fully closed, UTC-aligned** `MarketTrend.TrendMinutes` period, sum all verified 5m **quote asset** volumes:

- `Q = sum(QuoteVolume)`
- `B = sum(TakerBuyQuoteVolume)`
- `S = Q − B`, provided every source observation is complete and satisfies `0 ≤ B_i ≤ Q_i`.
- **`TakerBuyRatio = B / Q`**, dimensionless, valid range **[0,1]**.
- **`TakerImbalance = (B−S)/Q = 2(B/Q)−1`**, dimensionless, valid range **[-1,1]**.

Use **ratio-of-sums**, never an unweighted average of per-candle ratios; the latter would overweight thinly traded candles. The two metrics are algebraically dependent. This is acceptable for distinct configuration/threshold convenience but they must **not** be represented as independent information sources in future composite conditions.

**Zero/missing semantics:** `Q <= 0`, unknown/null/invalid taker fields, out-of-range taker volume, non-finite values, unclosed/gapped/misaligned source periods, stale required source or insufficient retained history => **UNAVAILABLE**, not a fabricated zero or neutral `0.5`. Verified full data with `B=0` and `Q>0` yields valid buy ratio 0, imbalance -1; `B=Q` yields ratio 1, imbalance +1. Do not treat quote-volume 0 as a defined balanced market.

**Eligibility:** asset metrics, valid only on the configured frozen eligible asset population; no unintended global metric, static 5m TrendMinutes override, new mandatory lookback option, or restriction to a favorite higher timeframe.

## Proposed implementation sequence

1. **Raw mapper / model:** Add an optional taker-buy quote-volume field to `MarketCandle`; parse Binance kline index 10 without converting an absent/malformed value into valid zero. Preserve all existing OHLCV calculations and source validation.
2. **Persistence migration:** Extend `MarketDataWarmStartCache` with a safely versioned record format; prevent previous version-1 observations (which lack taker fields) from being interpreted as taker-complete. Prefer restoring v1 OHLCV for existing calculations while explicitly refreshing source history for newly enabled taker metrics. If this requires a one-time backfill, record its API and startup-duration cost; **do not silently delete old cache files or force all users into unnecessary cold starts**.
3. **Period calculator:** Sum verified taker-buy and total quote volumes over the exact latest complete MarketTrend period; keep the new calculator isolated from ATR/volume-expansion logic, using the same pinned source boundary.
4. **Registry / history:** Add two **asset-only** registry entries, with exact OHLCV source-retention requirements and normal trigger/reference semantics. The target catalogue rises from **24 to 26 names** (17 global-capable, **nine asset-only**). Funding remains unchanged and separately sourced.
5. **Integration / visibility:** Merge values and UNAVAILABLE reasons through the existing MarketTrend analyzer, SMS triggers, snapshots and Monitor export. Update existing tests and the single existing `Tests/Settings/settings.analyzer.json` in place; do not create a new analyzer folder/version subtree.
6. **Minimal correctness checks:** Parse complete/malformed kline forms, exact UTC-bar alignment, volume-weighting (ratio-of-sums), zero total, missing/gapped source, v1 cache migration, v2 cache restoration, and registry/scope consistency. Run a source-stamped solution build and directly affected focused checks. Defer broad synthetic/replay cycles and evaluate full-universe behavior using the eventual configured TestMode run.

## Migration, safety and performance decisions still to account for

- The existing cached 519-market OHLCV population represents a valuable warm-start baseline. A naïve cache schema bump that invalidates every v1 file would recreate the 13m34s cold history build observed on November 12. Avoid that where feasible; ensure no taker metrics become valid until source-confirmed fields are present.
- Cache save throttling currently prevents writes within its save window. A migration that populates newly needed taker history must ensure that a version-1 file cannot block persistence of upgraded content, otherwise repeated restarts may re-request source history.
- Preserve `BinanceFutures`, `Binance`, and `BinanceUS` dispatch; differentiate any provider-specific taker-field support transparently. Never claim unsupported exchanges have measured taker fields.
- Avoid extra Binance endpoints, settings knobs, changes to existing global/asset population semantics, or retroactive rewriting of historical decision snapshots.
- Monitor formatting, DashboardTop polling, startup SOM enable-only and PT delivery code are **out of scope** for this metric feature.

## Recommendation

Implement the two opt-in metrics directly in the normalized OHLCV path, taking special care with the existing v1 disk-cache migration and exact complete-period sums. **Do not publish a partial change that exposes metric names without reliable available/unavailable semantics, or that renders legacy cached candles spuriously valid.** New source changes require their own revision-stamped build and focused checks before calling this Phase 2 step implemented.

[Current technical roadmap](../roadmaps/CURRENT.md) · [D-053 validation](2026-11-12-d053-configured-testmode-validation.md)
