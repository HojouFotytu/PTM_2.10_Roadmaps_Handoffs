# PTMagic 2.10 — Metric Reassessment and Next Development Handoff
**Date:** 19 November 2026 · **Status:** Current analytics development authority (D-062) · **Change type:** Documentation only

## 1. Scope and authority

This handoff supersedes the *development order, presumed metric quotas, and "next Phase 4/Phase 5 implementation"* in the November 17 [Dev 10 → Dev 11](2026-11-17-ptm-210-dev10-to-dev11.md) handoff and older metric roadmaps. That older document remains the authoritative record **of its then-observed implementation and testing**, not of the current next-work priority. The [current technical roadmap](../roadmaps/CURRENT.md), [concise roadmap](../ROADMAP.md), [status](../STATUS.md), and [decision register](../DECISIONS.md) must point here for analytics continuation. Independent Monitor/UI, export, and ProfitTrailer LONG/SHORT strategy-settings workstreams remain separate.

**Application repository:** [HojouFotytu/PTMagic](https://github.com/HojouFotytu/PTMagic), existing branch `phase1/market-data-foundation`. Last inspected *functional* source: [`561bbc32`](https://github.com/HojouFotytu/PTMagic/commit/561bbc32c73a567c65348bf655328c5e7a1f5853), incorporating [`4bbe299e`](https://github.com/HojouFotytu/PTMagic/commit/4bbe299e64180ac1aaa9fe2bfccb342def8acad3) no-trade/90%-coverage changes. Its later **documentation-only** HEAD when this handoff was prepared was [`033a65a`](https://github.com/HojouFotytu/PTMagic/commit/033a65a36d3675ca7f6ddab677a0b3ff3b6a5239). Source of full audit and canonical name list: application [`CHANGELOG-2.10.md`](https://github.com/HojouFotytu/PTMagic/blob/phase1/market-data-foundation/CHANGELOG-2.10.md#november-19-2026--trading-need-first-metric-reassessment-documentation-only-design-authority), [`MarketTrendMetrics.cs`](https://github.com/HojouFotytu/PTMagic/blob/phase1/market-data-foundation/Core/MarketAnalyzer/MarketData/MarketTrendMetrics.cs).

**No development approval is implied:** this is an analytical reassessment, not permission to add, remove, implement or retune metrics; change `StoreDataMaxHours`; modify settings, code, tests, new endpoints, production deployments or personal strategy repositories. Explain prospective GitHub writes and obtain explicit authorization. No arbitrary new branches/folders.

## 2. Required hierarchy — binding for future metric decisions

1. **Trading need:** Which observable behavior must PTMagic recognize to improve LONG/SHORT regime selection, entries, exits or risk decisions?
2. **Analytical requirement:** Which reliable information distinguishes that behavior from relevant alternatives?
3. **Existing coverage:** Can current metrics, their underlying observations, multi-horizon combinations or their own recorded history already answer it?
4. **New measurement:** If not, define the smallest additional measurement and demonstrate its incremental analytical value, not merely plausible numerical values.
5. **Data requirements:** Derive observation resolution, timeframe, lookback, history/retention, freshness and market coverage from the necessary measurement.
6. **Acquisition feasibility:** Establish exact Binance API/source semantics, combined LONG+SHORT request-weight budget, operating-capacity and cold/warm/gap recovery.
7. **Implementation:** Only once justified and feasible, change acquisition, cache, retention, calculation, selection/trigger integration, exports, tests and documentation.

**The 96-hour store is an existing TestMode diagnostic setting, not a design or eligibility constraint.** Neither reject a valuable measurement because it requires longer local history nor invent new measurements because existing inputs make them cheap. If needed, increase PTMagic-acquired history with separately validated API/runtime/memory/disk consequences. No reliance on unavailable external historical datasets. Keep the independent, current **300-second pinned analysis-age guard** and fail-closed missing/stale semantics.

## 3. Verified current catalogue — 43 names, not 43 independent signals

**43 canonical metrics: 30 global-capable, 13 asset-only; `PriceTrend` also asset-capable.** No open-interest, top-trader-account-ratio, positioning or inferred leverage/crowding metrics, per D-053.

| Family | Count | Canonical names |
|---|---:|---|
| Price and market structure | 6 | `PriceTrend`, `MedianPriceTrend`, `MeanMedianSpread`, `Breadth`, `Dispersion`, `Concentration` |
| Relative performance and correlation | 5 | `RelativeStrengthMarket`, `RelativeStrengthBTC`, `CorrelationToBTC`, `MeanCorrelationToBTC`, `MedianCorrelationToBTC` |
| Volatility | 3 | `ATRP`, `MedianATRP`, `VolatilityBreadth` |
| Quote-volume and concentration | 8 | `VolumeExpansion`, `MedianVolumeExpansion`, `VolumeExpansionBreadth`, `StrongVolumeExpansionBreadth`, `VolumeConcentration`, `TopNVolumeShare`, `BTCVolumeShare`, `BTCETHVolumeShare` |
| Settled funding | 7 | `FundingRate`, `FundingSum`, `MedianFundingRate`, `PositiveFundingBreadth`, `NegativeFundingBreadth`, `ExtremePositiveFundingBreadth`, `ExtremeNegativeFundingBreadth` |
| Taker-buy/sell flow | 6 | `TakerBuyRatio`, `TakerImbalance`, `MedianTakerBuyRatio`, `BuyerDominanceBreadth`, `StrongBuyerDominanceBreadth`, `TakerImbalanceDispersion` |
| Price/flow agreement-divergence | 8 | `BuyerFlowPriceConfirmation`, `SellerFlowPriceConfirmation`, `BuyerFlowPriceDivergence`, `SellerFlowPriceDivergence` and the four corresponding `VolumeShare` global names |

The system already covers price direction, market breadth, dispersion, within-asset volatility, return leadership, relative strength/correlation, activity expansion, turnover concentration, settled funding and aggressive flow. These are separate economic dimensions even when statistically correlated. Registration, calculation, published visibility, trigger selection, and empirical usefulness are **different milestones**.

### 3.1 Non-independent / overlapping metrics

| Names | Correct interpretation and treatment |
|---|---|
| `TakerImbalance = 2*TakerBuyRatio - 1` | **Exact transformation**, one original taker volume source. Keep aliases if practical for readable triggers, but do not count separately as corroboration. |
| `MeanMedianSpread` | Derived from **unfiltered full mean − median**; note global `PriceTrend` may be outlier-filtered, so using it to reconstruct the full mean can be incorrect. |
| Ordinary/`Strong` volume-expansion breadth and buyer-dominance breadth | Nested threshold categories of the same distribution; need separate practical decision justification. |
| Positive/negative/extreme funding breadth | Related tails of the same distribution; zero rates prevent simple positive+negative=100 identity. Funding is **not** actual leverage or positioning. |
| `VolumeConcentration`, `TopNVolumeShare`, `BTCVolumeShare` and `BTCETHVolumeShare` | Shared turnover population but distinct whole-distribution, leader and BTC/ETH emphasis. Potentially complementary; demonstrate marginal decision value. |
| Four asset `FlowPrice` confirmation/divergence flags | A **single sign-based classification** published as four mutually exclusive non-neutral flag outputs, not four independent information sources. |
| Four `FlowPrice*VolumeShare` globals | Distinct condition-specific **net aggressive quote-volume** contributions, not breadth and not predictive by themselves. Compare with simpler flow/price/volume context. |
| `Dispersion` vs. `ATRP`; market vs. BTC-relative strength | **Not redundant solely by correlation**: different underlying quantities and decisions. |

No metric removal, merged trigger semantics, static threshold change or "count reduction" is preapproved. Reuse shared inputs/calculations and keep cheap useful derived outputs when warranted.

## 4. Current implementation and validation boundaries

- **Latest Phase 3 source behavior:** [`4bbe299e`](https://github.com/HojouFotytu/PTMagic/commit/4bbe299e64180ac1aaa9fe2bfccb342def8acad3) requires **≥90% observed coverage of the fixed eligible cohort** for four global flow-price `VolumeShare` metrics. Source-verified no-trade assets count as observed with zero quote volume, but their per-asset `TakerBuyRatio`, `TakerImbalance` and flags remain unavailable because 0/0 is undefined. Missing/stale/invalid assets do not contribute numerator or denominator and still count as missing coverage. The share is computed against **verified traded quote turnover within the observed subset**, not necessarily the complete population. Zero total turnover remains unavailable. Other quote-volume concentration metrics with 100% requirements remain unaffected. Older `100% Phase 3` specifications are dated historical source contracts.
- **Diagnostic fixture:** single direction-neutral TestMode analyzer, 10 trends M15–H72, 9 GlobalSettings (final uppercase `DEFAULT`), 12 SMS, all 43 registry names selected somewhere; Phase 3 eight H1. Its 96h cache depth was chosen for **that fixture**. An isolated [G08-first diagnostic fixture](https://github.com/HojouFotytu/PTMagic/blob/phase1/market-data-foundation/Tests/Settings/settings.analyzer.phase3-g08-priority.json) exists at `561bbc32`; no newer G08-first live selection is proved by the fixture's existence.
- **User-run historical tests:** after `33a33f0`, `Phase1COhlcv` **20/20 PASS** and `Phase2AdaptiveAcquisition` **9/9 PASS**; `ConfigurationLifecycle` **84/84 PASS** at `303b2e7`. The current `Tests/Phase1COhlcv/Program.cs` calls **22 groups** following newer no-trade/failure-reason additions. **Do not claim 22/22 PASS without execution.**
- **Actual previously deployed TestMode:** two `24d70402` LONG/SHORT runs, seven raids per instance, six conclusive post-cold per instance, all four H1 global Phase 3 shares available `719/719` at *then-current 100% policy*, SMS12 active on 682–692 markets; zero PT writes and no PTMagic ERROR/CRITICAL in supplied logs. Cold first raids ~5m21s correctly deferred under the 300s pinned age limit; steady raids ~19–25s. This is **not** current 90%-rule/new-G08/new-diagnostic runtime acceptance or live trading benefit.
- **Unresolved narrow checks:** re-run all current focused OHLCV groups; inspect later-source classified taker warnings and no-trade/coverage diagnostics in configured TestMode; demonstrate fresh decisive G08 selection using isolated fixture if desired; assess earliest uncached 719-market warm-up without weakening the time guard. These are verification items, not reasons to resume quota-based metric implementation.
- **Do not conflate:** source published, tests passing, configured test calculation, conclusive TestMode decision, actual non-TestMode PT settings delivery, Monitor browser acceptance and improved trade outcomes.

## 5. Trading gaps — assessed in decision order, NOT an approved feature backlog

| Trading decision / behavior | Existing coverage | Missing information | Provisional assessment |
|---|---|---|---|
| LONG/SHORT trend-following versus repeated reversals | Return, multi-horizon breadth/dispersion, ATRP | How directly price progressed versus zigzag travel to the same endpoint | **Strong investigation candidate:** path efficiency from contiguous closed candles; prove extra value beyond returns+volatility. |
| Recognize a developing trend or regime deterioration/recovery | Current multi-horizon breadth, return, volume, taker metrics | *Temporal direction of change of the same observations* and persistence | **First** retain and compare existing metric histories with exact source times/cohort, before registering a new indicator. |
| Protect exits from rapid adverse moves | Short returns, ATRP, breadth/dispersion, flow | Whether the current combination misses coordinated directional shocks | **Conditional** candidate only with demonstrated trading failure. |
| Predict whether a proposed entry/exit is executable with tolerable impact | Quote-volume and activity only | Current bid/ask spread, opposing book depth, side/notional-specific execution cost | **Clear missing native source**; assess all-symbol lightweight quotes and selective depth sampling; no blanket all-market depth polling. |
| Evaluate funding/carry and contract reference dislocation | Historical Regular funding | Next funding-event timing and mark/index basis, *if holding period makes them relevant* | **Conditional** native current observation; do not turn funding into leverage/positioning proxies. |
| Constrain added portfolio concentration | Market correlations, regime and PT asset state | Incremental risk of another position given current correlated holdings, margin and leverage | Portfolio-data/control integration first, not an automatic new global market metric. |

**Illustrative candidate (not approved):** directional path efficiency `E = |ln(C_end/C_start)| / Σ_i |ln(C_i/C_(i-1))|` on a justified contiguous closed-candle window, with separate existing direction and a declared policy for zero aggregate path movement. It can distinguish relatively direct trends from whipsaw paths that end at the same price, but must be compared against existing return/ATRP/dispersion. It does not require external history or a new endpoint if five-minute candles provide adequate resolution.

**Observation timing question:** Phase 3 currently classifies a completed UTC-aligned `TrendMinutes` period, e.g. a full H1, so a value may not change each five-minute raid. A rolling hour of **fully closed five-minute** bars may update sooner without using unfinished candles. Only change alignment after demonstrating a decision benefit and proving no look-ahead, incomplete sources or inconsistent cohort boundaries.

## 6. Data infrastructure follows selected measurements

- **History:** derive actual source count and worst UTC alignment for each metric, not a universal fixed history length. Example: daily ATR(14) requires 15 complete daily bars (360h) plus alignment; prior all-alignment report recommends 384h. Changing retained history is permitted if the trading need warrants it and Binance acquisition/startup cost is feasible.
- **Historical metric persistence:** version and retain time-stamped metric values, exact universe/published/eligible/missing counts, source timestamps, calculation settings and actual selected/applied decisions. The current latest JSON snapshot and initial JSONL audit are **not** complete replay/backtest capability. Use past *available* observations only, no hindsight/reconstructed full-depth history.
- **Resolution:** normalized 5m closed candles initially; finer sampling only if important event detection fails at 5m. Native quote/depth/funding observations need their own sampling and validity contracts.
- **Coverage:** market-count ≥90% is not a guarantee of representative **turnover**. Examine missing-market concentration, cohort changes, inactive EQUITY/INDEX sessions and observed-subset sensitivity without fabricating volumes. Keep full 100% where a distinct metric requires it.
- **Acquisition:** quantify both isolated bot instances on the shared IP quota, native endpoint weights, incremental versus cold and repair traffic, concurrency, memory, storage and pinned-age exposure. A warm raid duration is not evidence that new endpoints or deeper history are feasible cold.
- **Risk/decision testing:** state expected beneficial decision change for LONG and SHORT, compare against *existing metric combinations*, verify source completeness, statistical stability and actual trade-risk/outcome deltas where feasible. Do not use arbitrary thresholds, roadmap quotas or machine availability as evidence of alpha.
- **Integration only after approval:** source client/normalization, on-disk history, runtime metric registry, dependency selection, GlobalSettings/SMS, Monitor and strict three-valued tests. No user-specific strategy changes without a separate request.

## 7. Recommended next workflow and gates

**Gate A — existing coverage and redundancy:** identify concrete cases current metrics misclassify (trend vs chop; strengthening vs weakening; liquid vs merely high-turnover), then determine whether existing multi-horizon inputs or retained metrics suffice. No speculative feature code.

**Gate B — candidate analytical value:** compare path-efficiency/transition candidates to baseline return, breadth, dispersion, ATRP and flow; evaluate executable liquidity separately as missing order-book information. Require falsifiable hypotheses and outcome relevance, not a score invented to populate a roadmap.

**Gate C — source and capacity:** for a candidate surviving B, declare exact native Binance data, timestamps, source completeness, history, update cadence, shared budget and cold/warm burden. Increase PTMagic's own retention if warranted; reject only *proven* infeasibility or insufficient incremental value.

**Gate D — implementation authorization:** write an explicit narrow change plan and obtain owner permission, then implement/test one justified capability at a time. Keep all prior data-validity, startup SOM, freshness, TestMode/no-PT-write and acknowledgement guarantees.

**No "next add Phase 5" mandate.** Spread/depth/slippage are worth investigation because they fill a real gap, not because the previous phase map says Phase 5 follows Phase 4. Post-metric performance scheduling is likewise not a reason to approve irrelevant metrics.

## 8. Required documents and ownership

- **Current authority:** this handoff, [ROADMAP.md](../ROADMAP.md), [roadmaps/CURRENT.md](../roadmaps/CURRENT.md), [STATUS.md](../STATUS.md), and **D-062** in [DECISIONS.md](../DECISIONS.md).
- **App source evidence:** [PTMagic change log](https://github.com/HojouFotytu/PTMagic/blob/phase1/market-data-foundation/CHANGELOG-2.10.md) plus actual registry/engines, and TestMode fixtures under `Tests/Settings`.
- **Historical:** November 17 [Dev 10 → Dev 11](2026-11-17-ptm-210-dev10-to-dev11.md), [Phase 2B acceptance](2026-11-17-phase2b-testmode-runtime-handoff.md), earlier milestone roadmaps and retired OI/positioning work. Keep them for source-specific facts, not as instructions that supersede this decision.
- **Unchanged boundaries:** Monitor 8 independent [handoff](2026-11-17-monitor-8.md); independent user's ProfitTrailer LONG/SHORT DEFAULT/Analyzer/PAIRS/DCA/INDICATORS strategies and their repository; no GitHub modifications without explicit owner direction.

**This handoff is a record of the agreed approach and a precise next-analysis entry point; no code, tests, configurations, new market metrics or deployed behavior were changed.**
