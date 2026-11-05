# P1B/Unified PriceTrend — Migration compatibility audit

**State:** FIXES COMMITTED on d0b0b87 — local build and 88/88 tests PASS; nine-raid Binance Futures USDT live TestMode PASS; cross-quote Fiat/Spot/US/persistent OffTrigger still pending
**Date:** 2026-11-05
**App branch/commit:** HojouFotytu/PTMagic `phase1/market-data-foundation`, `0c31e58451a563406c214dee3438f0812e980ae6`
**Compared legacy source:** HojouFotytu/PTMagic `master` at time of audit
**Evidence scope:** code review + user's earlier local 82/82 passing tests and Futures TestMode. These results predate this audit and do NOT validate legacy parity in the following edge cases.

## P1: SMS Relative uses a capped global mean instead of uncapped SMS reference mean — CODE FIX COMMITTED

**Legacy:** `Core/Main/PTMagic.cs` on master, SMS activation near lines 1875–1917 and OffTrigger near 1688–1718: load the `SingleMarketTrendChanges[MarketTrendName]` for all selected assets, compute the arithmetic mean after excluding trend outliers (`TrendThreshold`), then `Relative = assetTrendChange - averageMarketTrendChange`. The `MaxMarkets` cap is applied to *global* trends in `BuildGlobalMarketTrends`, not the SMS relative average.

**Current:** `Core/MarketAnalyzer/MarketData/MarketTrendMetricTriggerResolver.cs` `TryResolveSingleWithRelation` calls `TryResolveGlobal` when relation is Relative. That returns the global `PriceTrend` from `MarketTrendAnalyticsEngine`, whose global universe was already restricted by `MarketTrendPopulationSelector.Select` to `MaxMarkets`. This changes SMS activation/OffTrigger comparisons.

**Deterministic counterexample:** BTC +10%, ETH +20%, `MaxMarkets=1` selects BTC globally. ETH Relative was +5 percentage points (20 − mean(10,20)); new code returns +10 (20 − global mean(10)). Trigger threshold +7 would change the decision.

**Remedy:** calculate/carry an uncapped, appropriate threshold-filtered SMS relative mean over the same normalized asset PriceTrend data; do not reintroduce legacy history ingestion. Document whether the 90% readiness rule must apply to this separate aggregate. Test both activation and OffTrigger; cover MaxMarkets=1, outlier threshold, missing/stale assets, and unbounded MaxMarkets.

## P1: TrendCurrency=Fiat silently becomes Market — CODE FIX COMMITTED

**Legacy:** `Core/MarketAnalyzer/BaseAnalyzer.cs` on master, `GetMarketTrendChanges` near lines 374–380: if `TrendCurrency=Fiat` and the USD value of main currency was available at both endpoints, multiply each quote-denominated price by its time-specific main-currency USD value. This is also described in the default settings.analyzer.json.

**Current:** `Core/MarketAnalyzer/MarketData/MarketTrendAnalyticsEngine.cs` `CalculateReturn` near lines 252–303 directly compares quote-denominated normalized closed-candle prices; no `TrendCurrency` branch or aligned main-quote/USD conversion is present. For a flat asset/BTC market and +10% BTC/USD, the old Fiat trend is +10%, but normalized returns 0%.

**Remedy:** either implement coherent as-of-aligned fiat conversions for each supported quote and exchange, or reject unsupported Fiat PriceTrend with clear metric-warning diagnostics. Do not silently substitute Market returns. Add Market-vs-Fiat parity tests with changing quote/USD conversion prices and missing conversion series. USDT-only live tests do not establish this behavior.

## P2: TrendThreshold influences every metric via shared global population — CODE FIX COMMITTED

`MarketTrendPopulationSelector.Select` applies `TrendThreshold` filtering to the global symbol list before `MarketTrendAnalyticsEngine.Calculate`, which reuses the same list for Breadth, MedianPriceTrend, Dispersion, Concentration, Phase1C quote-volume metrics and PriceTrend. Historical `TrendThreshold` affected the arithmetic PriceTrend mean; current default settings still say 'outlier ... not used when calculating market average'. The Phase1 design also emphasizes sharing the exact selected population. **Resolve the policy explicitly** rather than assuming the original or new behavior wins, then test representative high-return symbols for both price and volume metrics.

## P2: Source resolution changes supported TrendMinutes

`MarketTrendAnalyticsEngine.CalculateReturn` demands an exact 5m closed endpoint and a reference close exactly `TrendMinutes` earlier. Legacy trend values of 1–4 minutes or other non-5m multiples cannot be represented. D-016 explicitly adopts normalized 5m source constraints; this is not a violation of that accepted new contract, but backward compatibility must acknowledge it. Validate configured durations upfront, and provide a meaningful warning rather than silently unavailable values.

## Other follow-ups

- **Historical graph continuity:** `Core/Main/PTMagic.cs` `SaveRuntimeSummary` merges stored `MarketTrendChanges` from previous versions with new normalized observations under the same trend name. Browser chart rendering and a migration boundary have not been directly verified.
- **Decision-time freshness:** Pinned as-of time resolves the prior startup mixed-candle defect but can leave a newly completed candle unevaluated on a long refresh; follow-up raids correct this. Decide whether actions should wait for a freshness check or use a bounded catch-up refresh.
- **Legacy startup load:** `BinanceAnalyzerCommon.GetMarketDataAsync` still calls `CheckForMarketDataRecreationAsync`, creating expensive legacy tick history despite PriceTrend using normalized candles. Verify other consumers before removing it.
- **Stale log/UI text:** `Monitor/Pages/MarketMetrics.cshtml.cs` says blank Metrics retains *legacy* PriceTrend; `BinanceFuturesAnalyticsRuntime` StoreDataMaxHours warning likewise claims legacy PriceTrend continues.
- **Population choice:** `UseProfitTrailerEnabledPairs=false` intentionally selects broad exchange-wide eligible markets; compared with old `MarketList` behavior this may change mean values. Validate that users knowingly opt into the policy.
- **Unverified live acceptance:** Binance Spot, Binance US, TrendCurrency=Fiat, positive threshold-crossing SMS OffTrigger deactivation, original Market Analyzer browser chart.

## Tests missing in the current migration harness

`Tests/NormalizedPriceTrendMigration/Program.cs` has 12 cases including omitted/explicit Metrics, 90% coverage, incomplete source candle, MaxMarkets global-vs-asset population, BTC benchmark and exchange-name routing. It does **not** assert the SMS `Relative` calculation under MaxMarkets, `Fiat` conversion, or real activation-to-OffTrigger transitions. Existing 82/82 passing tests do not prove these untested semantics. Previous 3,116 asset-value comparisons were normalized exports against normalized summaries, not legacy vs normalized calculations.

## Exit conditions before declaring compatibility complete

1. Correct SMS Relative reference-population semantics and run deterministic activation/OffTrigger tests.
2. Implement or explicitly fail-close Fiat PriceTrend, update documentation, and verify on a relevant non-USDT quote.
3. Review and decide TrendThreshold's applicability to non-PriceTrend global metrics.
4. Re-run local .NET 10 build and all six existing regression harnesses plus any newly created tests (D-021/D-022), then TestMode.
5. Mark compatible only for the actually supported exchanges/configurations; remaining cases stay documented as limitations.


## Implementation update — 2026-11-05

User explicitly decided to **retain TrendThreshold for PriceTrend means only**, not remove it. The P2 recommendation to eliminate the setting is superseded.

Application commit [d0b0b87](https://github.com/HojouFotytu/PTMagic/commit/d0b0b877d6157b0db44cc4d1d2ac4b0cb0799abc):
- Uncapped `SmsRelativePriceTrend` feature with threshold-adjusted reference and 90% coverage policy; used for SMS Relative activation and OffTrigger.
- Aligned Fiat conversion via `MarketTrendFiatConversion`, requiring quote/USDT candle series except for USD/USDT quotes; absence fails closed.
- `TrendThreshold` filters only PriceTrend arithmetic mean calculations, not global population or the other metrics.
- `MarketTrendTimeframe` validates positive five-minute multiples before exchange history ingestion and within analytics.
- Added six tests, making the migration harness 18 and six-harness expected total 88; updated Monitor/defaults guidance.

**Status:** No .NET build/test or live-run result has been supplied for this commit. A PASS for the prior 82 tests does not establish that the new 88 pass. Further parity acceptance remains necessary.


## Verification update — 2026-11-05

User's `dotnet build` succeeded for Core, PTMagic and Monitor (.NET 10). The six deterministic test suites passed **88/88**: 5 + 13 + 5 + 29 + 18 + 18. Only eight nonfatal nullable-reference warnings remain in two test projects. This verifies the newly added deterministic compatibility test cases but does not replace non-USDT Fiat and actual SMS Relative/OffTrigger live TestMode acceptance on all three Binance exchanges. No source changes are needed to record this test outcome.


## Live validation — 2026-11-05

Nine completed Binance Futures TestMode raids plus independent exported snapshot checks support the SMS Relative uncapped benchmark, PriceTrend-only threshold, normalized snapshot parity, USDT-quote Fiat identity, and working true OffTrigger path with immediate reactivation. Details: [2026-11-05 nine-raid test report](../updates/2026-11-05-price-compatibility-nine-raid-testmode.md). Non-USDT Fiat and sustained OffTrigger deactivation remain unverified; do not close those acceptance items.
