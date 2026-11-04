# PTMagic 2.10 — Option C natural-language metric warnings

Date: 2026-11-04
Application: HojouFotytu/PTMagic
Branch: phase1/market-data-foundation
Source commit: e652b04cb8b18d88f13f6b8400fb77c2cce44617

## Change

Reformatted all normalized metric-warning groups in RAID SUMMARY to natural-language Option C.

- A single message explains which MarketTrend/metric was unavailable, the requesting GlobalSetting/SMS when identified, why it failed and an actionable check or configuration change.
- Recognizes `IgnoredMarkets` / `AllowedMarkets` exclusions, illegal asset-only metrics in global triggers (e.g. ATRP vs MedianATRP), explicit disabled metrics (including implicit PriceTrend compatibility), missing 5m endpoints, insufficient periods for higher-horizon ATRP/volume metrics, global coverage thresholds, unknown metric names and generic missing snapshots.
- Multiple triggers sharing a warning remain grouped; identifies affected caller examples and the number beyond the example cap.
- GlobalSetting indeterminate decision warnings have clearer plain-language statements.
- No intentional trading or calculation behavior changes. The detailed underlying analyzer values still exist in runtime JSON exports and metric snapshots; the RAID SUMMARY is deliberately shorter.

## Regression tests

The Phase1MetricWarnings harness now has 18 deterministic cases (six new cases). Expected total over six harnesses: 81 tests. **No new local .NET build or test run is claimed.**

### Local validation — user-owned (D-021)

```powershell
git pull --ff-only
dotnet build
dotnet run --project Tests/Phase1MetricWarnings/Phase1MetricWarnings.csproj
```

Expected harness line: `Phase 1 metric-warning summary tests passed: 18.`

Then run the remaining existing five harnesses and inspect a Binance Futures TestMode RAID SUMMARY. Confirm a warning such as FILTERED_1h PriceTrend identifies the SMS and SOL exclusion in one coherent sentence, and 8h metrics describe available vs required historical periods. Check GlobalSetting and SMS decisions remain unchanged. Spot/US end-to-end tests remain separate.

## Caveats

- User's prior diagnostic run verified 7 stable warning groups; that run predates the Option C formatting change.
- Outstanding cold-start refresh crossing a five-minute candle boundary remains a separate issue, not fixed by this change.
- No new GitHub Actions workflow was introduced; builds and TestMode remain local.
