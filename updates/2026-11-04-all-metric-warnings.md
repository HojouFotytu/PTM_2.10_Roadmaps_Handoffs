# 2026-11-04 — Display all distinct RAID SUMMARY metric warnings

**Application branch:** `HojouFotytu/PTMagic:phase1/market-data-foundation`  
**Source commit:** [`64e05e7`](https://github.com/HojouFotytu/PTMagic/commit/64e05e7e2a93aa23828890ef5e4708f002c696b8)  
**Task:** D-018 amendment.

The user reported seeing `... and 6 more` in the compact raid metric-warning summary and required **all** warnings to be visible. Removed the five-detail cap and overflow indicator. Every unique grouped MarketTrend/metric warning is now printed; identical per-market warnings remain deduplicated. Preserved deterministic ordering and existing trigger semantics.

Updated `Tests/Phase1MetricWarnings/Program.cs` to assert that nine distinct synthetic warnings produce ten total output lines (header + nine details) and verify presence of every metric. Existing six other test cases remain unchanged; suite is still seven checks.

**Verification:** Source committed; execution remains pending. Run `dotnet build` and `dotnet run --project Tests/Phase1MetricWarnings/Phase1MetricWarnings.csproj`, plus TestMode raid log review. No new runtime pass is claimed.
