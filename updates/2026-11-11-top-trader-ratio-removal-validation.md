# PTMagic 2.10 — Top-trader ratio removal and API-key removal validation

**Date:** November 11, 2026 (KST)  
**Application repository:** [HojouFotytu/PTMagic](https://github.com/HojouFotytu/PTMagic)  
**Application branch:** `phase1/market-data-foundation`  
**Exact user-tested source:** `1a1f1804237288433ed046b30fb7d9b780a32066`  
**SDK:** .NET 10.0.403

## Owner instruction

Remove the two top-trader ratio metrics and every application reference to their implementation. No backward compatibility is required. Retain only the public global-account long/short ratio.

## Implementation

The following PTMagic application paths were changed:

- `Core/MarketAnalyzer/MarketData/MarketTrendMetrics.cs`: removed both top-trader metric constants and registry entries.
- `Core/MarketAnalyzer/MarketData/FuturesLongShortRatio.cs`: removed top-trader source variants, metric mappings, endpoint mappings and API-key requirement.
- `Core/MarketAnalyzer/MarketData/FuturesLongShortRatioFeatureEngine.cs`: retained only the global-account metric and removed credential-dependent calculation paths.
- `Core/MarketAnalyzer/MarketData/FuturesLongShortRatioDataService.cs`: removed authentication-specific failure state and handling.
- `Core/MarketAnalyzer/MarketData/BinanceFuturesLongShortRatioClient.cs`: removed API-key parameter, API-key header and top-trader endpoint documentation.
- `Core/MarketAnalyzer/MarketData/BinanceFuturesAnalyticsRuntime.cs`: removed top-trader source scheduling, key lookup, authentication warnings and key-dependent analytics wiring.
- `Core/MarketAnalyzer/MarketData/MarketTrendAnalyticsEngine.cs`: removed the obsolete API-key calculation parameter.
- `Core/DataObjects/PTMagicData.cs`: removed the dedicated Binance Futures API-key property.
- `Monitor/Pages/SettingsGeneral.cshtml` and `.cshtml.cs`: removed the API-key input and its save/clear handlers.
- `PTMagic/_defaults/_default_settings_PT_2.x/settings.general.json` and `_Development/DevSettings/settings.general.json`: removed the obsolete application property.
- `Tests/Phase2LongShortRatios/Program.cs`: removed multi-source, top-trader endpoint, API-key and position-source tests; added sole-global-source assertions.
- `Tests/Phase2LongShortRatios/README.md`: now describes only the public global-account ratio.
- `CHANGELOG-2.10.md`: records the single supported ratio metric.

No compatibility aliases, disabled implementations or credential-gated top-trader paths remain in the changed application files. A post-commit read-back of all 15 changed files found zero remaining occurrences of the retired metric identifiers, source names, endpoint paths or `BinanceFuturesApiKey` property.

The retained `GlobalLongShortAccountRatio` continues to use Binance's public global-account endpoint. Its five-minute observation model, calculation, cache persistence, Unicode symbol handling and UNAVAILABLE behavior remain.

## User-run validation — PASS

The user pulled and ran the existing `Tests/Phase2OpenInterestIncremental/Run-Phase2Validation.ps1` at the exact source above.

- .NET SDK: **10.0.403**.
- Core, PTMagic and Monitor solution build: **PASS**, 18.2 seconds.
- Offline harnesses: **17/17 PASS**.
- Individual checks: **377 PASS**.
- Build errors: **0**.
- Failed tests: **0**.
- Nonfatal nullable warnings: **8**, in the existing `Phase1SmsSummaryIsolation` and `NormalizedPriceTrendMigration` test projects.

The Phase 2 ratio harness now passes **32 checks**, including:

- Global account is the sole ratio metric.
- Only the public global-account endpoint path remains.
- Five-minute pinned history URL and 500-row page bound.
- Unicode symbol service, URL encoding and cache restoration.
- Complete and partial cache restoration across service restarts.
- Corrupt-cache recovery.
- Exact window coverage and ratio calculations.
- Missing observations remain unavailable.

Other harness results: funding 21, raw OI 19, incremental OI 18, ConfigurationLifecycle 73 and DecisionHistory 13, with all remaining regression harnesses passing.

## Acceptance boundary

This is a successful solution build and offline regression result. It does not establish live Binance endpoint acceptance, a configured PTMagic raid, a configured two-startup request-reduction result or Monitor browser rendering.

## Remaining Phase 2 work

The separate D-051 acquisition redesign remains pending:

1. Remove the three user-configurable per-raid request-budget properties.
2. Implement application-managed adaptive derivative acquisition using shared Binance rate-limit state, endpoint request weights, response headers and 429/418 cooldowns.
3. Preserve internal pagination, per-symbol progress safeguards, fairness, incremental coverage, persistent caches and UNAVAILABLE semantics without replacement user-facing static limits.
4. Complete configured Unicode-market raid acceptance and configured two-startup persistence acceptance.

This work is PTMagic application development only. No ProfitTrailer LONG/SHORT strategy-settings repositories, analyzers, PAIRS/DCA/INDICATORS files or settings-development documents were changed.
