# PTM 2.10 — Metric-Catalogue Disposition (Stage A/B Corrected)

**Repository record:** Documentation-only metric-disposition recommendation, not implementation authorization. The evidence files are linked in [audits/README.md](README.md).

**Date:** 2026-11-21. **Source checked:** PTMagic `phase1/market-data-foundation` at `146f56f80601b5ab34b06790d7f311872f037b7f`. **Evidence:** November 19 GeorgeLong `_data` archive. **Scope:** market-regime characterisation only. No PT trading, entry/exit outcomes, or predictive-return scoring.

## Decisions — action now, not another speculative backlog

1. **Retain the 43 existing published registry names**, because no independently demonstrated regime-characterization deficiency justifies deleting an interface. This is *not* 43 independent sources. The source confirms one exact transform (`TakerImbalance`), one four-way sign classification emitted as four binary asset flags, and related distribution cutoffs. Preserve externally usable trigger names.
2. **Do not count `TakerImbalance` as separate informational evidence.** It is exactly `2*TakerBuyRatio - 1`; leave it published as a cheap alias and reuse the underlying per-asset calculation.
3. **Keep ordinary and strong/extreme breadth variants.** The November 19 recorded H1 buyer dominance was 41.655% ordinarily versus 5.103% strongly; H1 volume expansion was 58.897% versus 35.448% strongly; H24 positive funding breadth was 70.345% versus 2.621% extremely positive. These measure different tails, not just repeated numbers.
4. **Recommend one narrow new measurement family for owner approval (no source change):** `PricePathEfficiency` (per-asset) and `MedianPricePathEfficiency` (global) as *one new measurement family*, because endpoint-return / aggregate OHLC cannot reconstruct the price path. Existing normalized closed candles are sufficient in principle; no new endpoint is implied. Do not treat the family as a new trading signal. Implementation still requires explicit owner permission.
5. **No new generic `RegimeStrengthScore`, `RegimePersistenceScore`, artificial shock metric, or turnover-as-liquidity metric.** No demonstrated independent information or validated measurement contract. Do not add source endpoints or metric-history infrastructure solely to populate a catalogue.
6. **Hold native spread/order-book depth measurements for a separate source/data-cost decision**. They characterize possible liquidity-stress regimes but cannot be reconstructed from OHLCV; no broad acquisition is authorized.

## Current catalogue — individual dispositions

| Registered name | Family | Disposition | Regime information / rationale |
|---|---|---|---|
| `PriceTrend` | Price structure | KEEP — PRIMARY | Rolling endpoint return; market aggregation has specific outlier rule; primary directional measurement |
| `MedianPriceTrend` | Price structure | KEEP — DERIVED | Median of eligible market returns; robust center, distinct from filtered mean |
| `MeanMedianSpread` | Price structure | KEEP — DERIVED | Unfiltered mean minus median; detects cross-sectional return asymmetry |
| `Breadth` | Price structure | KEEP — DERIVED | Share of valid markets with positive return; participation independent of return magnitude |
| `Dispersion` | Price structure | KEEP — DERIVED | Cross-market standard deviation of returns; measures disagreement |
| `RelativeStrengthMarket` | Relative performance | KEEP — DERIVED | Asset return minus market median; cross-sectional relative direction |
| `RelativeStrengthBTC` | Relative performance | KEEP — DERIVED | Asset return minus BTC return; different benchmark from market median |
| `Concentration` | Price structure | KEEP — DERIVED | Top10 turnover-ranked mean return minus remaining mean; leadership in returns |
| `ATRP` | Volatility | KEEP — PRIMARY | Within-asset true range, not cross-sectional return dispersion |
| `MedianATRP` | Volatility | KEEP — DERIVED | Median within-asset normalized range; global range intensity |
| `VolatilityBreadth` | Volatility | KEEP — DERIVED | Fraction beyond configured ATRP threshold; distribution, not median |
| `VolumeExpansion` | Volume participation | KEEP — PRIMARY | Current complete-period quote volume relative to historical volume baseline |
| `MedianVolumeExpansion` | Volume participation | KEEP — DERIVED | Typical expansion, robust to outliers |
| `VolumeExpansionBreadth` | Volume participation | KEEP — DERIVED | Extent of activity expansion across markets |
| `StrongVolumeExpansionBreadth` | Volume participation | KEEP — DERIVED | Tail of expansion distribution; Nov19 H1 35.45% vs ordinary 58.90% |
| `VolumeConcentration` | Turnover leadership | KEEP — DERIVED | HHI of turnover weights; whole-distribution concentration |
| `TopNVolumeShare` | Turnover leadership | KEEP — DERIVED | Turnover share of selected top N; distinct from HHI |
| `BTCVolumeShare` | Turnover leadership | KEEP — DERIVED | BTC share of turnover; special leader interpretation |
| `BTCETHVolumeShare` | Turnover leadership | KEEP — DERIVED | BTC+ETH share; difference from BTC-only is ETH component |
| `CorrelationToBTC` | BTC synchronization | KEEP — PRIMARY | Asset/BTC synchronized return correlation |
| `MeanCorrelationToBTC` | BTC synchronization | KEEP — DERIVED | Mean cross-market BTC correlation; sensitive to tails |
| `MedianCorrelationToBTC` | BTC synchronization | KEEP — DERIVED | Median BTC correlation; resistant to outliers |
| `FundingRate` | Settled funding | KEEP — PRIMARY | Latest verified Regular settlement in selected window; no positioning inference |
| `FundingSum` | Settled funding | KEEP — DERIVED | Sum of verified settlements; accumulative, not equal to latest |
| `MedianFundingRate` | Settled funding | KEEP — DERIVED | Typical settled funding across eligible markets |
| `PositiveFundingBreadth` | Settled funding | KEEP — DERIVED | Share with positive Regular funding; sign distribution |
| `NegativeFundingBreadth` | Settled funding | KEEP — DERIVED | Share with negative Regular funding; zeros mean not necessarily complement |
| `ExtremePositiveFundingBreadth` | Settled funding | KEEP — DERIVED | Positive extreme tail distinct from sign breadth; Nov19 H24 2.62% vs positive 70.35% |
| `ExtremeNegativeFundingBreadth` | Settled funding | KEEP — DERIVED | Negative extreme tail distinct from sign breadth |
| `TakerBuyRatio` | Aggressive flow | KEEP — PRIMARY | Source-verified buyer aggressor quote volume over total quote volume |
| `TakerImbalance` | Aggressive flow | KEEP — ALIAS | Exactly 2*TakerBuyRatio - 1; retain as trigger-facing convenience, never independent evidence |
| `MedianTakerBuyRatio` | Aggressive flow | KEEP — DERIVED | Typical buyer aggressor share across eligible markets |
| `BuyerDominanceBreadth` | Aggressive flow | KEEP — DERIVED | Fraction of markets >0.5 taker buy ratio; market participation |
| `StrongBuyerDominanceBreadth` | Aggressive flow | KEEP — DERIVED | High-dominance tail; Nov19 H1 5.10% vs ordinary 41.66% |
| `TakerImbalanceDispersion` | Aggressive flow | KEEP — DERIVED | Spread of individual aggressor balances; derived from same ratios but not their median |
| `BuyerFlowPriceConfirmation` | Price/flow class | KEEP — CLASSIFICATION | One of four outputs of sign-based aligned price/flow classification; trigger convenience |
| `SellerFlowPriceConfirmation` | Price/flow class | KEEP — CLASSIFICATION | One of four outputs of sign-based aligned price/flow classification; trigger convenience |
| `BuyerFlowPriceDivergence` | Price/flow class | KEEP — CLASSIFICATION | One of four outputs of sign-based aligned price/flow classification; trigger convenience |
| `SellerFlowPriceDivergence` | Price/flow class | KEEP — CLASSIFICATION | One of four outputs of sign-based aligned price/flow classification; trigger convenience |
| `BuyerFlowPriceConfirmationVolumeShare` | Price/flow class | KEEP — COMPONENT | Net aggressor-weighted contribution of buyer-aligned price rises / total observed turnover |
| `SellerFlowPriceConfirmationVolumeShare` | Price/flow class | KEEP — COMPONENT | Net aggressor-weighted contribution of seller-aligned price falls / total observed turnover |
| `BuyerFlowPriceDivergenceVolumeShare` | Price/flow class | KEEP — COMPONENT | Net aggressor-weighted contribution of buyer-aggressive price falls / total observed turnover |
| `SellerFlowPriceDivergenceVolumeShare` | Price/flow class | KEEP — COMPONENT | Net aggressor-weighted contribution of seller-aggressive price rises / total observed turnover |

## One new, specifically defined measurement family

### `PricePathEfficiency` (asset) / `MedianPricePathEfficiency` (global)

For an arbitrary user-configured `TrendMinutes=T` supported by the normalized source interval, require the **T/interval + 1** consecutive, fully closed, valid candle closes ending at the raid-pinned latest closed endpoint. Let `C_0, ..., C_N` be those closes:

\[ E_T = \frac{|\ln(C_N/C_0)|}{\sum_{i=1}^{N}|\ln(C_i/C_{i-1})|} \]

- `0 ≤ E ≤ 1` for positive valid prices. The metric is signless; directional sign comes from existing `PriceTrend`. `E=1` means the observed closes moved monotonically in one direction; lower values mean more reversal travel relative to net distance.
- **Undefined denominator (all observed close changes exactly zero)**: UNAVAILABLE with explicit reason, not fabricated `0` or `1`. Distinguish from missing/invalid source history.
- **Gap/misalignment/insufficient retention**: UNAVAILABLE. No interpolation, external database, or current incomplete candle.
- **Global result:** median across eligible and valid asset efficiencies for the same configured `T`, with existing cohort/coverage validity rules; always preserve valid/eligible counts.
- **Avoid cross-horizon raw comparisons.** Longer path length mechanically drives smaller efficiencies under typical fluctuating price paths. A value at one configured duration cannot be interpreted using another duration’s reference thresholds; no fixed global cutoffs are proposed.
- **Source limitation:** efficiency uses normalized candle closes, so price reversals hidden entirely within each five-minute candle are not resolved; do not claim full intrabar path knowledge.

### Reproducible observed variation (not predictive backtesting)

From the same valid closed candles on November 19, 15:19:59.999 UTC, across all **ten configured durations** in the archive:

| Configured diagnostic horizon | Valid markets | Median efficiency | 10th–90th percentiles | Correlation with absolute contemporaneous return |
|---|---:|---:|---:|---:|
| M15 (15m) | 725 | 1.0000 | 0.5361–1.0000 | 0.324 |
| M30 (30m) | 725 | 0.4774 | 0.1702–0.7263 | 0.443 |
| H1 (60m) | 725 | 0.3218 | 0.0838–0.5595 | 0.445 |
| H2 (120m) | 725 | 0.2290 | 0.0534–0.4395 | 0.473 |
| H4 (240m) | 725 | 0.1209 | 0.0271–0.2841 | 0.616 |
| H6 (360m) | 725 | 0.0897 | 0.0203–0.2169 | 0.640 |
| H12 (720m) | 725 | 0.0525 | 0.0096–0.1504 | 0.674 |
| H24 (1440m) | 725 | 0.0323 | 0.0043–0.0947 | 0.660 |
| H48 (2880m) | 719 | 0.0243 | 0.0045–0.0763 | 0.621 |
| H72 (4320m) | 719 | 0.0206 | 0.0033–0.0623 | 0.611 |

These are *diagnostic configurations only*. They impose no product horizon or history-retention duration. Variation and incomplete correlation establish distinct descriptive content, **not** that the new measurement is automatically useful as a regime selector. The observed fall in median efficiency with duration is a real comparability limitation.

## Exclusions and gate

- **Retained:** all current metric interfaces; no deletions, renamed triggers, metric-family count targets, application edits, or PT/settings changes.
- **First proposed development:** the tightly scoped two-output **path-efficiency** family, pending owner authorization and a focused correctness test that contrasts same aggregate OHLC/turnover with different internal closed-candle paths.
- **Do not advance** unrelated positioning/OI, forward-return prediction, arbitrary signal scores, volume-as-executable-liquidity or unconstrained new native API collection.
- The same-horizon metric can be verified on synthetic complete/gapped/flat source candle sequences and source-of-truth archived native candles, plus an assessment of whether it disambiguates genuine sustained versus choppy *observed* market structure; predictive trade outcomes are explicitly excluded.

## Boundaries

Publishing this document changes repository documentation only. No PTMagic code, metrics, runtime behavior, Analyzer settings, or trading configuration was changed by this assessment. The register is a **completed disposition recommendation**, not an implemented metric or a user-approved change to the running analyzer.