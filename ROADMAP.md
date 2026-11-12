# PTMagic 2.10 — User Roadmap

**D-053 implementation checkpoint — November 12, 2026:** PTMagic application source [`892a5f1f4729a3fccd3cb477ba6ad22fbbe0918d`](https://github.com/HojouFotytu/PTMagic/commit/892a5f1f4729a3fccd3cb477ba6ad22fbbe0918d) now removes the three OI/long-short positioning metrics, OI/ratio source acquisition and active cache integrations, obsolete tests, and UI labels. The **24 retained metrics** include 17 global-capable and seven asset-only measurements; settled funding remains with independent safe acquisition. A new user-local .NET build, the reduced **15-harness** offline suite and configured runtime checks are **pending**. The earlier `d101b5a0` 18-harness PASS is **pre-removal evidence**, not validation of the new code. This status **supersedes all earlier “source removal pending” or OI/positioning future-work instructions** in this document; past implementation and validation records are historical. The next step is local validation of `892a5f1f4729a3fccd3cb477ba6ad22fbbe0918d`, not further OI/positioning development.


**Updated:** November 12, 2026 · **Status:** In development · **Current scope:** [D-053](DECISIONS.md#d-053--remove-binance-futures-open-interest-and-longshort-positioning-metrics-from-ptmagic-210)

[Current technical plan](roadmaps/CURRENT.md) · [Development status](STATUS.md) · [Active handoff](handoffs/2026-11-10-som-enable-only.md)

PTMagic 2.10 develops native, transparent market analysis for ProfitTrailer. The approved roadmap emphasizes normalized price/volume, relative strength, correlation, settled funding, taker flow and liquidity. OI and long/short positioning analysis **are no longer approved features**.

## November 12 decision: remove OI and positioning

The owner chose to remove three currently implemented asset-only metrics rather than redesign historical-data acquisition for large populations:

- `OpenInterestChange`
- `OpenInterestValueChange`
- `GlobalLongShortAccountRatio`

Withdraw the corresponding data collectors, active disk-cache dependencies, triggers/registry/export/Monitor integration, and the **future OI/positioning market-wide metric families**. The target registry is **24 metrics: 17 global-capable and 7 asset-only**. Do not keep the withdrawn metrics as an optional SMS-only or legacy product.

**Implementation status:** The removal is an approved plan **not yet applied to PTMagic source**. The latest user-validated source `d101b5a03e01f8f76acf8cc9a6bde7214ff34aa2` still implements 27 metrics. A successful .NET 10.0.403 build and 18/18 offline harnesses at that SHA is historical pre-removal evidence, not evidence of removal.

## Active development order

| Stage | Remaining work |
|---|---|
| **1 — Scope cleanup (next)** | Remove OI/ratio source and metric integrations from the existing `phase1/market-data-foundation` branch; adjust existing tests, diagnostic settings and Monitor labels. Preserve funding, SOM, and market eligibility. |
| **2 — Configured verification** | Confirm remaining metrics, startup/raid behavior, funding persistence, rate-limiter safety and SMS/GlobalSetting selection with appropriate focused offline and runtime evidence. Do not repeat now-irrelevant OI/ratio persistence acceptance. |
| **3 — Taker flow (Phase 2)** | Add `TakerBuyRatio` and `TakerImbalance` with explicit units, complete periods, invalid-data handling and an economical data source; evaluate reusing existing Binance kline taker-buy volume before proposing a new endpoint. |
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
