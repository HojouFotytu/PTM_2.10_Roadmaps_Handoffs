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

## November 10 — Phase 2 offline build and full regression suite PASS

**User-run acceptance evidence:** exact source `5f51faaa0db928cf33c52f6f93ca6f1b301735fb`, .NET SDK **10.0.403**, solution build **11.3 seconds** (Core, PTMagic, Monitor), followed by **15/15 offline harnesses and 315/315 test groups passing**. Phase 2 OI raw mapping passed **18/18** and incremental cache/metric integration passed **17/17**. The preceding `CS4008` test fixture error was corrected at this source. Older nullable-reference warnings remain nonfatal (two in Phase1SmsSummaryIsolation; six in NormalizedPriceTrendMigration).

**Status:** Phase 2 open-interest **deterministic development acceptance complete** at the exact tested source; configured live Binance data acquisition, native PT integration and Monitor/browser acceptance remain unverified. The specific outstanding Phase 1 integration scenarios remain deferred under D-042/D-045, **not** the Phase 2 offline tests. [Full 315-group evidence](updates/2026-11-10-phase2-oi-offline-validation.md).

## November 10 — Testing scope clarified (D-045)

The owner deferred only the specific remaining Phase 1 configured-runtime / PT API / Monitor-browser integration acceptance checks discussed before moving to Phase 2. Phase 2 compilation, deterministic feature tests and affected regressions were **never deferred**. New source must be built and relevant harnesses executed before marking a development batch validated.

The Phase 2 OI source was subsequently built and all 315 offline test groups passed at exact source `5f51faa` on November 10. This section records the original mandatory-testing policy, not the current pending test status. The fail-fast PowerShell runner is available at `Tests/Phase2OpenInterestIncremental/Run-Phase2Validation.ps1` in the application repository. The Phase 1 configured integration checks remain separately pending, not waived.

## Phase 2 started — November 10

**OI retention correction:** Removed the separate `MarketAnalyzer.OpenInterestRetentionHours` property (previously defaulted to 72 hours). Required historical OI observations are now derived from the longest explicitly OI-enabled MarketTrend's `TrendMinutes`, including the exact reference and overlap. The actual provider history window determines availability, not a fixed PTMagic hour ceiling. Request-budget controls remain independent. See [corrected Phase 2 handoff](handoffs/2026-11-10-phase2-open-interest-incremental.md).


Initial raw OI models/client were followed by opt-in, bounded incremental historical acquisition and per-asset OI metric integration at `b723f76`. New settings and explicit metric names are documented in the [Phase 2 incremental handoff](handoffs/2026-11-10-phase2-open-interest-incremental.md). The user subsequently ran and passed 315/315 offline test groups at `5f51faa`; existing configurations do not enable OI automatically. The owner deferred further Phase 1 configured runtime/Monitor/PT acceptance while Phase 2 implementation proceeds. These remaining tests stay pending for release. See the [Phase 2 handoff](handoffs/2026-11-10-phase2-open-interest.md).

## Remaining work

| Stage | Work |
|---|---|
| Deferred Phase 1 acceptance | Existing configured runtime, PT API, Monitor and cross-exchange checks remain open; no repeat testing now |
| Phase 2 / 2B | OI raw source, opt-in bounded acquisition and metric integration implemented and 35/35 new offline groups passed; next funding, positioning, taker flow and aggregates |
| Phase 3 | Transparent leverage expansion, crowding, deleveraging, and flow-divergence measurements |
| Phase 4 | Integrate and validate each added metric family in GlobalSettings, SMS, exports, and Monitor |
| Phase 5 | Spreads, depth, slippage estimates, and liquidity stress |
| Phase 6 | Extend the initial decision history into reproducible native historical analysis |
| After all new metrics | Profile and optimize startup, historical reconstruction, snapshot reuse, calculations, logging, network and allocation costs |

**Performance optimization is explicitly scheduled after completion of all approved new metrics.** It is not a prerequisite for continuing the metric roadmap.

PTMagic 2.10 is an application-development project. Personal trading-strategy development is outside this roadmap. No release date or trading-performance claim is implied.
