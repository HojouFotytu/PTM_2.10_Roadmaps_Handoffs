# PTMagic 2.10 — User Roadmap

**Updated:** November 7, 2026 · **Status:** In development

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

## Implemented in the current checkpoint — validation pending

- Reliable delivery state and retries for ProfitTrailer configuration updates.
- Correct removal of the final active SMS.
- Startup global SOM through PT's API: stop new buys and DCA buys, allow sells, and release after a fresh, conclusive configuration is acknowledged.
- Monitor editing that preserves distinct metric and tag trigger rows.
- Invalid-reference safeguards, request-boundary and decision-age checks, and explicit history requirements.
- Trend-duration ranking for return Concentration.
- Per-market BTC correlation and market mean/median correlation.
- Bounded native decision-history records with configuration/source identity and delivery outcomes.

The latest November 7 user-local run at `86c2ea3` built Core, PTMagic, and Monitor successfully and passed 193 checks across ten harnesses, including 21 correlation, 40 trigger-validation, and 28 Monitor round-trip checks. ConfigurationLifecycle then failed to compile because its fixture used an ambiguous Telegram type reference; DecisionHistory did not run. That reference and the same source-reviewed defect in DecisionHistory are corrected, with execution still pending for both harnesses. Relevant configured runtime checks also remain required. [Validation evidence](updates/2026-11-07-193-check-validation.md).

## Remaining work

| Stage | Work |
|---|---|
| Current acceptance | Validate lifecycle, startup protection, correlation, history, Monitor, and remaining exchange/quote cases |
| Phase 2 / 2B | Open interest, funding, positioning, taker flow, and market-wide summaries |
| Phase 3 | Transparent leverage expansion, crowding, deleveraging, and flow-divergence measurements |
| Phase 4 | Integrate and validate each added metric family in GlobalSettings, SMS, exports, and Monitor |
| Phase 5 | Spreads, depth, slippage estimates, and liquidity stress |
| Phase 6 | Extend the initial decision history into reproducible native historical analysis |
| After all new metrics | Profile and optimize startup, historical reconstruction, snapshot reuse, calculations, logging, network and allocation costs |

**Performance optimization is explicitly scheduled after completion of all approved new metrics.** It is not a prerequisite for continuing the metric roadmap.

PTMagic 2.10 is an application-development project. Personal trading-strategy development is outside this roadmap. No release date or trading-performance claim is implied.
