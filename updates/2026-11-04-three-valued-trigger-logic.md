# 2026-11-04 — Three-valued normalized trigger logic

**Task:** P4-TRIG, Phase 1A correctness refinement.  
**Application repository:** `HojouFotytu/PTMagic`, branch `phase1/market-data-foundation`.  
**Source HEAD after implementation:** `9f180952db853659cd94c7b2a26341f972b47fca`.  
**Design decision:** D-017.

## Change

The previous implementation skipped any GlobalSetting with an unavailable normalized trigger and vetoed SMS activation whenever a single required metric was unavailable, even for `true OR unavailable` expressions. The user clarified that validity must be determined by the *complete Boolean expression*.

- `true OR unavailable = true`; `false OR unavailable = unavailable`.
- `false AND unavailable = false`; `true AND unavailable = unavailable`.
- `NOT unavailable = unavailable`, including custom nested expressions.
- GlobalSetting, SMS activation and OffTrigger now use the same tri-state evaluator.
- A final unknown expression never activates or deactivates a setting. Fully evaluable independent settings remain eligible.
- Existing active GlobalSetting hold remains applicable for indeterminate selection. SMS long-term OffTrigger retention logic is preserved.
- Omitted `Trigger.Metric` continues using existing legacy behavior.
- A source parser operates on tagged Boolean expression trees, not substring replacement that could corrupt overlapping tags.

## Commits

1. [`eeffc05`](https://github.com/HojouFotytu/PTMagic/commit/eeffc05d0146ac31f355db31881250d9f93cfbc5) — shared `ThreeValuedTriggerLogic` and 29-case dependency-light regression harness.
2. [`9f18095`](https://github.com/HojouFotytu/PTMagic/commit/9f180952db853659cd94c7b2a26341f972b47fca) — GlobalSetting, SMS activation, SMS OffTrigger integration.

## Required verification

```powershell
dotnet build
dotnet run --project Tests/Phase1TriggerLogic/Phase1TriggerLogic.csproj
dotnet run --project Tests/Phase1AReadiness/Phase1AReadiness.csproj
```

Also run TestMode with a valid `OR` branch and unavailable metric, a false `AND` branch and unavailable metric, nested negation, previously active GlobalSetting and persistent SMS OffTrigger states.

**Status:** Application code committed; syntax/source sanity checks performed. No SDK available here; no C# build, automated test execution or TestMode verification claimed. This is not a completed tested correctness closeout.

**Unchanged:** Phase 1C dynamic MarketTrend timeframe D-016; ATRP/MedianATRP remain next.
