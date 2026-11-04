# PTMagic 2.10 — Pinned refresh time for normalized candles

Date: 2026-11-05
Application commit: 0c31e58451a563406c214dee3438f0812e980ae6
Application branch: phase1/market-data-foundation

## Defect reproduced in user TestMode logs

The initial 756-market Binance Futures normalized kline refresh crossed a five-minute candle boundary. After the refresh completed, MarketTrend evaluation required the newly closed candle for every symbol, although markets fetched earlier could not yet have that candle. This caused 31 first-raid metric warning groups, 71.6% global return coverage, and false MissingEndpoint errors. The second raid refreshed affected assets, restored 100% coverage, and reduced warnings to seven intentional diagnostic cases.

## Source changes

- `Core/MarketAnalyzer/MarketData/MarketDataService.cs`: accepts optional `refreshAsOfUtc` and uses it for per-market incremental refresh decisions rather than an independent clock read.
- `Core/MarketAnalyzer/MarketData/BinanceFuturesAnalyticsRuntime.cs`: captures UTC timestamp immediately before refresh, stores it for the active raid, and passes the same as-of time to global population selection and MarketTrend metric calculation. Logs the pinned reference timestamp. Resets the timestamp when beginning a new refresh/exchange switch.
- `Tests/Phase1AReadiness/Program.cs`: adds asynchronous deterministic test using early and late market responses across the five-minute boundary, verifies full pinned coverage, reproduces false coverage failure under the later clock, and confirms later raid advances normally.
- `Tests/Phase1AReadiness/README.md`: updated test scope.

No intentional changes to trigger semantics, metric formulas, selected market eligibility policy, ProfitTrailer writes, or API rate limits. Applies to Binance Futures, Binance Spot and Binance US, all through the shared runtime.

## Required user-local verification (D-021)

From the PTMagic repository root in PowerShell:

```powershell
git pull --ff-only
dotnet build
dotnet run --project Tests/Phase1AReadiness/Phase1AReadiness.csproj
dotnet run --project Tests/Phase1COhlcv/Phase1COhlcv.csproj
dotnet run --project Tests/Phase1SmsSummaryIsolation/Phase1SmsSummaryIsolation.csproj
dotnet run --project Tests/Phase1TriggerLogic/Phase1TriggerLogic.csproj
dotnet run --project Tests/NormalizedPriceTrendMigration/NormalizedPriceTrendMigration.csproj
dotnet run --project Tests/Phase1MetricWarnings/Phase1MetricWarnings.csproj
```

Expected: Phase1AReadiness **5/5**, Phase1COhlcv **13/13**, SMS Summary Isolation **5/5**, Phase1TriggerLogic **29/29**, NormalizedPriceTrendMigration **12/12**, Phase1MetricWarnings **18/18**, total **82/82**. These are expectations, not executed results.

Then run a new Binance Futures TestMode cold start spanning a five-minute close. Inspect the new log line `normalized MarketTrends evaluate as of ... (pinned to kline refresh start)`, confirm first-raid global/asset return endpoint coverage, and verify no extra temporary MissingEndpoint failures. Verify Spot and US when available. No GitHub Actions build or remote test execution should be initiated.

## Acceptance limitations

This change only addresses clock consistency. Genuine missing source candles, incomplete stored history (e.g., 8h indicators with 96h retention), eligibility exclusions, global-metric scope errors, and Binance rate-limit delays remain possible and should still fail closed. It does not add persistent on-disk OHLCV caching.
