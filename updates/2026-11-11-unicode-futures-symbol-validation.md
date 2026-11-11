# PTMagic 2.10 — Unicode Binance Futures symbols: offline validation PASS

**Date:** November 11, 2026 (KST)  
**Application repository:** [HojouFotytu/PTMagic](https://github.com/HojouFotytu/PTMagic)  
**Application branch:** `phase1/market-data-foundation`  
**Exact user-tested source:** `f108cd1ab39c44103bed91d1899f90f86a830eb4`  
**SDK:** .NET 10.0.403

## Incident

The user reported a raid failure after the Binance Futures universe froze 717 eligible markets. OI service symbol preparation threw:

`System.ArgumentException: A futures symbol contains unsupported characters.`

A read-only inspection of `_data/Exchange/BinanceFuturesMarketMetadata.json` found five eligible COIN/PERPETUAL symbols containing Chinese characters:

- `哈基米USDT`
- `币安人生USDT`
- `我踏马来了USDT`
- `牛来USDT`
- `龙虾USDT`

The shared derivative symbol normalizer accepted only ASCII A–Z, digits and underscore, rejecting these exchange-provided names before OI acquisition.

## Source correction

`FuturesOpenInterest.NormalizeSymbol` now uses Unicode rune-aware letter/digit validation and continues to allow underscore. It still rejects empty/overlong values, embedded whitespace, query separators and unsupported punctuation.

The OI, funding and long/short ratio clients already URL-encode symbol parameters with `Uri.EscapeDataString`; no endpoint or URL-construction change was required. All three derivative data services and their disk caches share the same symbol normalization identity.

No changes were made to market eligibility, underlying-type filters, request budgets, cache versions/formats, metric calculations, PT settings or trading strategies. The five markets were not removed from the configured universe.

## User-run validation

The user executed the existing `Tests/Phase2OpenInterestIncremental/Run-Phase2Validation.ps1` at exact source `f108cd1ab39c44103bed91d1899f90f86a830eb4`.

- .NET 10.0.403 solution build: **PASS**, 16.7 seconds; Core, PTMagic and Monitor compiled.
- Offline harnesses: **17/17 PASS**.
- Individual checks: **384 PASS**.
- Build errors: 0.
- Failed tests: 0.
- Nonfatal nullable warnings: 8, from the existing `Phase1SmsSummaryIsolation` and `NormalizedPriceTrendMigration` test projects.

| Harness | Result |
|---|---:|
| Phase2Funding | 21 |
| Phase2OpenInterest | 19 |
| Phase2OpenInterestIncremental | 18 |
| Phase2LongShortRatios | 39 |
| Phase1AReadiness | 5 |
| Phase1AnalyticsReliability | 16 |
| Phase1COhlcv | 13 |
| Phase1DCorrelation | 21 |
| Phase1MetricWarnings | 18 |
| Phase1SmsSummaryIsolation | 5 |
| Phase1TriggerLogic | 29 |
| NormalizedPriceTrendMigration | 18 |
| NormalizedWarmStartCache | 8 |
| TriggerConfigurationValidation | 40 |
| MonitorSettingsRoundTrip | 28 |
| ConfigurationLifecycle | 73 |
| DecisionHistory | 13 |
| **Total** | **384** |

## Unicode regression coverage

- All five reported symbols pass shared normalization and OI URL-encoding checks.
- OI service and disk-cache restart are exercised with `哈基米USDT`.
- Funding service, disk-cache identity and URL encoding are exercised with `币安人生USDT`.
- Long/short ratio service, disk-cache identity and URL encoding are exercised with `我踏马来了USDT`.
- Existing ASCII symbol tests continue to pass.
- Query injection and embedded whitespace remain rejected.

The service/cache integration tests use offline provider delegates. They establish application-side Unicode handling and persistence, not live exchange acceptance for all five symbols.

## Acceptance boundary and next step

This result closes the Unicode symbol-normalization regression at source/offline-test level. It does **not** yet establish that Binance's live OI, funding and ratio endpoints accept every Unicode symbol, nor that a configured PTMagic raid completes successfully with these markets.

Next: perform configured runtime acceptance. Confirm the ordinary raid completes, the OI/funding/ratio services no longer abort on these symbols, and per-family request/availability summaries remain healthy. Continue the separate configured two-startup persistence acceptance: confirm warm cache restoration, reduced second-startup Binance requests, and unchanged metrics for the same pinned data window.

Taker-flow development remains deferred until configured derivative persistence acceptance.
