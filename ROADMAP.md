# PTMagic 2.10 — User Roadmap

**Updated:** November 11, 2026 · **Status:** In development

[Current technical plan](roadmaps/CURRENT.md) · [Acceptance status](STATUS.md) · [Current handoff](handoffs/2026-11-10-som-enable-only.md)

PTMagic 2.10 expands native market analysis beyond price trends. It adds breadth, volatility, volume, relative strength, correlation, and later futures positioning and liquidity measurements, using transparent calculations and existing GlobalSetting/SMS controls.

## Current priorities — November 11, 2026

### Dashboard refresh follow-up — open

The top-dashboard **Possible Buys (PBL)** and **Positions** data must refresh reliably. Preserve the existing jQuery `.load()` request and its callback. The authorized correction is **scheduling-only in `Monitor/Pages/Index.cshtml`**; do not replace the transport, add an endpoint/count cache, change PBL/Positions data retrieval or calculations, or alter DashboardTop rendering. Leave DashboardBottom, ticker refresh, tooltip cleanup/reinitialization and profit autocoloring untouched. The November 2 callback-dependent polling path is an investigation lead, not a runtime-confirmed root cause. Explain the exact proposed code change, files and scope before editing, then wait for owner review.

The dashboard was fully rolled back to the pre-experiment source baseline. PBL and Positions still become stale in Monitor; the refresh root cause is not runtime-confirmed. Current zero-limit behavior is the original behavior: the entire Possible Buys card is hidden when `MaxDashboardBuyEntries=0`. The earlier count-card/layout experiment remains withdrawn. No refresh correction has been implemented or accepted yet.

### Next analyzer metric family — Phase 2

**Most recently completed:** Binance USD-M Futures open-interest and settled funding metrics. Funding was the latest completed family: `FundingRate` and `FundingSum`; the preceding OI metrics are `OpenInterestChange` and `OpenInterestValueChange`. The funding/OI tests passed at `49f2aab` and are included in the later full 337/337 offline acceptance at `fb94373`.

**Next:** three distinct per-symbol feeds:

1. Global long/short account ratio — all traders' account participation for that symbol.
2. Top-trader long/short account ratio — account participation among the top 20% by margin balance, each account counted once.
3. Top-trader long/short position ratio — long/short position-size proportions among the top 20% by margin balance.

The endpoint's word **global** means all traders for one symbol, not an exchange-wide aggregate. Account ratios and position ratios are different populations and must remain separate. Binance supports periods from 5m through 1d, returns at most 500 rows per request, and exposes only the latest 30 days; the top-trader endpoints require an API key. Exact PTMagic metric outputs, acquisition windows and UNAVAILABLE/coverage rules must be designed before implementation. [Binance USDⓈ-M Futures market-data API](https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/market-data).

### Acceptance status

SOM and Monitor lifecycle changes passed 16/16 harnesses and 337/337 groups twice at `fb94373`. That result predates later Monitor edits and the dashboard rollback. Live PT API, configured-exchange and browser acceptance remain separate.

[Current technical plan](roadmaps/CURRENT.md) · [Current handoff](handoffs/2026-11-10-som-enable-only.md).

## Accepted foundation

- Shared normalized five-minute OHLCV history with incremental refresh and incomplete-data safeguards.
- Price returns, breadth, dispersion, relative strength, and return concentration.
- Trend-duration ATR and quote-volume measurements.
- Binance USDⓈ-M Futures open-interest and settled funding metrics (`OpenInterestChange`, `OpenInterestValueChange`, `FundingRate`, `FundingSum`).
- Metric-based GlobalSetting, SMS activation, and SMS OffTrigger evaluation.
- Market Metrics inspection, exported snapshots, and grouped diagnostics.
- Unified normalized PriceTrend on Binance Futures, Binance Spot, and Binance US in source; the strongest recorded runtime evidence is for Futures USDT.

The accepted baseline passed a local .NET 10 build, 88 regression checks, and recorded Futures TestMode runs. Those results precede the changes below.

## Implemented — deterministic checks passed, runtime acceptance next

- Reliable delivery state and retries for ProfitTrailer configuration updates.
- Correct removal of the final active SMS.
- Startup native global SOM is **enable-only** under D-047. It blocks new/DCA buys while allowing sells; the **user releases it manually in ProfitTrailer**. Automatic release after a completed raid is obsolete.
- Monitor editing that preserves distinct metric and tag trigger rows.
- Invalid-reference safeguards, request-boundary and decision-age checks, and explicit history requirements.
- Trend-duration ranking for return Concentration.
- Per-market BTC correlation and market mean/median correlation.
- Bounded native decision-history records with configuration/source identity and delivery outcomes.

The latest full offline acceptance is 16/16 harnesses and 337/337 groups, passed twice at exact source `fb94373d8928b681e3ebe1f7209bd1439db42e72`. It includes the SOM and Monitor lifecycle changes, but not the later dashboard rollback. Configured TestMode, actual PT API and browser acceptance remain separate. [Validation evidence](updates/2026-11-10-som-monitor-offline-validation.md).

## Targeted warm-start improvement — source published

The normalized five-minute OHLCV cache now persists closed candles and reuses them after a restart, rather than automatically downloading the full window. This feature is an explicit exception to the later performance-program ordering; other optimization work remains deferred.

**Status:** published at `925db7c`, eight new regression groups passed at `925db7c`, with .NET build and 37/37 focused checks passing; configured two-startup validation pending. It does not eliminate older tick-data reconstruction or first-seen checks.

## November 10 — Startup global SOM made enable-only; two-raid manual-release warning

**Safety correction source:** `891f709010c867259a6cde3df8e9c82781091b7f`, existing PTMagic branch `phase1/market-data-foundation`. The change was subsequently included in the full 16-harness, 337/337 offline acceptance at `fb94373`. The current branch head includes later Monitor changes not covered by that run.

The startup SOM API in PTMagic is now **enable-only**. The application no longer issues global `enabled=false` after normal analysis or configuration delivery, nor from restart/legacy release checkpoints. When `StartupSellOnlyMode=true`, an initial startup may send `enabled=true` to ProfitTrailer before long data loading; the user must manually disable global SOM in ProfitTrailer when ready. Without an ownership-aware live state API PTMagic cannot establish whether SOM is presently on, so it must not claim live-state monitoring or automatic restoration.

The checkpoint is versioned to schema 2 with enable intent, acknowledgement, and manual-review metadata. Old pending-release checkpoints migrate into manual review, never an automatic `false` request. An unacknowledged enable blocks unsafe bootstrap rather than repeatedly overriding manual choices. Normal user-selected settings continue to be delivered after conclusive analysis independently of the global SOM flag. TestMode never sends a remote SOM command.

**User-visible notice:** on the **first two raids of each startup**, when PTMagic requested the SOM guard, the RAID SUMMARY logs a warning to manually release SOM in PT. The shared Monitor ticker row displays a **red `PT: SOM`** badge alongside Selected Global Setting, SMS and PT health, with an information tooltip explaining startup activation, continued block on new/DCA buys, and manual release. The ticker disappears after raid 2; it does not verify the live PT flag or secretly switch it off. The underlying manual-review status remains inspectable in Status Summary.

**Offline acceptance:** SOM lifecycle and first-two-raid notice regressions were included in the 337/337 full-suite PASS at `fb94373`. Do not repeat that completed full suite as a prerequisite for the next metric family. Live PT acknowledgement, ordinary configured raids and Monitor/browser rendering remain separate acceptance steps.

## November 10 — Funding and open-interest deterministic regression PASS

**Verified exact application source:** `49f2aab66592b6e2922097ca5242b5a614090602` · **.NET SDK 10.0.403** · solution build **11.0 seconds** · **16/16** offline harnesses, **332/332** test groups. All **17 funding tests**, **35 open-interest tests**, and **280 pre-existing regression groups** passed. Eight nonfatal nullable warnings remain in two older test harnesses. [Full source-attributed evidence](updates/2026-11-10-phase2-funding-offline-validation.md).

The current source includes an additional **Monitor Global Settings activation-trigger audit** change beyond the previous funding checkpoint. Core/PTMagic/Monitor compilation and 28/28 existing Monitor settings roundtrip checks passed, but the new Monitor screen has **not** been independently browser-tested.

**Acceptance:** Funding and OI **deterministic development tests PASS at this source**. Live Binance history, ordinary configured raids, remote PT API acceptance and user-interface/browser checks are not established by these offline results. The separate specific deferred Phase 1 integration cases remain open. Next Phase 2 code work: distinct account/position long-short ratios with mandatory new unit/regression tests.

## November 10 — Phase 2 funding-rate acquisition and normalization published

**Application implementation source:** `6430bab1afa262fadd4ae31199c11084508b28c7` (`phase1/market-data-foundation`).

Funding history is now an opt-in, Binance USD-M Futures-only data family using the documented `GET /fapi/v1/fundingRate` API, bounded ascending pages and the existing HTTP rate limiter. Each observation retains its native signed decimal `fundingRate`, `fundingTime`, `rateType` (Regular/Special/Unknown), and available `markPrice`; future `premiumIndex` funding estimates are not substituted for settled history.

The two new per-asset metrics are `FundingRate` (latest **Regular** settled rate in the selected MarketTrend) and `FundingSum` (sum of **Regular** settled rates across that MarketTrend). Their output is in **percentage points** (native decimal rate ×100), not annualized. Special funding from stock dividends is separate and not included; an unclassified type makes affected metrics unavailable rather than inventing zero or guessing Regular. Complete funding history must be retrieved before either metric is valid. An exhausted empty period yields a valid zero for the `FundingSum` only; absent regular settlements make `FundingRate` unavailable.

**Dynamic retention contract:** History begins at the longest funding-enabled Exchange MarketTrend's `TrendMinutes`, with no fixed 8-hour rate schedule or independent retention-hours setting. The `FundingMaxRequestsPerRaid` property controls acquisition only (default 60, allowed 0–400; 0 disables). Provider pages are limited to 1000 observations and two pages per selected symbol per raid; incomplete pages remain unavailable until pagination completes. Source is kept in a separate in-memory store and the existing metric/trigger/export/Monitor path is reused. No funding requests are made for configurations without funding metrics, or on Binance Spot/US.

**Verification:** 17 new offline funding case groups have been authored and added to the now **16-project** fail-fast development runner. **No .NET build or execution of these new funding tests has been performed.** The earlier **315/315** deterministic PASS at source `5f51faaa` belongs to the preceding OI-only code, not this new funding source. Separate Phase 1 configured integration testing remains deferred; normal Phase 2 builds and regressions remain mandatory under D-045. The next Phase 2 family is account/position long-short ratios; provider-specific fundingIntervalHours metadata, live funding API acceptance and configured live integration remain pending.

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
| Safety fix — SOM | Enable-only API with manual PT release; red first-two-raid Monitor ticker and warnings published; new offline regression execution required |
| Deferred Phase 1 acceptance | Existing configured runtime, PT API, Monitor and cross-exchange checks remain open; no repeat testing now |
| Phase 2 / 2B | Funding 17/17 and OI 35/35 offline PASS at `49f2aab`; proceed with account/position ratios, then taker flow and market-wide derivatives aggregates |
| Phase 3 | Transparent leverage expansion, crowding, deleveraging, and flow-divergence measurements |
| Phase 4 | Integrate and validate each added metric family in GlobalSettings, SMS, exports, and Monitor |
| Phase 5 | Spreads, depth, slippage estimates, and liquidity stress |
| Phase 6 | Extend the initial decision history into reproducible native historical analysis |
| After all new metrics | Profile and optimize startup, historical reconstruction, snapshot reuse, calculations, logging, network and allocation costs |

**Performance optimization is explicitly scheduled after completion of all approved new metrics.** It is not a prerequisite for continuing the metric roadmap.

PTMagic 2.10 is an application-development project. Personal trading-strategy development is outside this roadmap. No release date or trading-performance claim is implied.
