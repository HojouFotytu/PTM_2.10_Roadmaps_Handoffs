# PTMagic 2.10 — Temporal metric information: product-wide assessment

**Recorded:** November 22, 2026. **Stage:** Post-45-metric product assessment; **no new metric implementation approved**. **Objective:** accurate **current and evolving market-regime characterization** for any user-configured MarketTrend duration and any user's regime-definition approach. ProfitTrailer entries/exits, profitability, future returns and predictive trading scores are out of scope.

## A. Actual information difference

**Existing 45-name catalogue:** PriceTrend, Breadth, Dispersion, PricePathEfficiency, ATRP, turnover, volume expansion, taker imbalance, funding, relative strength and BTC correlation characterize market conditions **at their respective observation endpoints**. Having different user-configured MarketTrends describes different overlapping intervals, **not necessarily whether the same measurement is strengthening, weakening or persistent as time advances**.

**Observed counterexample, native November 21 GeorgeLong application log:** The archived *configured 60-minute MarketTrend* contained these two valid, eligible-population observations:

| Log time (KST) | Current global PriceTrend | Current Breadth | Current MedianPricePathEfficiency | Change in global PriceTrend from its immediately preceding recorded observation |
|---|---:|---:|---:|---:|
| 19:39:50 | **-0.21647%** | **28.80658%** | **0.21643** | **-0.20024 percentage points** |
| 20:14:50 | **-0.22361%** | **28.80658%** | **0.19127** | **+0.10239 percentage points** |

The population had the same 729 eligible symbols across the retained decision-history snapshots; logged global population counts were also 729 throughout the 90 LONG raids reviewed. The contemporaneous direction/breadth/path measurements are similar, but the same-horizon measured condition was **deteriorating at the first observation and improving at the second relative to each immediately preceding recorded point**. This is not an assertion of a broad market-regime change, nor a forecast. It demonstrates a real **missing temporal perspective**, not a new market data source. Differences in other metrics can coexist with these examples.

**Second, critical observation:** 90 consecutive GeorgeLong raids included 90 reported values for each configured trend, but successive entries are not all independent measurements:

| Existing metric on an archived configured trend | Adjacent raid pairs | Numeric changes | Repeated values |
|---|---:|---:|---:|
| Global PriceTrend, 60-minute trend | 89 | **89** | 0 |
| MedianPricePathEfficiency, 60-minute trend | 89 | **89** | 0 |
| MedianTakerBuyRatio, 60-minute trend | 89 | **7** | **82** |
| MedianTakerBuyRatio, 240-minute trend | 89 | **2** | **87** |

The existing calculations have different observation semantics. PriceTrend and path efficiency use rolling, last-closed-source endpoints. Some flow/volume aggregates use a *fully completed MarketTrend-sized period* and naturally repeat unchanged across raids between its completed boundaries. **Counting repeated raid output as new independent evidence of regime persistence is invalid.** Distinguish *raid time*, *calculation time*, *source period/end timestamp*, and *new observation versus repeated publication*. These 60/240-minute durations are examples from one user's fixture, **not product defaults or requirements**.

GeorgeShort's 93 archived raids showed the same repeating-versus-changing measurement behavior. Logs cover a single market episode; they do not establish universal regime frequencies or numerical thresholds.

## B. What the existing application actually retains

Source reviewed: PTMagic phase1/market-data-foundation at the path-efficiency implementation lineage. Relevant source: [MarketTrendAnalyticsEngine](https://github.com/HojouFotytu/PTMagic/blob/phase1/market-data-foundation/Core/MarketAnalyzer/MarketData/MarketTrendAnalyticsEngine.cs), [snapshot exporter](https://github.com/HojouFotytu/PTMagic/blob/phase1/market-data-foundation/Core/MarketAnalyzer/MarketData/MarketTrendAnalyticsMonitorExporter.cs), [decision-history record](https://github.com/HojouFotytu/PTMagic/blob/phase1/market-data-foundation/Core/Helper/DecisionHistory.cs), and [global setting log snapshot builder](https://github.com/HojouFotytu/PTMagic/blob/phase1/market-data-foundation/Core/MarketAnalyzer/MarketData/GlobalSettingMetricLogSnapshotBuilder.cs).

- **Normalized source candles:** a rolling market-data cache exists; it can potentially support retrospective calculation within the retained, source-valid window. Retaining candles does **not** by itself guarantee recreation of the historical selected global cohort or configuration.
- **MarketTrendAnalytics.json:** exports the **latest** calculated market and asset metric snapshot, not a complete time-indexed feature series.
- **DecisionHistory JSONL:** records actual decision-context metric inputs, data timestamps, covered universes and validity. In the final LONG decision there were **3 global metric inputs**, all the selected G09 median-efficiency triggers, whereas the latest 60-minute snapshot published **26** global metrics. A particular decision-history record is **not an exhaustive archive of all available global metrics**; SMS entries are selectively trigger-based as well.
- **Per-raid INFO logs:** can be used for this offline retrospective audit but are **not a structured, guaranteed complete, comparable historical-feature contract**. Log retention, source acquisition, configuration changes and missing observations prevent assuming that arbitrary user-duration history is always available.

The 26 retained LONG decision-history records and the 26 SHORT records had a stable *set* of 729 global/asset symbols across trends (the volume-ranked **ordering** may change; membership did not). This removes cohort churn as a confound for those observed comparisons only. Other users, other snapshots or different filters **can** change membership; similar aggregate numeric values then need not represent the same population.

## C. Metric-development dispositions — definite, product-wide

| Candidate measurement | Decision | Reason |
|---|---|---|
| **Change in any existing numeric metric between comparable observations of the same configured MarketTrend** | **YES: distinct descriptive dimension; pursue a reusable generic temporal comparison capability** | A current value alone does not encode its measured direction of development. Existing 45 metrics are the numeric inputs; a separate registered ChangeOfPriceTrend, ChangeOfBreadth, ChangeOfFlow, etc. for every metric is unnecessary duplication |
| **Elapsed persistence of a defined observed condition** | **YES as a generic derived temporal description, but DO NOT register a fixed PersistenceScore yet** | Elapsed persistence requires an explicit condition, independent source observations, genuine timestamps and gap/missing-data handling. No universally meaningful preset boundary or score is justified |
| **Regime transition / recovery labels** | **NO new standalone registry names now** | Such labels require a declared regime condition; they are interpretations of observed comparable changes, not independent source measurements. Do not hardcode a universal LONG/SHORT state machine |
| **Acceleration, strengthening-score or confidence-score per metric** | **DO NOT ADD** | Higher-order derivatives or weighted blends are not justified as independently necessary product data. Evaluate only when a distinct missing characterization is demonstrated |
| **New native Binance acquisition endpoint** | **NOT REQUIRED for the demonstrated temporal difference** | Current repeated metric values and normalized candles already furnish the raw information; the unresolved constraint is reliable historical value/provenance comparability, not a new market field |

**This is a metric-information decision, not approval for a generalized data-warehouse redesign.** The correct next gate is a minimal, reusable *temporal metric comparison contract*, not dozens of new registry entries or a rigid fixed horizon/retention system.

## D. Required comparison contract before any implementation

A valid temporal comparison must have the **same metric definition**, same configured TrendMinutes and currency/reference units, and known original configuration identity. For cross-sectional metrics, retain or verify source cohort identity and aggregation/coverage rules; do not silently attribute membership turnover to strengthening or weakening. It must record:

1. Each observation's metric name and scope, actual value, validity/reason, coverage and eligible cohort identity.
2. **Source-period boundary / latest closed-candle timestamp**, pinned calculation time, and whether the source inputs have changed since the prior reported observation.
3. The actual elapsed time between comparable values; a *user-selected* comparison interval or valid source-observation sequence, never an assumed number of raids or hardcoded MarketTrend duration.
4. Explicit UNAVAILABLE for missing prior observation, invalid/stale sources, a gap, incompatible configuration/cohort, or ambiguous timestamp. Never fill a missing prior value with zero or silently compare different populations.
5. History capacity derived from the user's requested comparison and each metric's own underlying source lookback (including fully completed-period and funding settlement semantics). No fixed 96h ceiling or external-history dependency.
6. Evidence that the minimal needed history can be retained/reconstructed under **combined LONG/SHORT acquisition, CPU/RAM/storage and existing 300-second pinned-decision freshness safeguards**. Verify cold, warm and gap recovery before requesting a code change.

A first implementation, **if separately authorized**, should deliver a **single generic prior-versus-current comparable-value operation** for existing metrics. Evaluate persistence duration only after confirming the observation sequence handles duplicated source periods and missing intervals. This is a narrow measurement contract; it does not prescribe particular trigger thresholds, regime choices or trading rules.

## E. Acceptance and next step

**Assessment outcome:** *GO* for specifying a generic source-time-aware **metric-change comparison**; *DEFER* persistence-duration or transition-label implementation until its history and condition definition are validated; *NO-GO* on new per-metric acceleration/persistence score names at this stage. Existing **45 registered measurements remain intact**.

**Next roadmap gate:** validate the generic comparison contract with two or more actual timestamped observations, matched cohort/configuration, repeated fully completed-period values and genuine rolling updates, then establish the smallest retention/compute budget required for arbitrary configured comparisons. Obtain explicit authorization for any PTMagic source/configuration modifications. Do not turn this assessment into a trading-performance project.

**Evidence provenance:** user's supplied November 21, 2026 LONG/SHORT PTMagic logs and _data ZIPs, read-only; no raw private archives or ProfitTrailer settings placed in this repository.
