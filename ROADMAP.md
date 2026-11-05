# PTMagic 2.10 — User Roadmap

**Updated:** November 5, 2026  
**Status:** In active development — this is not a final-release announcement.  
**Application:** [PTMagic](https://github.com/HojouFotytu/PTMagic) · **Detailed plan:** [Technical roadmap](roadmaps/revised-2.10-2026-11-04-markettrend-timeframe.txt) · **Live tracker:** [Development status](STATUS.md)

## The goal

PTMagic 2.10 expands market analysis beyond average price changes. It adds clearer measures of **market direction, breadth, volatility, trading activity and relative strength**, followed by correlation, futures positioning, liquidity and historical evaluation. These measurements can help drive existing Global Settings and Single Market Settings (SMS). The roadmap uses transparent calculations, **not an external AI service**.

## Built and tested — Phases 0, 1A, 1B and 1C

- **Better market data:** Shared five-minute price-and-volume candles, incremental updates, configurable history, and safeguards against incomplete or out-of-date market data. Calculations use each configured MarketTrend timeframe rather than assuming a fixed indicator timeframe.
- **Market direction and breadth:** Average and median price changes, percentage of markets rising, market-wide dispersion, and the difference between average and median performance.
- **Relative performance:** Compare individual markets with the broader market or BTC; identify whether the highest-volume markets are outperforming.
- **Volatility:** Individual and market-wide ATR-based volatility, plus the proportion of markets experiencing elevated volatility.
- **Trading volume:** Volume expansion, the share of markets seeing stronger activity, and how volume is concentrated among leading markets or BTC/ETH.
- **Actionable analytics:** Select the measurements needed for each MarketTrend; reference supported measurements in Global Settings, SMS entry conditions and SMS exit conditions. Missing data cannot be treated as a valid signal. More readable warnings explain why a metric or condition is unavailable.
- **Visibility:** A dedicated **Market Metrics** Monitor page and saved analysis snapshots make the new measurements inspectable.

These core features have passed development tests and Binance Futures TestMode checks. They are **not** a claim that the full 2.10 release is finished.

## Implemented, with additional verification outstanding

- **One PriceTrend calculation system:** The legacy PriceTrend calculator was removed in favor of the normalized system. Existing settings that omit a metric continue to select PriceTrend by default; compatibility behavior for relative SMS comparisons, outlier thresholds and fiat conversion has been restored in code.
- **Simpler exchange support:** Binance Futures, Binance Spot and Binance US remain supported. CoinMarketCap, Bittrex and Poloniex analysis sources were removed.
- **Compatibility and reliability:** The latest PriceTrend changes passed a local .NET 10 build and **88/88 regression checks**. A cold-start fix that keeps markets aligned when a candle closes during a long refresh was also verified on Binance Futures.

**Still to validate:** The latest PriceTrend compatibility changes in live TestMode, Binance Spot and Binance US behavior, fiat conversion with non-USDT quotes, and selected SMS exit/Monitor scenarios. These checks are separate from the completed regression suite.

## What comes next

| Stage | Planned improvement | Benefit |
|---|---|---|
| **1D — Next** | Market correlation and BTC co-movement | Identify markets moving together, independently or in opposite directions. |
| **1E — Partly complete** | More Monitor inspection, independent checks and performance testing | Make indicators easier to interpret and trust. |
| **2 + 2B — Planned** | Futures open interest, funding, trader positioning and buy/sell flow, with market-wide summaries | See whether participation and positioning support price moves. |
| **3 — Planned** | Leverage expansion, crowding, deleveraging and price/flow divergence | Recognize potentially fragile or one-sided market conditions. |
| **4 — Partly complete** | Extend existing Global Setting / SMS trigger support to future measurements | Use additional indicators in the same rule system as they become available. |
| **5 — Planned** | Bid/ask spread, order-book depth, imbalance and liquidity stress | Detect worsening trading conditions and thin liquidity. |
| **6 — Planned** | Historical metric storage and outcome analysis | Review how market conditions and settings behaved over time, without hindsight bias. |

## Scope and release notes

- **No release date is committed.** Completed phases are development-branch milestones, not a production-release guarantee.
- Future metrics are dependent on suitable exchange data, accuracy checks and acceptable resource use. They will be optional where appropriate.
- PTMagic 2.10's market-analysis expansion is separate from the completed **2.9 modernization and CPU-efficiency release**.
- For exact implementation details, acceptance evidence and open issues, use [STATUS.md](STATUS.md) and the [technical roadmap](roadmaps/revised-2.10-2026-11-04-markettrend-timeframe.txt). Those sources take precedence over this simplified overview.
