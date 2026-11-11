# PTMagic 2.10 — D-051 adaptive derivative acquisition implementation

**Date:** 2026-11-11 (KST)  
**Application:** [PTMagic](https://github.com/HojouFotytu/PTMagic), branch `phase1/market-data-foundation`  
**Source commit:** [`5a21a482711c8026b50fce10c55b3fb76f4075c3`](https://github.com/HojouFotytu/PTMagic/commit/5a21a482711c8026b50fce10c55b3fb76f4075c3)  
**Status:** Published to GitHub, **local .NET build and offline harness validation pending**.

## Earlier completed evidence

At source `66067123635cbe68063713cbbc389793e5690fed`, the user ran .NET SDK 10.0.403: Core/PTMagic/Monitor build PASS (16.2s), 17/17 offline harnesses PASS and 377 checks PASS. Eight nonfatal nullable warnings came from `Phase1SmsSummaryIsolation` and `NormalizedPriceTrendMigration`. This validates D-051 removal of user-facing request budgets and the earlier top-trader removal, but **not** the later adaptive scheduler.

## New source behavior

- `Core/MarketAnalyzer/BinanceRateLimiter.cs`: single in-process IP/host state reserves estimated request weights; observes Binance `X-MBX-USED-WEIGHT-1M` feedback; enforces the published 1000/5-minute historical-data allowance shared by OI and global-account ratio and the separate 500/5-minute funding allowance, each conservatively gated at 80% capacity; honors 429/418 Retry-After and fallback cooldowns. The legacy shared HTTP transport remains the point of admission for every actual request.
- `Core/MarketAnalyzer/MarketData/BinanceDerivativeAcquisitionScheduler.cs`: round-robin page admission for OI/funding/global-account ratio. Quota saturation defers instead of waiting an entire exchange quota window during analysis. Admission ends at the existing pinned analysis-freshness deadline.
- `Core/MarketAnalyzer/MarketData/BinanceFuturesAnalyticsRuntime.cs` and `Core/Main/PTMagic.cs`: execute enabled derivative families concurrently under one scheduler and linked cancellation deadline. Reports show requests actually made rather than a count/ceiling fraction. Expiry defers the remaining work; it does not authorize any fabricated metric or fresh trading decision.
- `FuturesOpenInterestDataService.cs`, `FuturesFundingDataService.cs`, `FuturesLongShortRatioDataService.cs`: production uses `int.MaxValue` as an unbounded request-count sentinel, plus a per-page admission callback. The three fixed `DefaultRequestsPerRaid=60` constants were removed. Explicit bounded service calls remain for deterministic fixtures; finite provider page sizes, per-symbol page progression, disk cache, exact observation validation and UNAVAILABLE semantics remain.
- `Tests/Phase2AdaptiveAcquisition`: new offline project and nine focused groups for quotas, headers, 429/418, family scheduling, deadline/cancellation and requests beyond sixty per family. Registered in the existing `Run-Phase2Validation.ps1` runner, now **18 harnesses**.

No user-configurable replacement budgets, additional derivative API keys, PT strategy settings, SOM changes or Monitor presentation changes were introduced. Binance IP quotas are tracked **within each PTMagic process**, not across independent PTMagic processes sharing one external IP; live acceptance must account for that limitation.

## Required local acceptance

Run from the existing PTMagic clone:

```powershell
$ErrorActionPreference = "Stop"
git switch phase1/market-data-foundation
if ($LASTEXITCODE -ne 0) { throw "Branch switch failed" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Git pull failed" }
git log -1 --format="%H"
& ".\Tests\Phase2OpenInterestIncremental\Run-Phase2Validation.ps1"
if ($LASTEXITCODE -ne 0) { throw "Adaptive validation failed" }
```

Expected commit at authoring: `5a21a482711c8026b50fce10c55b3fb76f4075c3`. **Actual output is required before marking any result PASS.** Following a successful local run, perform configured Unicode COIN-market raid and configured two-startup derivative-cache persistence/request-reduction acceptance, then live Binance and Monitor review. Taker-flow development remains deferred until persistence acceptance.
