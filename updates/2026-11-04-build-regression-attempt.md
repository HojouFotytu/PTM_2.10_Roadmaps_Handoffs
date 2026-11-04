# PTMagic 2.10 — Build/regression verification attempt

Date: 2026-11-04
Application repository: HojouFotytu/PTMagic
Branch: phase1/market-data-foundation
Cleanup commit: 08612fed2cb02746a433f5d96013d481d2816bc6
CI workflow commit: 40849bdce295ea703dad9a7a9691e61c97106fb7
Workflow: .github/workflows/phase1-regression.yml

## What was done

- Added a GitHub Actions .NET 10 Release build for PTMagic.sln and all six executable regression harnesses.
- Workflow triggers on pushes to the development branch affecting source, tests or its workflow, and supports manual workflow_dispatch.
- Minimal permissions: contents:read. No ProfitTrailer license, exchange API credentials or secrets supplied.
- Reviewed implementation changes and confirmed the cleanup commit is the parent of the workflow commit.

## Results and limitations

- The execution container lacks the .NET SDK ('dotnet: command not found').
- Its network cannot resolve github.com; no local checkout/restore/run was possible.
- GitHub Actions reported zero workflow runs after the workflow commit, so no CI build/test result exists at the time of this report. GitHub Actions may need to be enabled on the fork and/or a manual dispatch may be needed.
- Therefore NO PASS is claimed for compile, regression, live data or TestMode.
- No three-exchange TestMode execution was performed: it requires exchange network access, valid local PT configuration, and an environment that can read data safely.

## Next commands

In the repository root with .NET 10 SDK installed:

```sh
dotnet build PTMagic.sln --configuration Release
dotnet run --project Tests/Phase1AReadiness/Phase1AReadiness.csproj --configuration Release
dotnet run --project Tests/Phase1COhlcv/Phase1COhlcv.csproj --configuration Release
dotnet run --project Tests/Phase1MetricWarnings/Phase1MetricWarnings.csproj --configuration Release
dotnet run --project Tests/Phase1SmsSummaryIsolation/Phase1SmsSummaryIsolation.csproj --configuration Release
dotnet run --project Tests/Phase1TriggerLogic/Phase1TriggerLogic.csproj --configuration Release
dotnet run --project Tests/NormalizedPriceTrendMigration/NormalizedPriceTrendMigration.csproj --configuration Release
```

## Required TestMode acceptance, for each exchange

Set Application.TestMode=true and Application.Exchange to BinanceFutures, Binance or BinanceUS, with valid PT connectivity and a nonproduction/testing PT instance.

1. MarketTrend with Metrics omitted or empty has normalized global and per-asset PriceTrend.
2. Explicit PriceTrend and explicit metric-only trends compute requested metrics, with implicit PriceTrend when a blank-Metric trigger references that trend.
3. Omitted GlobalSetting Metric preserves thresholds, trigger logic and fail-closed handling of unavailable metrics.
4. Omitted SMS/OffTrigger Metric preserves Relative, Absolute, RelativeTrigger, activation snapshot price and 24-hour-volume semantics.
5. Verify ignored/allowed lists, MaxMarkets, TrendThreshold, eligible population, and BTC benchmark for quote currency.
6. Check old Market Analyzer, Monitor, and runtime summary fields display normalized values, without new settings being sent when active settings are unchanged.
7. Verify no CoinMarketCap API calls or legacy PriceTrend calculation occurs.
8. Explicitly evaluate TrendCurrency=Fiat legacy configurations: numerical parity with legacy calculated returns has not yet been demonstrated.

Do not mark #3 or #4 complete until actual build and TestMode evidence exists.
