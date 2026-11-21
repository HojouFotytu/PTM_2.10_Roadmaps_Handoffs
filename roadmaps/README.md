# PTMagic 2.10 Roadmaps

## Current active roadmap — November 19, 2026

**Use [CURRENT.md](CURRENT.md), [D-062](../DECISIONS.md#d-062--trading-need-first-metric-design-and-43-metric-reassessment-november-19-2026) and the [November 19 reassessment handoff](../handoffs/2026-11-19-ptm-210-metric-reassessment.md)** for all new PTMagic analytics planning. The earlier D-053/24/26/35-metric material below is historical source-specific context, not the active feature-development order.

The application currently registers **43 metric names** (30 global-capable / 13 asset-only) with significant derived overlap; D-062 requires **trading need → analytical requirement → existing coverage → justified new measurement → required data/history → Binance/operational feasibility → implementation**. The 96h TestMode store is not a development cap. The four Phase 3 global flow-price volume shares use **≥90% observed frozen-cohort coverage** since `4bbe299e`; no-trade observations count as observed zero-volume, absent observations do not enter turnover sums. Other stricter volume metrics remain distinct. No new candidate—price-path quality, historical regime changes, order-book liquidity or other—is approved merely by its appearance in a roadmap.

**Historical D-053 implementation checkpoint — November 12, 2026 (superseded by later 43-name source):** PTMagic application source [`892a5f1f4729a3fccd3cb477ba6ad22fbbe0918d`](https://github.com/HojouFotytu/PTMagic/commit/892a5f1f4729a3fccd3cb477ba6ad22fbbe0918d) now removes the three OI/long-short positioning metrics, OI/ratio source acquisition and active cache integrations, obsolete tests, and UI labels. The **24 retained metrics** include 17 global-capable and seven asset-only measurements; settled funding remains with independent safe acquisition. A new user-local .NET build, the reduced **15-harness** offline suite and configured runtime checks are **pending**. The earlier `d101b5a0` 18-harness PASS is **pre-removal evidence**, not validation of the new code. This status **supersedes all earlier “source removal pending” or OI/positioning future-work instructions** in this document; past implementation and validation records are historical. This was the next step **at that historical revision**, not an instruction to revisit its obsolete 24-name test suite. The current research order is in D-062 and CURRENT.md.


**D-053 scope (historical November 12):** OI and long/short positioning metrics and their proposed aggregates were withdrawn and subsequently removed. The old 24-name target and pre-removal source status are **superseded**; the current source has 43 registered names and no reinstatement of removed OI/positioning families.

## Current authority

**[CURRENT.md](CURRENT.md)** is the standalone current technical roadmap. [../ROADMAP.md](../ROADMAP.md) is its concise user-facing overview. Current implementation and execution evidence are in [../STATUS.md](../STATUS.md).

## Historical sources

| File | Historical role |
|---|---|
| [original.txt](original.txt) | Original market-analysis expansion proposal |
| [revised-2.9.1-2026-11-04.txt](revised-2.9.1-2026-11-04.txt) | Earlier version designation; superseded when this work became 2.10 |
| [revised-2.10-2026-11-04.txt](revised-2.10-2026-11-04.txt) | Earlier readiness/Phase 1C planning snapshot |
| [revised-2.10-2026-11-04-markettrend-timeframe.txt](revised-2.10-2026-11-04-markettrend-timeframe.txt) | Detailed November 4 plan with the TrendMinutes correction and appended acceptance history |

These files are preserved unchanged. They contain historical statements about a parallel legacy PriceTrend path, completed work, pending tests, metric names, and development order. **They do not override the current source-validity contract, D-062 trading-need-first approval gates, or the distinction between approved development and historical metric quotas.**

Do not resume from a historical “next action” or “current handoff” section. Start with the [November 19 metric reassessment handoff](../handoffs/2026-11-19-ptm-210-metric-reassessment.md) and the [active technical roadmap](CURRENT.md).
