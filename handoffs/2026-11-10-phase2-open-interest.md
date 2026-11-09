# PTMagic 2.10 — Phase 2 open-interest foundation handoff

**Date:** November 10, 2026  
**Application:** `HojouFotytu/PTMagic`, branch `phase1/market-data-foundation`  
**Source checkpoint:** `314214b1a20bcddd1643b8fa8df032db5463b04d`  
**Status:** Historical first source slice; superseded as the active handoff by [incremental integration](2026-11-10-phase2-open-interest-incremental.md). No local .NET build or offline harness was executed for the first slice.

## Current scope and disposition

The owner instructed the project to move into Phase 2 and **defer further Phase 1 runtime, PT API, Monitor/browser and restart acceptance testing**. This is a scheduling deferral, not an acceptance claim or a waiver of eventual release gates. Existing evidence is retained in `STATUS.md` and `updates/2026-11-09-reused-configured-testmode-evidence.md`.

Phase 2 addresses PTMagic market-analysis data, not personal trading strategy or ProfitTrailer property-trio development. Existing normalized analytics and configuration behavior remain unchanged by the first source slice.

## Phase 2 first published slice

- `Core/MarketAnalyzer/MarketData/FuturesOpenInterest.cs`: typed Binance USD-M native current and historical observations; preserve `sumOpenInterest` and `sumOpenInterestValue` separately; strict symbol/timestamp/decimal fields; no interpolation or current/history splicing; exact 5-minute endpoint percent-change calculation.
- `Core/MarketAnalyzer/MarketData/BinanceFuturesOpenInterestClient.cs`: opt-in current OI and single historical page requests using existing shared HTTP/rate-limit/retry transport; no automatic refresh, fan-out, or changes to raids.
- `Tests/Phase2OpenInterest/`: 18 deterministic offline case groups authored; execution and compile status are **not verified**.

Relevant provider endpoints: `GET /fapi/v1/openInterest` and `GET /futures/data/openInterestHist`; historical endpoint periods and row limit are explicit. Historical retention is limited by the provider; source data availability must remain independent of `StoreDataMaxHours` configured for normalized OHLCV.

## Next source-only development

1. Add an **opt-in, bounded derivatives observation service** using pinned raid timestamps, symbol eligibility, cache/reuse, explicit endpoint budgets and availability diagnostics; avoid per-symbol full reload each raid.
2. Wire requested per-asset `OpenInterestChange` into the Metric registry, engine, exports, and triggers with transparent scope and units. Historical 5-minute data are independent of existing OHLCV; absent OI remains UNAVAILABLE. Binance Spot and Binance US do not receive futures OI.
3. Add raw funding, account/position ratio, and taker-flow adapters using individually verified provider contracts, then Phase 2B aggregates and Phase 3 derived states.
4. Integrate each feature across inspection/Monitor and decision history through the existing metric flow.

**Not yet done:** raw OI collection on ordinary raids, a live 30-day horizon or rate-limit experiment, any new selectable OI metric, Phase 2B aggregates, and any tests executed against new source. These are intentionally not claimed.

## Local verification command for a later test window

Owner testing is deferred. Preserve this fail-fast script for when testing resumes; it is not a request to run tests now.

```powershell
git switch phase1/market-data-foundation
if ($LASTEXITCODE -ne 0) { throw "git switch failed" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "git pull failed" }
git rev-parse HEAD
dotnet build .\PTMagic.sln
if ($LASTEXITCODE -ne 0) { throw "build failed" }
dotnet run --project .\Tests\Phase2OpenInterest\Phase2OpenInterest.csproj
if ($LASTEXITCODE -ne 0) { throw "Phase 2 OI tests failed" }
```

Reference: [current technical roadmap](../roadmaps/CURRENT.md) · [release change record](../CHANGELOG-2.10.md) · [previous stabilization handoff](2026-11-07-stabilization-correlation-validation.md).
