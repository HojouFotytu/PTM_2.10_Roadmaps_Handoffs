# PTMagic 2.10 — Phase 2 OI incremental metric integration handoff

**Date:** November 10, 2026  
**Application:** `HojouFotytu/PTMagic`, branch `phase1/market-data-foundation`  
**Source checkpoint:** `b723f76664aa0de6b76de3f5ddf281c036c32275`  
**Status:** source published; build and tests not executed because further testing was deferred.

## Scope and architecture

Phase 2 is strictly application market-analysis development. No personal LONG/SHORT strategy development or PT preset manipulation is part of this handoff. The earlier [Phase 2 initial raw-data handoff](2026-11-10-phase2-open-interest.md) remains historical.

The first open-interest batch introduced typed current/history Binance USD-M observation mapping and offline fixtures. The second batch builds the opt-in acquisition, persistent cache, per-asset metrics, selection, and diagnostics around that foundation.

Files added:
- `Core/MarketAnalyzer/MarketData/FuturesOpenInterestDataService.cs`: bounded, fair, incremental historical source collection with a request cap and exact UTC pin.
- `Core/MarketAnalyzer/MarketData/FuturesOpenInterestDiskCache.cs`: versioned compressed per-symbol cache, validate-before-reuse, bounded capacity, atomic writes and recovery from corruption.
- `Core/MarketAnalyzer/MarketData/FuturesOpenInterestFeatureEngine.cs`: exact two-endpoint percent changes in native OI quantity and separately provider-reported OI value.
- `Tests/Phase2OpenInterestIncremental/`: 15 new offline test groups for request budgets, fairness, pagination, cache restart, missing data, scope and metric integration.

Updated registry, analyzer configuration model/default templates, source-independent history requirements, error diagnostics, runtime orchestration, and existing metric/export/trigger path. No new alternate expression language.

## Configuration

```json
"MarketAnalyzer": {
  "OpenInterestRetentionHours": 72,
  "OpenInterestMaxRequestsPerRaid": 60
}
```

Example explicit MarketTrend field (not configured by default):

```json
"Metrics": "OpenInterestChange,OpenInterestValueChange"
```

The first metric is the percentage change of native `sumOpenInterest`. The second is the percentage change of the Binance-reported `sumOpenInterestValue`. Both are **asset-scoped**, percentage values, requiring synchronized exact historical 5m endpoints. They are not global aggregate metrics and cannot be referenced in a GlobalSetting's asset-free metric context. A blank Metrics selection still means PriceTrend, not derivatives.

**Network policy:** Only explicitly requested OI on Binance USD-M Futures enables collection. Default limit is 60 requests per raid, hard maximum 400; no single request has more than 500 records; two pages maximum per asset in any one raid. The collector is serialized and reuses the existing Binance HTTP rate limiter. It favors least-recently serviced symbols and incremental gaps rather than full historical downloads on every raid. An incomplete series stays unavailable. `0` disables acquisition.

**Retention policy:** Historical OI is independent of normalized OHLCV `StoreDataMaxHours`; maximum 672h (28 days) stays inside Binance's approximately 30-day history window. No fabricated history, proxy notional, arbitrary value conversion or fallback to Spot/US data.

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
