# PTMagic 2.10 — D-051 adaptive derivative acquisition implementation

**Date:** 2026-11-11 (KST)  
**Application:** [PTMagic](https://github.com/HojouFotytu/PTMagic), branch `phase1/market-data-foundation`  
**Source commit:** [`5a21a482711c8026b50fce10c55b3fb76f4075c3`](https://github.com/HojouFotytu/PTMagic/commit/5a21a482711c8026b50fce10c55b3fb76f4075c3)  
**Status:** Published to GitHub and **offline validated November 11, 2026** (.NET 10.0.403 solution build PASS; 18/18 harnesses, 386 checks PASS). Configured runtime acceptance remains pending.

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

Expected and user-verified commit: `5a21a482711c8026b50fce10c55b3fb76f4075c3`. The required local run has now passed (evidence recorded below). Next: configured Unicode COIN-market raid, configured two-startup derivative-cache persistence/request-reduction acceptance, then live Binance/PT and Monitor review. Taker-flow development remains deferred until persistence acceptance.

## November 11 — User-executed offline acceptance

**User-run validation (November 11, 2026):** Exact source `5a21a482711c8026b50fce10c55b3fb76f4075c3`, .NET SDK 10.0.403, Core/PTMagic/Monitor solution build **PASS in 13.9 seconds**, all **18/18 offline harnesses PASS (386 checks)**. New `Phase2AdaptiveAcquisition`: **9/9** focused groups PASS, including OI/global-ratio shared allowance, separate funding allowance, request-weight headers, 429/418 cooldowns, family admission, freshness/cancellation, and more than 60 pages in each family. Eight nonfatal nullable warnings remain in `Phase1SmsSummaryIsolation` (2) and `NormalizedPriceTrendMigration` (6). No live Binance, configured raids, ProfitTrailer API actions or Monitor browser acceptance occurred.

The focused adaptive groups explicitly confirm shared OI/global-account-ratio historical allowance, separate funding allowance, endpoint-weight response-header accounting, HTTP 429/418 cooldowns, fair family admission, stale/saturated/cancelled acquisition, and completion beyond 60 pages for all three derivative families. Earlier cache and Unicode service regressions also passed in the same suite.

**Acceptance:** D-051 offline implementation and validation COMPLETE at `5a21a482711c8026b50fce10c55b3fb76f4075c3`. **Not yet accepted:** live provider/IP enforcement, multiple PTMagic processes sharing one outbound IP, configured Unicode Binance symbols, actual request reduction and unchanged values across two real startups, actual ProfitTrailer delivery, and Monitor browser behavior. No strategy-settings workstream modifications are authorized or implied.
