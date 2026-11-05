# PTMagic 2.10 — User Roadmap

**Updated:** November 5, 2026 · **Status:** In development  
[PTMagic source](https://github.com/HojouFotytu/PTMagic) · [Development status](STATUS.md) · [Full technical roadmap](roadmaps/revised-2.10-2026-11-04-markettrend-timeframe.txt)

PTMagic 2.10 expands market analysis beyond price trends, adding **market breadth, volatility, volume, relative strength, correlation and eventually futures positioning and liquidity analysis** — without an external AI service.

## Completed and tested — Phases 0–1C

- **Market-data foundation:** Shared 5-minute OHLCV history, incremental updates and safeguards against incomplete data; indicators use each MarketTrend's configured timeframe.
- **Price and market strength:** Average/median returns, market breadth, dispersion, relative strength versus the market or BTC, and top-volume market outperformance.
- **Volatility and volume:** ATR-based volatility, volatility breadth, volume expansion, participation breadth, and volume concentration/shares.
- **Trading rules:** Supported metrics can drive Global Settings and SMS entry/exit triggers. Unavailable metrics cannot generate false signals, and diagnostic warnings explain failures.
- **Monitor:** Dedicated Market Metrics page and exported snapshots.

Core Phase 1 features passed regression tests and Binance Futures TestMode.

## Implemented — further testing pending

- **Unified PriceTrend:** Replaced the legacy calculator while retaining implicit PriceTrend settings; restored relative SMS, `TrendThreshold` and fiat-conversion compatibility in code.
- **Exchange cleanup:** Binance Futures, Spot and US remain; removed CoinMarketCap, Bittrex and Poloniex.
- **Reliability:** Fixed candle-boundary inconsistencies during long refreshes (verified on Futures). Latest PriceTrend changes passed a .NET 10 build and **88/88 local regression tests**.

**Outstanding:** Live acceptance of the latest compatibility changes, Spot/US runtime checks, fiat conversion, selected SMS exits and Monitor behavior.

## Upcoming development

| Phase | Focus | Status |
|---|---|---|
| **1D** | Correlation and BTC co-movement | **Next** |
| **1E** | Monitor improvements, validation and performance | Partly complete |
| **2 / 2B** | Futures open interest, funding, positioning, trading flow and market summaries | Planned |
| **3** | Crowding, leverage, deleveraging and price/flow divergence | Planned |
| **4** | Extend metric-based Global Setting and SMS triggers | Partly complete |
| **5** | Spreads, order-book depth and liquidity stress | Planned |
| **6** | Historical metrics, backtesting evidence and outcome analysis | Planned |

**Release status:** No 2.10 release date has been set. This roadmap covers development milestones, not a finished production release. The completed 2.9 modernization is separate. See [STATUS.md](STATUS.md) for the latest verification and outstanding issues.
