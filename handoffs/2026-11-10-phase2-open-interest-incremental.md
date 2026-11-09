# PTMagic 2.10 — Phase 2 OI incremental metric integration handoff

**Date:** November 10, 2026  
**Application:** `HojouFotytu/PTMagic`, branch `phase1/market-data-foundation`  
**Latest deterministic-tested source:** `5f51faaa0db928cf33c52f6f93ca6f1b301735fb`  
**Status:** source build and **315/315 offline regression groups PASSED** at the exact tested SHA; live Binance acquisition and other configured integration acceptance remain pending. Only the specific remaining Phase 1 configured integration checks were deferred.

## November 10 — Executed verification PASS

The owner ran the full fail-fast offline validation on Windows with .NET SDK 10.0.403 at source `5f51faaa0db928cf33c52f6f93ca6f1b301735fb`. Core, PTMagic and Monitor built in **11.3s**. **15/15 harnesses and 315/315 case groups passed**, including **18 raw OI + 17 incremental OI**. Eight nonfatal nullable-analysis warnings were emitted by two pre-existing test projects. See [full evidence](../updates/2026-11-10-phase2-oi-offline-validation.md). This completes deterministic OI development acceptance at the tested SHA; it does not establish live Binance, PT API, or Monitor/browser acceptance.

## Mandatory Phase 2 build and regressions (D-045)

Only the specific remaining Phase 1 configured PT/API/Monitor/browser acceptance was deferred. The Phase 2 .NET build, raw OI and incremental OI offline tests and affected regression harnesses remain **required now**. **Completed November 10:** their results are PASS at `5f51faa`; future source changes require new evidence.

Run the repository's `Tests/Phase2OpenInterestIncremental/Run-Phase2Validation.ps1` or the complete PowerShell block below. This runner performs ordinary offline build/harness work only; it does not start PTMagic against configured PT or write settings. Record the exact Git source SHA and the results. Do not resume the separately deferred Phase 1 integration cases as part of this test.

## Scope and architecture

Phase 2 is strictly application market-analysis development. No personal LONG/SHORT strategy development or PT preset manipulation is part of this handoff. The earlier [Phase 2 initial raw-data handoff](2026-11-10-phase2-open-interest.md) remains historical.

The first open-interest batch introduced typed current/history Binance USD-M observation mapping and offline fixtures. The second batch builds the opt-in acquisition, persistent cache, per-asset metrics, selection, and diagnostics around that foundation.

Files added:
- `Core/MarketAnalyzer/MarketData/FuturesOpenInterestDataService.cs`: bounded, fair, incremental historical source collection with a request cap and exact UTC pin.
- `Core/MarketAnalyzer/MarketData/FuturesOpenInterestDiskCache.cs`: versioned compressed per-symbol cache, validate-before-reuse, bounded capacity, atomic writes and recovery from corruption.
- `Core/MarketAnalyzer/MarketData/FuturesOpenInterestFeatureEngine.cs`: exact two-endpoint percent changes in native OI quantity and separately provider-reported OI value.
- `Tests/Phase2OpenInterestIncremental/`: 15 new offline test groups for request budgets, fairness, pagination, cache restart, missing data, scope and metric integration.

Updated registry, analyzer configuration model/default templates, source-independent history requirements, error diagnostics, runtime orchestration, and existing metric/export/trigger path. No new alternate expression language.

## Corrected MarketTrend-derived OI history

The independent `OpenInterestRetentionHours` setting and 672-hour cap have been **removed**. Enabled OI MarketTrends determine the required history: each needs its exact `TrendMinutes` interval, a reference observation, and a small overlapping repair window. The collector holds the longest duration required across configured OI-enabled Exchange MarketTrends, including different per-MarketTrend values. `StoreDataMaxHours` still applies to OHLCV, not OI. Provider history may have a shorter availability window: in that case OI is unavailable and the application does not shorten the requested trend.

Monitor History Requirements shows the user's trend-derived requirement separately from OHLCV capacity. The 72-hour/672-hour limits described in the superseded implementation have no effect. The retained `OpenInterestMaxRequestsPerRaid` budget controls request volume, not retention. Source validation was subsequently **executed and passed** at `5f51faa`.

## Configuration

```json
"MarketAnalyzer": {
  "OpenInterestMaxRequestsPerRaid": 60
}
```

Example explicit MarketTrend field (not configured by default):

```json
"Metrics": "OpenInterestChange,OpenInterestValueChange"
```

The first metric is the percentage change of native `sumOpenInterest`. The second is the percentage change of the Binance-reported `sumOpenInterestValue`. Both are **asset-scoped**, percentage values, requiring synchronized exact historical 5m endpoints. They are not global aggregate metrics and cannot be referenced in a GlobalSetting's asset-free metric context. A blank Metrics selection still means PriceTrend, not derivatives.

**Network policy:** Only explicitly requested OI on Binance USD-M Futures enables collection. Default limit is 60 requests per raid, hard maximum 400; no single request has more than 500 records; two pages maximum per asset in any one raid. The collector is serialized and reuses the existing Binance HTTP rate limiter. It favors least-recently serviced symbols and incremental gaps rather than full historical downloads on every raid. An incomplete series stays unavailable. `0` disables acquisition.

**Retention policy:** Historical OI is independent of normalized OHLCV `StoreDataMaxHours`; its required duration is computed from the longest enabled OI MarketTrend. Binance's approximately one-month history window remains a source availability constraint, not an application retention limit. No fabricated history, proxy notional, arbitrary value conversion or fallback to Spot/US data.

## Acceptance status, limits, and upcoming phase

The incremental suite has 17 groups (expanded from the original 15), and the raw suite has 18. **Both passed: 35/35 new Phase 2 groups.** The full 15-harness deterministic run passed **315/315**, and the .NET build succeeded at exact source `5f51faa`. No live exchange run, actual PT API action, Monitor browser acceptance or configured performance benchmark is claimed. The existing Phase 1 acceptance and operational runtime testing remain deferred as directed.

The next feature batch should add the separate raw funding rate family and then distinct account/position ratio data, maintaining documented provider history and sampling contracts. Phase 2B market-wide aggregation follows raw family verification, and Phase 4 exposure through the existing metric/trigger/export pipeline is continuous. Keep general performance work deferred.

## Full local PowerShell verification (for future source revisions)

Run from the PTMagic application repository, not the roadmap repository:

```powershell
git switch phase1/market-data-foundation
if ($LASTEXITCODE -ne 0) { throw "Branch switch failed" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull failed" }
git rev-parse HEAD

$checks = @(
  ".\Tests\Phase2OpenInterest\Phase2OpenInterest.csproj",
  ".\Tests\Phase2OpenInterestIncremental\Phase2OpenInterestIncremental.csproj",
  ".\Tests\Phase1DCorrelation\Phase1DCorrelation.csproj",
  ".\Tests\Phase1AnalyticsReliability\Phase1AnalyticsReliability.csproj",
  ".\Tests\TriggerConfigurationValidation\TriggerConfigurationValidation.csproj",
  ".\Tests\Phase1MetricWarnings\Phase1MetricWarnings.csproj"
)

dotnet build .\PTMagic.sln
if ($LASTEXITCODE -ne 0) { throw "Build failed" }

foreach ($check in $checks) {
  Write-Host "Checking $check"
  dotnet run --project $check
  if ($LASTEXITCODE -ne 0) { throw "FAIL: $check" }
}
```

The full 15-harness offline runner has already executed successfully at `5f51faa`. This command block remains for future source changes; do not rerun solely to reconfirm that recorded result. Configured Phase 1 integration testing is deferred separately.

[Current technical roadmap](../roadmaps/CURRENT.md) · [current status](../STATUS.md) · [decision register](../DECISIONS.md).
