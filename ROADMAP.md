# PTMagic 2.10 — User Roadmap

**Phase 2 Taker Flow implementation — November 12:** application source [`5b02d4b75d7fcb24782492fa84ed642e0ebbffdf`](https://github.com/HojouFotytu/PTMagic/commit/5b02d4b75d7fcb24782492fa84ed642e0ebbffdf) now contains **26 registered metrics** (17 globally evaluable, nine asset-only), including `TakerBuyRatio` and `TakerImbalance`. The existing kline reader retains index-10 taker-buy **quote** volume, an opt-in exact-period feature engine calculates both metrics, legacy OHLCV cache **v1** remains readable, and cache **v2** persists source-verified taker fields with targeted repair of old cache windows. The existing diagnostic TestMode analyzer was extended in place; Monitor labels/colors and focused tests were updated. **Published and source-inspected; .NET build, new focused test execution and configured taker-flow raid are PENDING.** The earlier D-053 PASS cannot be reattributed to this feature. [Implementation and verification handoff](updates/2026-11-12-phase2-taker-flow-implementation.md).

**Phase 2 Taker Flow — source assessment started November 12:** [Source/persistence review](updates/2026-11-12-phase2-taker-flow-source-review.md) confirms Binance kline index 10 is currently discarded by `BinanceKlineClient`; `MarketCandle` and version-1 normalized warm-start cache contain no taker-buy quote volume. Proposed new asset-only metrics `TakerBuyRatio=B/Q` and `TakerImbalance=2B/Q−1` will reuse the existing pinned 5m kline pipeline, sum exact complete TrendMinutes periods and keep missing data UNAVAILABLE. **Implementation is not yet published**; preserving existing OHLCV cache warm-start behavior while safely refreshing missing taker fields is the principal design requirement. D-053 is closed at configured TestMode level; Phase 2 Taker Flow is the active development track.

**2026-11-12 D-053 configured verification — PASS:** user-run `.NET 10` solution build **PASS (12.9s)** at application source `e31635a1e67347918ca1bbf94d0fb64809b1cea0`; **Phase2Funding 28/28** and **Phase2AdaptiveAcquisition 8/8** (**36/36 focused offline checks**). The user-supplied log and `_data` archive show **four completed TestMode raids**, 519 COIN markets, **519/519 funding history coverage**, **4,169/4,169 available trigger inputs** per decision, **zero completed-raid metric warnings**, successful bulk-only funding acquisition (6/1/1/1 pages; no failures) and fresh determinate decisions. Obsolete OI/ratio warnings preceded the corrected analyzer reload. **D-053 source, focused checks and configured TestMode acceptance are complete**; non-TestMode PT delivery, startup SOM enforcement and Monitor browser acceptance remain unverified. **Next development: Phase 2 taker-flow assessment and implementation; do not repeat retired OI/ratio validation.** [Full D-053 configured evidence](updates/2026-11-12-d053-configured-testmode-validation.md).

**D-053 implementation and removal-audit checkpoint — November 12, 2026:** PTMagic source [`892a5f1f4729a3fccd3cb477ba6ad22fbbe0918d`](https://github.com/HojouFotytu/PTMagic/commit/892a5f1f4729a3fccd3cb477ba6ad22fbbe0918d) contains the completed removal of `OpenInterestChange`, `OpenInterestValueChange` and `GlobalLongShortAccountRatio`, including their acquisition/services/active caches/registry/Monitor integrations. The source audit compared the **22-metric pre-introduction baseline** [`66629347`](https://github.com/HojouFotytu/PTMagic/commit/66629347f0dc9c7b68ea9f1c3f5bf536f3d7c427), **27-metric pre-removal** `d101b5a0` and current **24-metric** code: all 22 original metric identities and scopes survive; `FundingRate` and `FundingSum` also survive. A real shared Unicode symbol-validator dependency was temporarily broken by deleting OI, then repaired by [`02820822`](https://github.com/HojouFotytu/PTMagic/commit/02820822b9bb) and [`d7847c46`](https://github.com/HojouFotytu/PTMagic/commit/d7847c46190b). No further major/critical removal-related defect was established by source inspection; **current-revision local build, 15-harness test execution and configured runtime acceptance remain unverified**. The earlier 18-harness PASS at `d101b5a0` is strictly **pre-removal evidence**. [Full read-only audit](updates/2026-11-12-d053-removal-code-audit.md) (links relative to repository root). **This checkpoint supersedes all contradictory claims below that removal is pending, that retired OI/positioning is active, or that its tests/feature work remain required. Dated implementation evidence is retained as history.** No rollback and no strategy-settings work.


**Updated:** November 12, 2026 · **Status:** In development · **Current scope:** [D-053](DECISIONS.md#d-053--remove-binance-futures-open-interest-and-longshort-positioning-metrics-from-ptmagic-210)

[Current technical plan](roadmaps/CURRENT.md) · [Development status](STATUS.md) · [Active handoff](handoffs/2026-11-10-som-enable-only.md)

PTMagic 2.10 develops native, transparent market analysis for ProfitTrailer. The approved roadmap emphasizes normalized price/volume, relative strength, correlation, settled funding, taker flow and liquidity. OI and long/short positioning analysis **are no longer approved features**.

## November 12 decision: remove OI and positioning

The owner chose to remove three currently implemented asset-only metrics rather than redesign historical-data acquisition for large populations:

- `OpenInterestChange`
- `OpenInterestValueChange`
- `GlobalLongShortAccountRatio`

Withdraw the corresponding data collectors, active disk-cache dependencies, triggers/registry/export/Monitor integration, and the **future OI/positioning market-wide metric families**. The target registry is **24 metrics: 17 global-capable and 7 asset-only**. Do not keep the withdrawn metrics as an optional SMS-only or legacy product.

**Implementation status:** The removal is **applied to PTMagic source and read-only audited**; no current-revision local build or runtime acceptance has been recorded. The last user-validated pre-removal source `d101b5a03e01f8f76acf8cc9a6bde7214ff34aa2` implemented 27 metrics; current source `892a5f1f` implements 24. A successful .NET 10.0.403 build and 18/18 offline harnesses at that SHA is historical pre-removal evidence, not evidence of removal.

## Active development order

| Stage | Remaining work |
|---|---|
| **1 — Scope cleanup (complete; audited)** | D-053 source removal, test configuration, registry and Monitor label cleanup complete. One symbol-validator dependency break was repaired; no rollback. |
| **2 — Configured verification** | Confirm remaining metrics, startup/raid behavior, funding persistence, rate-limiter safety and SMS/GlobalSetting selection with appropriate focused offline and runtime evidence. Do not repeat now-irrelevant OI/ratio persistence acceptance. |
| **3 — Taker flow (Phase 2, implemented; verification pending)** | Validate the published `TakerBuyRatio` and `TakerImbalance` with explicit units, complete periods, invalid-data handling and an economical data source; evaluate reusing existing Binance kline taker-buy volume before proposing a new endpoint. |
| **4 — Market aggregates (Phase 2B)** | Funding median/positive-negative/extreme breadth; taker-flow median buy ratio, dominance breadth and imbalance distribution. Define true eligible/valid populations, weighting, freshness and coverage. |
| **5 — Transparent conditions (Phase 3)** | Price/volume/taker-flow confirmation and divergence. Do not reconstruct removed leverage/crowding/deleveraging signals through undocumented proxies. |
| **6 — Integration and liquidity (Phases 4–5)** | Integrate each retained family in GlobalSetting/SMS, Monitor, exports and history; add spread, depth, imbalance, slippage and liquidity/funding/volatility stress components. |
| **7 — History and performance (Phase 6 onward)** | Expand reproducible decision history. Defer the broader performance program until remaining approved metric additions are complete. |

## What remains available

**17 globally evaluable metrics:** PriceTrend; MedianPriceTrend; MeanMedianSpread; Breadth; Dispersion; Concentration; MedianATRP; VolatilityBreadth; MedianVolumeExpansion; VolumeExpansionBreadth; StrongVolumeExpansionBreadth; VolumeConcentration; TopNVolumeShare; BTCVolumeShare; BTCETHVolumeShare; MeanCorrelationToBTC; MedianCorrelationToBTC.

**7 asset-only metrics:** RelativeStrengthMarket; RelativeStrengthBTC; ATRP; VolumeExpansion; CorrelationToBTC; FundingRate; FundingSum. PriceTrend also supports asset scope and is counted only once in the 24-metric total.

Funding is retained with verified regular-settlement history and bulk acquisition. The removal of OI/ratio does not remove its separate provider capacity or cache.

## Unchanged safety and delivery contracts

- **Startup SOM:** enable-only when configured; PTMagic never sends global SOM OFF, and the user releases it manually in PT.
- **Three-valued decisions:** missing, stale or invalid inputs remain UNAVAILABLE; never invent zero or force DEFAULT.
- **Population:** respect Binance Futures classified underlying-type eligibility and the configured MarketTrend/SMS asset populations; Spot/Binance US behavior remains separate.
- **Monitor:** preserve the restored five-second DashboardTop `.load()` refresh and existing PBL/Positions behavior.
- **Workflow boundary:** PTMagic software/documentation is independent from all personal LONG/SHORT analyzer/strategy/settings development. No PAIRS/DCA/INDICATORS or strategy repository changes are authorized.

## Evidence and history

The user reported a successful .NET 10.0.403 solution build (14.8 seconds), 18/18 offline harnesses and 80 ConfigurationLifecycle checks at `d101b5a0` before D-053. The corrected funding bulk fallback and underlying-type filtering passed their checks. The November 12 live raids proved funding complete (519/519 with one bulk page) and exposed OI/ratio shared request-capacity limitations. Those data points explain the scope choice; they **do not** establish the future source removal.

Earlier OI/ratio source commits, validations and dated development updates are preserved as history in [updates](updates/README.md), [handoffs](handoffs/README.md), Git history and [D-043–D-051](DECISIONS.md). Their old “next” instructions are superseded by D-053.

No application source, production settings, or strategy-settings files were changed by this roadmap revision.
