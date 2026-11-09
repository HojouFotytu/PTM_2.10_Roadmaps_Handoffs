# PTMagic 2.10 — Phase 2 OI incremental metric integration handoff

**Date:** November 10, 2026  
**Application:** `HojouFotytu/PTMagic`, branch `phase1/market-data-foundation`  
**Source checkpoint:** `0ae76f4c7886397a06ad346b42a375f6aa06be00`  
**Status:** source published; normal Phase 2 build and regression tests are required and pending. Only the separate remaining Phase 1 configured integration tests were deferred.

## Mandatory Phase 2 build and regressions (D-045)

Only the specific remaining Phase 1 configured PT/API/Monitor/browser acceptance was deferred. The Phase 2 .NET build, raw OI and incremental OI offline tests and affected regression harnesses remain **required now**. Their results are still pending; the new source must not be labelled compiled or accepted.

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

Monitor History Requirements shows the user's trend-derived requirement separately from OHLCV capacity. The 72-hour/672-hour limits described in the superseded implementation have no effect. The retained `OpenInterestMaxRequestsPerRaid` budget controls request volume, not retention. Source-only validation has been extended, but **not executed**.

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

All 15 new incremental test groups plus the previous 18 raw-data groups are authored, but **have not been executed**. No build, live exchange run, PT API action, Monitor browser exercise, or performance benchmark is claimed. The existing Phase 1 acceptance and operational runtime testing remain deferred as directed.

The next feature batch should add the separate raw funding rate family and then distinct account/position ratio data, maintaining documented provider history and sampling contracts. Phase 2B market-wide aggregation follows raw family verification, and Phase 4 exposure through the existing metric/trigger/export pipeline is continuous. Keep general performance work deferred.

## Full local PowerShell verification (when testing resumes)

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

The script is a retained local acceptance instruction, not a request to perform the deferred testing immediately. When tests do run, record source SHA and actual outcomes before promoting acceptance.

[Current technical roadmap](../roadmaps/CURRENT.md) · [current status](../STATUS.md) · [decision register](../DECISIONS.md).
