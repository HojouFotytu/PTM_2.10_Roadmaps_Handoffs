# PTMagic 2.10 — PriceTrend compatibility restoration handoff

Date: 2026-11-05
App: HojouFotytu/PTMagic, `phase1/market-data-foundation`
Commit: `d0b0b877d6157b0db44cc4d1d2ac4b0cb0799abc`
Validation state: **source committed, local verification pending**

## Intent and accepted decision

Restore the historical semantics that are still meaningful while keeping a single normalized OHLCV architecture.

1. **SMS Relative**: use the mean of uncapped eligible asset PriceTrend returns, not the `MaxMarkets`-capped global mean. A single normalized snapshot carries `SmsRelativePriceTrend`; both SMS activation and OffTrigger resolve through it. If enough valid asset data is not present, leave triggers unavailable.
2. **Fiat**: restore `TrendCurrency=Fiat` with synchronized current/reference asset and quote/USDT candles, so a flat asset/BTC and +10% BTC/USDT produces +10% fiat PriceTrend. The quote conversion must not enter eligible market statistics. USD and USDT quote currencies use a 1:1 USD-unit convention consistent with the former implementation. Missing conversion produces unavailable measurements instead of arbitrary results. Applies to the shared normalized runtime for Binance Futures/Spot/US.
3. **TrendThreshold**: **retained**, not removed. Filter only arithmetic PriceTrend mean outliers for global PriceTrend and uncapped SMS-relative reference means. Do not remove those markets from `GlobalSymbols`; other metrics' medians, breadth, dispersion, volume, concentration, and MeanMedianSpread must not change from the threshold rule. `TrendThreshold=0` disables this filter. Existing property name remains valid.
4. **TrendMinutes**: reject `TrendMinutes<=0` and any non-multiple of 5 for Exchange MarketTrends; do not silently round or choose nearby candles. Validation before network startup and inside direct calculations includes trend name and an actionable message.

## Code touched

- `Core/MarketAnalyzer/MarketData/MarketTrendAnalyticsEngine.cs`
- `Core/MarketAnalyzer/MarketData/MarketTrendMetricTriggerResolver.cs`
- `Core/MarketAnalyzer/MarketData/MarketTrendPopulationSelector.cs`
- `Core/MarketAnalyzer/MarketData/MarketTrendFiatConversion.cs` (new)
- `Core/MarketAnalyzer/MarketData/MarketTrendTimeframe.cs` (new)
- `Core/MarketAnalyzer/MarketData/BinanceFuturesAnalyticsRuntime.cs`
- `Core/Main/PTMagic.cs`; `Core/DataObjects/PTMagicData.cs`
- Monitor MarketTrends input help, MarketMetrics tooltip, defaults and DevSettings descriptions
- `Tests/NormalizedPriceTrendMigration/Program.cs` and README: 18 migration test cases.

## Required PowerShell regression execution — user-owned (D-021)

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

Expected **88 tests**: 5 + 13 + 5 + 29 + 18 + 18. Build/test results have NOT been observed yet; correct any failures before concluding the work.

## Live acceptance requirements

- A Binance Futures TestMode run with current normalized settings; verify zero unexpected metric failures and correct GlobalSetting/SMS decisions.
- Test `MaxMarkets` smaller than the SMS eligible population with `Relative` trigger/OffTrigger; verify the SMS relative benchmark is the uncapped mean.
- Fiat on a quote such as BTC with an available aligned `BTCUSDT` market; verify the quote conversion data fetch (and its failed/missing behavior), and note that the exchange must actually list the conversion pair. USD/USDT quotes remain identity conversion.
- Binance Spot and Binance US parity still require live tests. Positive OffTrigger deactivation remains separately necessary.
- Check `TrendMinutes=61` in configuration emits an explicit validation error and does not begin historical recreation.
- Review any old stored Monitor chart values for mixed legacy/normalized history separately.

The local benchmark runs and external integration are **not** performed by the assistant.
