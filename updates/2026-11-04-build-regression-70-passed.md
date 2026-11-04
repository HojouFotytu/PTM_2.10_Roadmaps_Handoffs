# PTMagic 2.10 — Release build and regression verification SUCCESS

Date: 2026-11-04
Application repository: HojouFotytu/PTMagic
Branch: phase1/market-data-foundation
Source cleanup commit: 08612fed2cb02746a433f5d96013d481d2816bc6
Validation workflow setup commit: 40849bdce295ea703dad9a7a9691e61c97106fb7
Validation workflow fix commit: 8ff8c87900aa6f56c8721444dd11f0885c99ac3d
Successful GitHub Actions run: https://github.com/HojouFotytu/PTMagic/actions/runs/41836826883
Job ID: 126597788189

## Verified results (GitHub Actions, .NET 10)

- Release build of PTMagic.sln: SUCCESS
- Phase1AReadiness: 4/4
- Phase1COhlcv: 13/13
- Phase1MetricWarnings: 7/7
- Phase1SmsSummaryIsolation: 5/5
- Phase1TriggerLogic: 29/29
- NormalizedPriceTrendMigration: 12/12
- TOTAL: 70/70

Initial CI attempt failed due to absent runtime-only settings.general.json and settings.analyzer.json in PTMagic/. CI was fixed to copy the tracked example settings files into the runner before building. No private credentials were used.

Warnings: nullable reference checks in Tests/Phase1SmsSummaryIsolation/Program.cs and Tests/NormalizedPriceTrendMigration/Program.cs. No errors or failing tests.

## Scope and remaining acceptance

Outstanding #3 (build and regression tests): DONE, as of the successful workflow run.

Outstanding #4 (TestMode on BinanceFutures, Binance and BinanceUS): NOT VERIFIED. The GitHub CI environment did not run PTMagic against ProfitTrailer or live Binance exchange endpoints. It runs offline tests only.

Three exchange TestMode runs remain necessary to verify:
- Default and explicit normalized PriceTrend.
- Implicit GlobalSetting and SMS triggers using existing thresholds and relations.
- Market universe filtering, global averages and per-asset return populations.
- Existing Monitor, summary and settings compatibility.
- Previously used TrendCurrency=Fiat configurations (numerical equivalence not yet demonstrated).

Phase 1D remains unstarted by this work. No claims are made that the three exchange TestMode checks have passed.

The prior report updates/2026-11-04-build-regression-attempt.md records the initial execution environment limitation and an earlier state before GitHub Actions ran. This document supersedes its build/test status.
