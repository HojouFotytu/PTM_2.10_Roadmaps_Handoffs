# PTMagic 2.10 — D-053 three-metric removal: read-only code audit

**Date:** 2026-11-12 (KST)  
**Status:** Source inspection complete; no further critical or major removal-related defect identified in inspected source. **A post-removal local build, current harness execution, configured raids and live PT/Monitor acceptance have not been verified.**  
**Scope:** PTMagic **software** implementation only; independent of personal LONG/SHORT analyzers or PAIRS/DCA/INDICATORS strategy settings. No rollback requested, proposed or performed.

## Source provenance and comparison

| Checkpoint | PTMagic application commit | Relevance |
|---|---|---|
| Baseline immediately before introducing OI integration | [`66629347f0dc9c7b68ea9f1c3f5bf536f3d7c427`](https://github.com/HojouFotytu/PTMagic/commit/66629347f0dc9c7b68ea9f1c3f5bf536f3d7c427) | 22 normalized/correlation metrics, before new derivatives |
| Immediately before D-053 source removal | [`d101b5a03e01f8f76acf8cc9a6bde7214ff34aa2`](https://github.com/HojouFotytu/PTMagic/commit/d101b5a03e01f8f76acf8cc9a6bde7214ff34aa2) | 27 metrics: original 22 + two funding + two OI + one public positioning |
| Source removal | [`3b867399f2f235708a8959448ebf4e084a0b2428`](https://github.com/HojouFotytu/PTMagic/commit/3b867399f2f235708a8959448ebf4e084a0b2428) | Deletes OI/positioning metrics and source families; simplifies shared acquisition |
| Tests/configuration cleanup | [`5e0372aa1ac3`](https://github.com/HojouFotytu/PTMagic/commit/5e0372aa1ac3) | Removes obsolete suites; retains/adapts funding and 24-metric checks |
| Funding normalizer repair (part 1) | [`02820822b9bb`](https://github.com/HojouFotytu/PTMagic/commit/02820822b9bb) | Moves Unicode-safe symbol validation from deleted OI class to retained funding class |
| Funding normalizer repair (part 2) | [`d7847c46190b`](https://github.com/HojouFotytu/PTMagic/commit/d7847c46190b) | Updates funding feature engine's remaining normalizer reference |
| Audited application branch head | [`892a5f1f4729a3fccd3cb477ba6ad22fbbe0918d`](https://github.com/HojouFotytu/PTMagic/commit/892a5f1f4729a3fccd3cb477ba6ad22fbbe0918d) | Latest inspected D-053 source and 24-metric changelog |

The 22 **pre-introduction** metric identifiers and their original global/asset scope classifications match the audited branch. The two retained asset metrics `FundingRate` and `FundingSum` are additional to the original 22. Current effective catalogue: **24 distinct metrics, 17 global-capable and seven asset-only**. `PriceTrend` has both global and asset scope but counts once. Exactly `OpenInterestChange`, `OpenInterestValueChange` and `GlobalLongShortAccountRatio` were withdrawn; top-trader ratios and their API-key path had already been removed in the earlier D-051 change.

## Dependency-by-dependency inspection

| Affected area | Finding / disposition |
|---|---|
| `MarketTrendMetrics` registry and scope | All 22 original registrations/scopes preserved; the two funding registrations preserved; only three withdrawn entries deleted |
| `MarketTrendAnalyticsEngine` | OI/ratio asset calculation branches removed; retained funding merge and normalized calculations remain |
| `MarketTrendHistoryRequirements` | Source-family-specific OI/ratio requirements deleted; normalized OHLCV and separate funding-history contracts remain |
| `MarketTrendMetricTriggerResolver` / runtime reference checks | OI/ratio special exchange checks deleted; funding-only Futures restriction, scope checking, missing/UNAVAILABLE handling remain |
| `Core/Main/PTMagic.cs` | Pre-evaluation acquisition now calls `RefreshFundingHistoriesAsync` instead of the old three-family refresh; normalized trend evaluation remains |
| `BinanceFuturesAnalyticsRuntime` | OI/ratio services and collectors removed; funding service, frozen population and pinned-deadline acquisition retained |
| `BinanceRateLimiter` | Removed retired historical-data 1,000/5m quota bookkeeping only; retains funding/fundingInfo 500/5m provider quota, conservative 80% threshold, shared IP weight, header feedback and 429/418 cooldowns |
| Acquisition scheduler | The old fairness scheduler for three families replaced with a funding-only deadline/cancellation-aware scheduler. No cross-family fairness is required with just one family |
| Funding client, service, cache, feature engine | Bulk-first funding, verified pagination, conditional per-symbol fallback, persistent `_data/DerivativesFundingCache`, settled-event types/units and incomplete-history UNAVAILABLE behavior retained |
| Monitor | OI/ratio label, tooltip and value-rendering special cases removed; funding values and VolumeExpansion neutral-value rule preserved |
| Configuration models / examples | Removed obsolete metric references from the current example tester; no withdrawal-related application control remains |
| Existing disk data | Retired OI and ratio cache directories are no longer active dependencies. This code removal does not delete users' existing cache files |
| Old metric references in user-authored configurations | Runtime treats removed names as unknown/unavailable, with diagnostic warning rather than an invented zero. As before, metric warnings are not necessarily fatal configuration errors; an obsolete user configuration can start while its affected triggers cannot resolve |

**Source search scope:** inspected the directly changed code, relevant Core runtime/analytics/limiter/ProfitTrailer paths, Monitor pages and settings, retained funding paths, application configuration, existing test harnesses, and Monitor's first-party analyzer JavaScript. No remaining references to deleted runtime types, method names or metrics were found in the inspected active production paths. This is a *source audit*, not a proof that a live binary or every third-party asset was examined.

## Confirmed removal mistake and correction

Deleting `FuturesOpenInterest` also deleted `FuturesOpenInterest.NormalizeSymbol`, which the retained funding implementation had reused. This was a real shared dependency, not an OI-only function. The D-053 cleanup therefore initially left unresolved funding references.

The subsequent `02820822` and `d7847c46` commits corrected the dependency: `FuturesFunding.NormalizeSymbol` retains Unicode rune-aware letters/digits, underscores, uppercase conversion and the original length/rejection rules; the funding HTTP client, parser, service, cache and feature engine now call the funding-owned validator. **The repair is present in the audited head.** Current-run compile/execution proof remains pending.

## Retained test architecture and limitations

The current `Tests/Phase2OpenInterestIncremental/Run-Phase2Validation.ps1` entry point is intentionally kept for local command compatibility, but now enumerates **15** test projects, rather than the **18** used before D-053. Deleted OI/ratio harnesses are correctly removed. The retained `Phase2AdaptiveAcquisition` test has **eight** funding/metric-scope/limiter/deadline groups; `Phase2Funding` has **28** offline case groups, including Unicode symbols, cache restart and corruption, bulk pagination, fallback and exact value semantics. Tests are present in source; **their current-revision execution was not observed in this audit**.

The current `Tests/Settings/settings.analyzer.json` lists all **24** metrics across three trends (M30, H1, H24), with no orphaned trend reference among the 25 inspected trigger references.

**Documentation discrepancy found:** the application `Tests/Phase2Funding/README.md` still described the runner as **16** offline harnesses, while the script currently lists **15**. Correct this documentation to 15; it is not a production-code defect.

No GitHub Actions run for this removal was found in the examined branch history. The last locally reported 18-harness PASS applies to the **pre-removal** `d101b5a0` source; it cannot validate `892a5f1f`.

## Overall assessment and next scope

**Result:** The removed metric catalogue, source-family deletions, retained funding integration, rate-limit protections and existing normalized metrics appear internally consistent **after** the two symbol-normalizer corrections. No additional high-severity or critical removal-related defect was established by source inspection. This is **not** a claim of current-revision build success, live correctness or universal absence of bugs.

A proportionate verification step is a clean `dotnet build .\PTMagic.sln` and, if desired, the two directly affected offline harnesses (`Phase2Funding` and `Phase2AdaptiveAcquisition`) against the printed source SHA. The existing full 15-harness runner remains available, but unrelated repeated synthetic test cycles are not prerequisites for unrelated strategy work. Configured runtime/funding freshness, live Binance behavior and PT/Monitor interactions remain separately unverified.

Continue only with approved retained families: funding, future taker-flow metrics and their market aggregates, transparent price/volume/flow conditions and liquidity/depth/stress work. No OI/positioning restoration, redesign or historical acceptance work is planned. Prior dated OI/ratio handoffs and passing tests remain historical evidence, not current instructions. Keep PTMagic software and user-specific analyzer/strategy development strictly separate.
