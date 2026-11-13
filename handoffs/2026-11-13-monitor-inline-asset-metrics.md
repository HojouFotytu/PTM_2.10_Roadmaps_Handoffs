# PTMagic 2.10 Monitor — Expandable asset metrics handoff

**Date:** November 13, 2026 (KST)  
**Application:** [PTMagic](https://github.com/HojouFotytu/PTMagic/tree/phase1/market-data-foundation) / existing `phase1/market-data-foundation` branch  
**Inspected HEAD:** `5f09cd3d2da1bc87ccfca990170f7d24dc047767`  
**Documentation:** `HojouFotytu/PTM_2.10_Roadmaps_Handoffs` / `main`  
**Earlier Monitor handoff:** [November 11 DashboardTop refresh](2026-11-11-monitor-dashboard-refresh-resolved.md)  
**Related:** [STATUS](../STATUS.md) · [DECISIONS](../DECISIONS.md) · [Roadmap](../roadmaps/CURRENT.md)

## Current implementation

The owner rejected a dedicated Per-Market Metrics table/page, then approved **expandable metrics inside the existing Market Analyzer market rows**. The original standalone view remains removed; `MarketMetrics.cshtml` remains a redirect.

- [`f70c0e1`](https://github.com/HojouFotytu/PTMagic/commit/f70c0e1b7bb0171066998acb84d39c5b1aeac57a) added collapsed-by-default chevrons and inline metric details.
- [`68ee15c`](https://github.com/HojouFotytu/PTMagic/commit/68ee15c0d693d3a63003ed4e1de9d0333354e9c1) corrected the missing green/red colors based on raw feature numbers.
- The initial changes affected only `Monitor/Pages/MarketAnalyzer.cshtml` and `Monitor/Pages/MarketAnalyzer.cshtml.cs`; no new page, folder, branch, data source, API acquisition, analytics calculation, or strategy change was part of these commits.

## Required layout and behavior

1. The existing **Market-Wide Metrics** grouped panel remains unchanged. Do **not** add asset metrics to its market-wide aggregates.
2. In the existing **Absolute Trend Changes** and **Relative Trend Changes** tables, show a chevron beside each market that has applicable configured asset-scoped metrics. All start collapsed; expanded metric labels are indented beneath the market name.
3. Values appear **under the MarketTrend column that requested them**, not a separate metric/timeframe grid. Display only explicitly configured asset-scope metrics from the displayed Exchange MarketTrends (`DisplayOnMarketAnalyzerList`) and only for symbols in that trend's selected `AssetSymbols`.
4. Omit unconfigured/inapplicable cells. For configured, missing/invalid/stale/unpublished features, show `--` with an explanatory tooltip; never fabricate zero.
5. `PriceTrend` already appears in the parent row. Do not add duplicate PriceTrend detail rows; a blank `Metrics` field alone does not create extra rows.
6. Asset metric values are **native and identical** in Absolute and Relative modes; only the existing price-trend figures use those modes. Switching modes collapses detail rows.
7. Tablesaw sort must collapse rows before sorting, so no metric row detaches from its market. Only expand to create detail DOM rows, not a permanent multiplication of hundreds of market rows.

The page model uses the existing `MarketTrendAnalytics.json` `AssetMetrics` snapshot and escapes JSON for the Razor script. Client code inserts the detail rows; no new provider calls occur on expansion.

## Value color policy

Color classes `text-success` (green), `text-danger` (red), `text-muted` (neutral) are calculated from the **unrounded raw value**, not the formatted text.

| Metric | Green | Red | Neutral |
|---|---|---|---|
| Signed values: funding, strength, correlation, `TakerImbalance` | `>0` | `<0` | `0` |
| `VolumeExpansion` | `>1.0x` | `<1.0x` | `1.0x` |
| `TakerBuyRatio` | `>0.5` | `<0.5` | `0.5` |
| Invalid, stale, missing or unpublished | Never | Never | `--` |

These are numeric direction/reference colors, **not** profitability signals.

## Active metric scope (D-053 / D-054)

The inspected branch has **26 registered metrics: 17 globally usable, nine asset-only**. Only configured ones appear in expanded rows. Nine eligible asset-only names: `RelativeStrengthMarket`, `RelativeStrengthBTC`, `ATRP`, `VolumeExpansion`, `CorrelationToBTC`, `FundingRate`, `FundingSum`, `TakerBuyRatio`, `TakerImbalance`.

**Do not restore withdrawn metrics** from the earlier discussion's illustration: `OpenInterestChange`, `OpenInterestValueChange`, `GlobalLongShortAccountRatio`, and the two top-trader ratio feeds are removed by prior decisions. The old long/short ratio's 1.0 neutral color rule is obsolete. `TakerBuyRatio` and `TakerImbalance` arrived later from kline-derived taker flow and are dependent measures, not independent sources.

## Verification / next check

- **Initial implementation:** User ran `git pull --ff-only` and `dotnet build .\PTMagic.sln` — Core/PTMagic/Monitor **PASS in 11.1 seconds**. The output did not print a SHA. User then reported **“All good, except the values aren't colored correctly.”** This confirms the general browser layout, **not** value colors.
- **Color correction:** Commit `68ee15c` was published and confirmed on GitHub. The user has **not yet reported a post-color-correction browser check** in this conversation.
- **Later source-specific build:** At `f7d802f`, user ran solution build **PASS (16.1s)** and **33/33 focused offline checks PASS** (Phase1COhlcv 15, NormalizedWarmStartCache 10, Phase2AdaptiveAcquisition 8). This includes the prior Monitor work but does not prove live browser colors.
- **Current inspected source:** `5f09cd3` retains the inline display and newer taker metrics; do not confuse its HEAD with the SHA in the earlier 11.1-second build.

Narrow browser acceptance remaining: expand a market, check correct value alignment/tooltip, green/red/neutral against 0 / 1.0 / 0.5, and `--` availability. Then switch Absolute/Relative and sort. Verify the Market-Wide panel and main DashboardTop refresh remain unaffected. No need to rerun large previous test suites simply for this.

## Workstream rules

Before any GitHub edit explain exact files/behavior, and do not create branches, new folders, duplicate components or unrequested UI changes. Keep PTMagic application development separate from LONG/SHORT strategy settings (D-052). Preserve the [DashboardTop refresh fix](2026-11-11-monitor-dashboard-refresh-resolved.md) and the [design-only Performance Export handoff](2026-11-13-monitor-performance-export-design.md), which is an independent future task.
