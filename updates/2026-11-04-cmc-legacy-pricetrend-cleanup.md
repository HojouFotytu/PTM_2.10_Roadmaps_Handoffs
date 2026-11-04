# PTMagic 2.10 — CoinMarketCap and legacy PriceTrend cleanup

Date: 2026-11-04
Application repository: HojouFotytu/PTMagic
Branch: phase1/market-data-foundation
Previous HEAD: 3c3b85c998a7eeace8f8084ce1a931ff00320368
Implementation commit: 08612fed2cb02746a433f5d96013d481d2816bc6

## Scope

Follow-up work after the Phase 1C acceptance baseline, limited to outstanding items 1 and 2.

- Removed CoinMarketCap runtime source, API ingestion, application configuration property, default API-key setting, and Monitor settings control/MarketTrend source option.
- Removed obsolete BaseAnalyzer historical PriceTrend calculation methods: BuildMarketTrends, GetMarketTrendChanges, BuildGlobalMarketTrends.
- Retained shared BaseAnalyzer networking, market metadata and historical Exchange snapshot reader, which remain needed for SMS prices/24h volume, selected market populations, and settings compatibility.
- Removed Bittrex/Poloniex analyzer sources and obsolete UI/symbol-format remnants. Supported exchanges remain Binance Futures, Binance Spot and Binance US.
- Consolidated GlobalSetting/SMS trigger use of the normalized resolver and removed superseded legacy trigger branches.
- Retained normalized PriceTrend mapping into existing Monitor/summary structures.
- Added an additional migration regression check: omitted GlobalSetting/SMS Metric resolves normalized PriceTrend, while explicit metrics still require enabling.

## Configuration compatibility contract

- MarketTrend with omitted or blank Metrics -> normalized PriceTrend.
- Trigger or OffTrigger with omitted or blank Metric -> normalized PriceTrend.
- For GlobalSettings, existing MinChange/MaxChange trigger semantics and three-valued unavailable handling remain.
- For SMS, Relative, Absolute and RelativeTrigger relation semantics remain, now applied to normalized PriceTrend.
- An explicit metric selects its enabled normalized metric; metric-only MarketTrends can acquire PriceTrend implicitly when referenced by a blank-metric trigger.
- Existing Exchange-platform JSON settings require no schema migration.
- CoinMarketCap-platform MarketTrends cannot continue using CoinMarketCap, since this source is removed. Change Platform to Exchange.

## Validation status

- GitHub source changes committed; branch ref advanced.
- Targeted static inspection: CMC references and legacy calculator names absent from inspected affected source/config/UI files; removed source files absent from the staged tree.
- .NET SDK unavailable in the execution environment. No successful new dotnet build, migration-harness run, entire regression-suite run, or three-exchange TestMode validation is claimed.
- Previous Phase 1C 58 passing cases do not validate this commit. Migration harness now contains 12 expected cases (70 total expected across six existing harnesses, subject to build).

## Follow-up verification

Run dotnet build, all six test harnesses, and three-exchange TestMode. Validate ignored/allowed markets, MaxMarkets, TrendThreshold, implicit global/SMS trigger metrics, relative/activation-relative SMS behavior, Monitor output, and any legacy settings using TrendCurrency=Fiat (which requires explicit compatibility confirmation before claiming full numerical parity).

This update does not close Phase 1D or change the wider roadmap scope.
