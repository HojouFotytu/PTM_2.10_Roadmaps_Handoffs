# PTMagic 2.10 — Verbose normalized metric-warning diagnostics

Date: 2026-11-04

Application source: HojouFotytu/PTMagic
Branch: phase1/market-data-foundation
Commit: efa7b5ff1a99606395c1b1b9636c828600a55353

## Change

Retain concise grouped end-of-raid reporting while making each metric warning traceable:

- Group by exact MarketTrend and normalized Metric; preserve failed-request and unique-market counts.
- For GlobalSetting, capture setting name, trigger tag, relation and full error reason.
- For SMS activation/OffTrigger, capture setting name, requested symbol, trigger tag or index, relation, explicit versus implicit metric, and error reason.
- Retain up to five examples per group and total counts for requests beyond the cap.
- For missing values, distinguish excluded asset populations, ignored/allowed filters, global versus asset scope, and no published metric/analysis.
- Print global feature flags, sample/coverage/endpoint metadata, detailed asset invalid reasons and sample markets; keep reasons bounded.
- Apply the grouped diagnostics to Binance Spot and Binance US in addition to Futures.
- No intentional changes to analytics, trigger truth values, settings, or PT updates.
- Remove the previous unrequested automatic GitHub Actions workflow, consistent with D-021.

## Tests and acceptance

Five additional deterministic tests in `Tests/Phase1MetricWarnings`, making **12** warning tests and **75** total expected checks across six test harnesses.

**Status: source committed; build, tests and new TestMode NOT RUN.** Under D-021 the user runs all execution locally. Recommended commands:

```powershell
dotnet build PTMagic.sln
dotnet run --project Tests/Phase1MetricWarnings/Phase1MetricWarnings.csproj
```

Then rerun remaining five existing regression harnesses. Check Binance Futures TestMode warning content, particularly `FILTERED_1h`, `FULL_2h/ATRP`, `IMPLICIT_1h/PriceTrend` and `INSUFFICIENT_8h`. Verify no per-pair warning floods and unchanged trigger outcomes. Test Spot and US separately when local instances are ready.

Prior successful 70/70 result belongs to the preceding version, not this new commit.
