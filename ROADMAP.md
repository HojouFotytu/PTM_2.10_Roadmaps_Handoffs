# PTMagic 2.10 — User Roadmap

**Updated:** November 10, 2026 · **Status:** In development

[Current technical plan](roadmaps/CURRENT.md) · [Acceptance status](STATUS.md) · [Current handoff](handoffs/2026-11-07-stabilization-correlation-validation.md)

PTMagic 2.10 expands native market analysis beyond price trends. It adds breadth, volatility, volume, relative strength, correlation, and later futures positioning and liquidity measurements, using transparent calculations and existing GlobalSetting/SMS controls.

## Accepted foundation

- Shared normalized five-minute OHLCV history with incremental refresh and incomplete-data safeguards.
- Price returns, breadth, dispersion, relative strength, and return concentration.
- Trend-duration ATR and quote-volume measurements.
- Metric-based GlobalSetting, SMS activation, and SMS OffTrigger evaluation.
- Market Metrics inspection, exported snapshots, and grouped diagnostics.
- Unified normalized PriceTrend on Binance Futures, Binance Spot, and Binance US in source; the strongest recorded runtime evidence is for Futures USDT.

The accepted baseline passed a local .NET 10 build, 88 regression checks, and recorded Futures TestMode runs. Those results precede the changes below.

## Implemented — deterministic checks passed, runtime acceptance next

- Reliable delivery state and retries for ProfitTrailer configuration updates.
- Correct removal of the final active SMS.
- Startup global SOM through PT's API: stop new buys and DCA buys, allow sells, and release after a fresh, conclusive configuration is acknowledged.
- Monitor editing that preserves distinct metric and tag trigger rows.
- Invalid-reference safeguards, request-boundary and decision-age checks, and explicit history requirements.
- Trend-duration ranking for return Concentration.
- Per-market BTC correlation and market mean/median correlation.
- Bounded native decision-history records with configuration/source identity and delivery outcomes.

All 272 checks across twelve harnesses have now passed: 193 checks in ten harnesses at `86c2ea3`, followed by 66 lifecycle and 13 history checks at `d331fbd`. The latest build succeeded in 10.9 seconds with .NET SDK 10.0.403. This completes deterministic acceptance across the two recorded revisions; configured TestMode, actual PT API, and browser checks remain. [Validation evidence](updates/2026-11-07-completed-harness-validation.md).

## Targeted warm-start improvement — source published

The normalized five-minute OHLCV cache now persists closed candles and reuses them after a restart, rather than automatically downloading the full window. This feature is an explicit exception to the later performance-program ordering; other optimization work remains deferred.

**Status:** published at `925db7c`, eight new regression groups passed at `925db7c`, with .NET build and 37/37 focused checks passing; configured two-startup validation pending. It does not eliminate older tick-data reconstruction or first-seen checks.

## Phase 2 started — November 10

**OI retention correction:** Removed the separate `MarketAnalyzer.OpenInterestRetentionHours` property (previously defaulted to 72 hours). Required historical OI observations are now derived from the longest explicitly OI-enabled MarketTrend's `TrendMinutes`, including the exact reference and overlap. The actual provider history window determines availability, not a fixed PTMagic hour ceiling. Request-budget controls remain independent. See [corrected Phase 2 handoff](handoffs/2026-11-10-phase2-open-interest-incremental.md).


Initial raw OI models/client were followed by opt-in, bounded incremental historical acquisition and per-asset OI metric integration at `b723f76`. New settings and explicit metric names are documented in the [Phase 2 incremental handoff](handoffs/2026-11-10-phase2-open-interest-incremental.md). Tests are authored but have not been executed; existing configurations do not enable OI automatically. The owner deferred further Phase 1 configured runtime/Monitor/PT acceptance while Phase 2 implementation proceeds. These remaining tests stay pending for release. See the [Phase 2 handoff](handoffs/2026-11-10-phase2-open-interest.md).

## Remaining work

| Stage | Work |
|---|---|
| Deferred Phase 1 acceptance | Existing configured runtime, PT API, Monitor and cross-exchange checks remain open; no repeat testing now |
| Phase 2 / 2B | OI raw source foundation published; next opt-in bounded acquisition, metric integration, funding, positioning, taker flow and aggregates |
| Phase 3 | Transparent leverage expansion, crowding, deleveraging, and flow-divergence measurements |
| Phase 4 | Integrate and validate each added metric family in GlobalSettings, SMS, exports, and Monitor |
| Phase 5 | Spreads, depth, slippage estimates, and liquidity stress |
| Phase 6 | Extend the initial decision history into reproducible native historical analysis |
| After all new metrics | Profile and optimize startup, historical reconstruction, snapshot reuse, calculations, logging, network and allocation costs |

**Performance optimization is explicitly scheduled after completion of all approved new metrics.** It is not a prerequisite for continuing the metric roadmap.

PTMagic 2.10 is an application-development project. Personal trading-strategy development is outside this roadmap. No release date or trading-performance claim is implied.
