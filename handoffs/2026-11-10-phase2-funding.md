# PTMagic 2.10 — Phase 2 funding-rate development handoff

**Date:** November 10, 2026 (KST)  
**Application branch:** `HojouFotytu/PTMagic` → `phase1/market-data-foundation`  
**Source checkpoint (verified offline):** `49f2aab66592b6e2922097ca5242b5a614090602`  
**Status:** Build and all offline regression tests **PASS**; provider/runtime/Monitor-browser integration remains pending.

## November 10 — Completed deterministic validation

At `49f2aab66592b6e2922097ca5242b5a614090602`, the user ran the full `Run-Phase2Validation.ps1` procedure: .NET 10.0.403 solution build PASS in **11.0s**, **16/16** offline test harnesses PASS, **332/332** groups PASS. Funding **17/17**, OI **35/35**, existing regression **280/280**. Eight nonfatal nullable warnings in two older test projects. [Full evidence](../updates/2026-11-10-phase2-funding-offline-validation.md).

The tested application source also includes a Monitor Global Settings activation-trigger log change; compilation and the 28 existing MonitorSettingsRoundTrip tests passed, but the new browser display was not acceptance-tested. The prior untested notes below describe the *initial publication state* and are superseded by these exact-source results.

## Funding implementation

The native historical endpoint is `GET /fapi/v1/fundingRate`, with inclusive `startTime`/`endTime` (milliseconds) and `limit<=1000`. It shares a 500/5-minute per-IP rate limit with `fundingInfo`. Queries are pinned to the raid timestamp, and the shared PTMagic HTTP transport owns retry, cancellation and global Binance limiter. The endpoint returns ascending records. The source model stores native decimal rate, exact funding time, rateType and markPrice without reinterpreting `premiumIndex.lastFundingRate` as a settled event.

`FundingRate` = latest Regular settled native funding rate inside `MarketTrend.TrendMinutes` ×100 (percentage points). `FundingSum` = sum of Regular settled rates within the same window ×100 (percentage points). Neither annualizes, converts per 8 hours, or mixes Special stock-dividend funding with regular funding. Unknown/missing rateType makes affected metrics UNAVAILABLE, not zero. A completely verified window containing no Regular events produces a valid zero FundingSum, but no FundingRate. No market-wide funding aggregates yet; those belong to Phase 2B.

**History is user-derived.** The longest funding-enabled MarketTrend controls historical acquisition. No fixed hours retention property and no universal funding cadence. The service holds verified fully exhausted request intervals and resumes partial pagination across successive raids. It is currently an in-memory cache (restart persistence is not yet implemented). Incomplete, malformed, conflicting, absent or insufficient history is UNAVAILABLE; no missing settlement is silently synthesized. Pagination uses an inclusive overlap at full-page timestamp boundaries to avoid losing Special/Regular events. The endpoint's available history remains an external constraint.

The `MarketAnalyzer.FundingMaxRequestsPerRaid` setting (default 60, allowed 0–400, zero disables acquisition) is a request budget, not a retention setting; two pages/market/raid and 1000 records/page maximum. Existing MarketTrend selection, per-asset SMS trigger/off-trigger resolution, MarketTrendAnalytics/Monitor export, History Requirements and rate-limit diagnostics are used. Funding data is Futures-only; other Binance variants do not request it. Default PriceTrend-only configurations do not request funding history.

## Source changes

- `Core/MarketAnalyzer/MarketData/FuturesFunding.cs`: strict mapping of native settlement rates, timestamps, types, mark prices.
- `Core/MarketAnalyzer/MarketData/BinanceFuturesFundingClient.cs`: optional pinned HTTP history page.
- `Core/MarketAnalyzer/MarketData/FuturesFundingDataService.cs`: bounded, fair and resumable history with completeness tracking.
- `Core/MarketAnalyzer/MarketData/FuturesFundingFeatureEngine.cs`: separate Regular funding-rate and sum calculations with validity metadata.
- Existing runtime/orchestrator, metrics registry, analyzer model/defaults, trigger resolver, history report and Monitor view integrated without an alternate framework.
- `Tests/Phase2Funding/`: **17 offline case groups** written to check source mapping, rate types, timestamps, invalid data, dynamic horizons, exact math, empty/missing history, partial pagination, budgets, source identity and scope.

## Test status and commands

**Completed:** The required full solution build and all 16 offline test projects were run at `49f2aab` and passed (332/332). The earlier 315/315 evidence remains attributed to its older OI-only source `5f51faaa`; it is not the latest checkpoint.

From the PTMagic application repository:

```powershell
git switch phase1/market-data-foundation
if ($LASTEXITCODE -ne 0) { throw "Branch switch failed" }

git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull failed" }

& ".\Tests\Phase2OpenInterestIncremental\Run-Phase2Validation.ps1"
```

The runner records the source revision, builds `PTMagic.sln`, then runs **16** deterministic test projects, including `Phase2Funding`, `Phase2OpenInterest`, `Phase2OpenInterestIncremental`, and all thirteen earlier PTM regression projects. No configured ProfitTrailer API writes, live trading actions or browser tests are included.

**Future work:** implement separate global/top-trader account and position long-short ratios, maintaining exact provider semantics and required tests; then taker flow and Phase 2B market aggregates. Distinct `fundingIntervalHours` metadata and live provider behavior still require separate acceptance. The particular deferred Phase 1 PT/SOM/browser integration tests remain pending separately. Ordinary Phase 2 source testing is mandatory.

[Current roadmap](../roadmaps/CURRENT.md) · [Development status](../STATUS.md) · [Funding test instructions](https://github.com/HojouFotytu/PTMagic/tree/phase1/market-data-foundation/Tests/Phase2Funding).
