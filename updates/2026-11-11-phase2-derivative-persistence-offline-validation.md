# PTMagic 2.10 — Phase 2 derivative persistence offline validation PASS

**Date:** November 11, 2026 (KST)  
**Application repository:** [HojouFotytu/PTMagic](https://github.com/HojouFotytu/PTMagic)  
**Application branch:** `phase1/market-data-foundation`  
**Exact user-tested source:** `86fa4c9a306f7eb61742c26bbb1ae633bb775a2a`  
**SDK:** .NET 10.0.403

## Result

The user ran the existing `Tests/Phase2OpenInterestIncremental/Run-Phase2Validation.ps1` from the existing local clone. The solution build completed successfully in **10.3 seconds**. Core, PTMagic and Monitor all compiled. All **17/17 offline harnesses passed**, totaling **378 passing checks**.

| Harness | Result |
|---|---:|
| Phase2Funding | 20 |
| Phase2OpenInterest | 18 |
| Phase2OpenInterestIncremental | 17 |
| Phase2LongShortRatios | 36 |
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
| **Total** | **378** |

Eight nonfatal nullable warnings were emitted from existing test sources:
- Two warnings in `Tests/Phase1SmsSummaryIsolation/Program.cs` (`CS8600`, `CS8602`).
- Six warnings in `Tests/NormalizedPriceTrendMigration/Program.cs` (`CS8625`, `CS8629`, `CS8602`).

No build errors or failed harnesses occurred.

## Derivative persistence checks now passing

The executed offline suite confirms:

- Funding complete-cache restoration through a newly constructed service, with no duplicate provider request.
- Funding partial-range progress persists and resumes across service restarts.
- Funding corrupt-cache recovery replaces the invalid file with valid observations and verified coverage after one bounded request.
- Long/short ratio complete-cache restoration through a newly constructed service, with no duplicate provider request.
- Ratio partial-range progress persists and resumes across service restarts.
- Ratio corrupt-cache recovery replaces the invalid file with valid observations and verified coverage after one bounded request.
- Existing OI raw and incremental tests remain passing.

The corrected corrupt-cache tests now assert the intended recovery result: the corrupt file is discarded, a bounded reacquisition occurs, and a valid replacement cache is written.

## Acceptance boundary

This is **offline development validation only**. It does not establish:
- A configured PTMagic startup or ordinary raid.
- Cache restoration by the installed/running PTMagic process.
- Actual Binance request reduction across two process startups.
- Live Binance funding, OI, global-account or top-trader endpoint acceptance.
- Actual PT API behavior or Monitor browser rendering.

## Next acceptance gate

Perform configured two-startup runtime acceptance with explicitly enabled Phase 2 metrics. Record the runtime working directory, exact running source/binary, selected symbols, configuration and settings hash, per-family request/restore summaries, and the resulting `_data/MarketTrendAnalytics.json` metric snapshots. Compare first-startup cold acquisition with second-startup restoration/incremental requests and confirm that available metric values remain consistent for the same pinned data window.

Top-trader ratio endpoints require the optional read-only `BinanceFuturesApiKey`; no API secret is required. If that key is not configured, top-trader metrics intentionally remain UNAVAILABLE and are not acquired.

Taker-flow implementation remains behind configured derivative persistence acceptance.
