# PTMagic 2.10 — Top-trader ratio removal and API-key removal validation

**Date:** November 11, 2026 (KST)  
**Application branch:** `phase1/market-data-foundation`  
**Exact user-tested source:** `1a1f1804237288433ed046b30fb7d9b780a32066`  
**SDK:** .NET 10.0.403

## Implemented removal

Both top-trader ratio metrics, their source variants, endpoint mappings, feature calculations, authentication-specific handling, API-key request parameter/header, runtime scheduling, dedicated application model property, Monitor General Settings input/save handlers, supplied PTMagic configuration entries and related tests were removed. No compatibility aliases, disabled implementations or credential-gated paths remain.

The sole supported ratio metric is the public asset-scoped `GlobalLongShortAccountRatio`. Its five-minute observations, calculations, persistent cache, Unicode symbol handling and UNAVAILABLE semantics remain.

## User-run validation — PASS

- Core, PTMagic and Monitor solution build: **PASS**, 18.2 seconds.
- Offline harnesses: **17/17 PASS**.
- Individual checks: **377 PASS**.
- Build errors: **0**; failed tests: **0**.
- Nonfatal nullable warnings: **8**, in existing `Phase1SmsSummaryIsolation` and `NormalizedPriceTrendMigration` test projects.
- Ratio harness: **32 checks PASS**, including global-account-only metric and public endpoint assertions.

Funding 21, raw OI 19, incremental OI 18, ConfigurationLifecycle 73 and DecisionHistory 13 also passed.

## Acceptance boundary

Offline build and regression validation only. Live Binance endpoint acceptance, configured raid behavior, two-startup request reduction and Monitor browser rendering remain unverified.

## Remaining work

1. Remove the three user-configurable per-raid request-budget properties.
2. Implement shared application-managed adaptive derivative acquisition using Binance rate-limit state, endpoint request weights, response headers and 429/418 cooldowns.
3. Preserve internal pagination, per-symbol progress, fairness, incremental coverage, persistence and UNAVAILABLE semantics without replacement user-facing static limits.
4. Complete configured Unicode-market raid and two-startup persistence acceptance.

This is PTMagic application work only. No ProfitTrailer strategy-settings repositories or artifacts were changed.
