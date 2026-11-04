# 2026-11-04 — Compact RAID SUMMARY metric warnings

**Application branch:** `HojouFotytu/PTMagic:phase1/market-data-foundation`  
**Code commit:** [`34c30aa`](https://github.com/HojouFotytu/PTMagic/commit/34c30aa08918252d2976d6fabd7dddb1589acfd9)  
**Decision:** D-018; no change to D-016 or D-017.

The analyzer now prints a short Metric warnings subsection at the end of RAID SUMMARY only when Binance Futures normalized metrics have warnings. The summary groups invalid global metrics and per-asset metric failures by MarketTrend/metric; combines repeated SMS/GlobalSetting trigger-resolution failures; prints no more than five details plus an overflow count; and includes a concise notice when GlobalSetting selection is indeterminate and an active setting is retained. If all evaluated normalized metrics are healthy it reports `+ Metric warnings: none`.

The prior per-trigger normalized metric WARN lines in GlobalSetting/SMS execution were replaced with collection into this summary. This is diagnostic only: the Boolean evaluator, setting selection/hold safeguards, SMS OffTriggers, legacy paths and PT writes are unchanged. It is not a Monitor dashboard alert.

**Source files:** `Core/MarketAnalyzer/MarketData/RaidMetricWarnings.cs`, `Core/Main/PTMagic.cs`, and `Tests/Phase1MetricWarnings` (seven cases covering healthy, duplicate, reset, coverage, asset aggregation, unknown metric, GlobalSetting decision and detail cap).

**Verification pending:** The assistant environment has no .NET SDK. Run:

```powershell
git pull --ff-only
dotnet build
dotnet run --project Tests/Phase1MetricWarnings/Phase1MetricWarnings.csproj
dotnet run --project Tests/Phase1TriggerLogic/Phase1TriggerLogic.csproj
dotnet run --project Tests/Phase1AReadiness/Phase1AReadiness.csproj
```

Then validate a TestMode raid summary with invalid/stale/insufficient coverage cases and an indeterminate GlobalSetting decision. Do not mark build/runtime verified until user supplies results. P1C-01 dynamic ATRP remains the next feature.
