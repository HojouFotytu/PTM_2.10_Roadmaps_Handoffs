# November 9, 2026 — Persistent normalized OHLCV warm-start cache

**Application source published:** `925db7c153ee4d53cfe3b7bf736318e7a30bccf1`

**Branch:** `HojouFotytu/PTMagic:phase1/market-data-foundation`

**Status:** .NET 10.0.403 solution build and focused regression tests passed on the user's machine at `925db7c`; configured cold/warm runtime validation pending under D-021.

## Motivation and observed evidence

A user-reported restart soon after a prior run caused large data downloads again. The submitted November 7 runtime log showed one cold normalized load of 908,712 five-minute candles across 756 Binance Futures markets with StoreDataMaxHours=100, alongside separate legacy tick-history rebuilding. Existing normalized candles were held only in memory, so the process could not resume its full validated OHLCV window after a restart.

The earlier decision D-032 deferred broad performance optimization until all metric families were completed. The user explicitly authorized this targeted warm-start implementation now (D-040). Other performance work remains deferred.

## Resulting behavior

- Production normalized runtime uses `MarketDataWarmStartCache` under `_data/NormalizedOhlcvCache`.
- Closed five-minute candle histories are written to separate per-exchange/per-symbol compressed files with versioning, hash-based safe filenames, UTC interval identity, OHLCV validation, complete-file checking, bounded reads, throttled writes and atomic replacement.
- At the next process startup, the normal `MarketDataService` restores valid cached histories before its anchored refresh. If a validated restored cache covers the required window, it requests only the latest missing periods plus two overlap candles. Ordinary incomplete in-memory series retain conservative full backfill. If gaps, missing depth, invalid/stale input or corrupt files are found, it requests an appropriate full/missing backfill.
- Cache read/write problems do not bypass metric availability or readiness, and do not alter PT configuration acknowledgements, TestMode isolation or global startup SOM state.
- The existing separate legacy one-minute tick-reconstruction and first-seen-date paths were not modified. Those may still have their own startup work.

## Source changes

- `Core/MarketAnalyzer/MarketData/MarketDataWarmStartCache.cs` — compressed atomic persistence.
- `Core/MarketAnalyzer/MarketData/MarketDataService.cs` — restore before pinned refresh and incremental backfill decisions.
- `Core/MarketAnalyzer/MarketData/MarketDataStore.cs` — expose shared validation to the disk reader.
- `Core/MarketAnalyzer/MarketData/BinanceFuturesAnalyticsRuntime.cs` — enable persistence for all three Binance exchange modes.
- `Tests/NormalizedWarmStartCache/` — new eight-group offline harness, project and README.
- `CHANGELOG-2.10.md` — surviving release behavior, synchronized into this documentation repository.

## Verification and limits

**Executed at `925db7c153ee4d53cfe3b7bf736318e7a30bccf1`:** .NET SDK 10.0.403, `dotnet build .\\PTMagic.sln` succeeded in 18.3 seconds for Core, PTMagic and Monitor. `Tests/NormalizedWarmStartCache` 8/8 PASS, `Tests/Phase1AnalyticsReliability` 16/16 PASS, `Tests/Phase1COhlcv` 13/13 PASS: **37/37 focused checks passed**. The existing 272-group accepted deterministic evidence is from older source revisions and is not evidence that this new commit has passed.

A configured cold/restart comparison should record:
- identical exchange, market population, retention and TestMode configuration;
- first-run full-download size and cache-file creation;
- second-run `Normalized warm-start restored ...` count and limited kline requests;
- unchanged availability and representative metric values;
- expected full backfill on an intentionally missing/corrupt series;
- legacy reconstruction as a separately measured path.

Use the focused fail-fast PowerShell script and exact source pin in the [current handoff](../handoffs/2026-11-07-stabilization-correlation-validation.md). Do not restart or duplicate an already-running instance solely to validate the cache. No live API or trade action is authorized by this document.
