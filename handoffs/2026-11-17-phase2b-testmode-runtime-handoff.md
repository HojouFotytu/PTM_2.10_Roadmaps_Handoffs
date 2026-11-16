# PTMagic 2.10 — November 17 Phase 2B dual-instance runtime handoff

**Current analytics authority.** User-provided files: `PTMagic-Logs-2026-11-16T16-59-19Z.zip` (GeorgeLong) and `PTMagic-Logs-2026-11-16T16-59-24Z.zip` (GeorgeShort), with `PTMagic/2026-11-17.txt`. Application branch `phase1/market-data-foundation`, docs `main`. Running binaries: `ef1f738a1e945db34f4b403f491c0cd4340835e6` in first eight raids per instance, `82ccf4ad7f457e3da9b0fa53067c8eb31a85df90` in final restarted raids. Earlier fix code `0b99efc`, focused test fixture commit `ef1f738`. Current branch HEAD may be later: source proof is the logged revision.

## Observed acceptance

| Dimension | Evidence |
|---|---|
| Completed raids | **18 (9 LONG, 9 SHORT)**; 16 post-cold TestMode decisions conclusive, eight per instance |
| Error/warning | No PTMagic ERROR/CRITICAL entries in either log; all 16 post-cold raid summaries show `Metric warnings: none` |
| First uncached raid | Both **5m24s**, deferred correctly under the **unchanged 300s pinned-age cap**. Normalized fetch LONG **302.724s**, SHORT **302.684s**, **829,726 candles/719 markets** each |
| Startup metadata/1m | Futures metadata LONG **15.396s**, SHORT **15.096s**; legacy 1m reconstruction explicitly **skipped** |
| Steady-state acquisition | Normally **~7–10s**, **2,157 requested candles** per 719-market refresh; no old recurring **~182s / >500k-candle H48** re-fetch in observed raids |
| Whole steady-state raids | **19–27s**; MarketTrend evaluation **~3.9–5.9s** |
| Warm restart | **829,007** validated cached candles restored *per instance*; only **4,294 LONG/4,305 SHORT** candle requests; restarted raids **~26s** |
| Funding | **719/719 eligible** markets verified after cold startup |
| Selection / SMS | `DIAG_G05_VOLUME_VOLATILITY` selected; **710–713** markets with active diagnostic SMS; TestMode preview/unchanged results without sending PT configuration |
| Metric fixture | 35 metrics = 26 global-capable + 9 asset-only; 10 trends M15–H72; eight GS and eleven SMS; final preset **`DEFAULT`** (Linux case-sensitive) |

**Interpretation:** The targeted taker-repair, unnecessary Futures legacy 1m skip, and monitoring-only SMS indeterminacy corrections are **configured TestMode verified** for the observed data. Missing data for SMS that actually changes PT properties or controls processing must still fail closed; no unsafe fallback or fabricated zero. Cold-first-raid time remains unresolved. TestMode does not prove live PT writes, browser rendering or production SOM release.

**Metric architecture:** Five funding global aggregates: median latest verified Regular settlement rate, positive/negative >0/<0 breadth, extreme >=+0.05 / <=-0.05 percentage-point default breadth. Four taker global aggregates: median per-asset taker-buy quote-volume ratio; buyer breadth ratio >0.5; strong buyer breadth ratio ≥0.60 default; cross-sectional population SD of `TakerImbalance=2×ratio−1` (nondirectional). Frozen global MaxMarkets eligible population, ≥ceil(90%×eligible) valid, equal per-market cross-sectional weighting. Calculate only dependencies needed by selected global/SMS metrics. Publish/display **all already calculated values** under their originating timeframe even if not independently selected for triggers. No extra calculations for Monitor; published-but-unselected values remain ineligible trigger references. No OI/positioning/top-trader or leverage-crowding proxies.

## Acceptance boundaries and next steps

The user previously executed `dotnet build .\PTMagic.sln` PASS **10.9s** and `Phase2AdaptiveAcquisition` **9/9 PASS**, but this was **before** `0b99efc`/`ef1f738`. New-source `NormalizedWarmStartCache` and `ConfigurationLifecycle` regression test executions are **not supplied**. The deployed binaries running these raids prove actual runtime execution, not those focused suite PASS claims. If a new code change depends on them, request exact-source `dotnet build`, `dotnet run --project .\Tests\NormalizedWarmStartCache`, `dotnet run --project .\Tests\ConfigurationLifecycle` results.

**Next development:** Phase 3 transparent price/quote-volume/taker-flow confirmation/divergence with explicit units, UTC period alignment, validity and thresholds. **Separate optional optimization:** first-ever cold-start 719-market 96h acquisition under 300s; do not raise freshness or move source pin to fabricate freshness. Shared Binance rate weight with parallel LONG/SHORT instances should be considered. Existing warm-start works and H48 refetch issue need not be reopened without new evidence.

**Separate Monitor/PT Data:** latest source implements **schema 1.3 / one-based PT pagination** with CI 26 PT Data simulations and Monitor Linux/listener tests. New real PT multi-page ZIP acceptance remains unverified; schema-1.2 page-1 repetition is dated historical evidence, not a proven schema-1.3 problem. Monitor Logs ZIP, build tooltip and first-raid waiting UI likewise have separate browser/real-time acceptance boundaries.

**Standing rules:** No new branches, no changes to independent LONG/SHORT Analyzer/DEFAULT settings/strategy repositories. Explain exact GitHub changes before writes and obtain user authorization. Preserve startup SOM enable-only, manual PT release, no writes in TestMode, three-valued safety, source-specific proof. Brief post-settings-deploy PT indicator errors that self-clear are observed transients; investigate persistent faults. Prefer extensive pre-change design analysis with minimal focused preflight execution, deeper simulated API tests for complex pagination.

[Technical roadmap](../roadmaps/CURRENT.md) · [STATUS](../STATUS.md) · [DECISIONS](../DECISIONS.md) · [PTMagic application changelog](https://github.com/HojouFotytu/PTMagic/blob/phase1/market-data-foundation/CHANGELOG-2.10.md).
