# PTMagic 2.10 — Price-path efficiency: LONG/SHORT TestMode acceptance

**Recorded:** November 22, 2026. **Decision:** **ACCEPTED / CLOSED** for the approved path-efficiency measurement family. The two new published metrics, **PricePathEfficiency** (asset) and **MedianPricePathEfficiency** (global), have passed focused offline validation and the remaining GlobalSetting/SMS TestMode integration check.

## Exact evidence

**Application tested:** PTMagic source revision [f75f229](https://github.com/HojouFotytu/PTMagic/commit/f75f229f87b420bcf35a422b9063f1e181559e01), including metric implementation [49dd01f](https://github.com/HojouFotytu/PTMagic/commit/49dd01f438f1c75f88a8873ff8e86bc1738f8d9b). The single canonical test analyzer was updated to **v2.5.1** at [cca206c8](https://github.com/HojouFotytu/PTMagic/commit/cca206c8fa0e68e8bd657f7e93c0ba9779346488); G09 was intentionally placed ahead of the other diagnostic GlobalSettings. Later repository HEADs are **not** claimed to have undergone new runtime acceptance merely by virtue of being newer.

**Owner-run .NET checks:** solution build succeeded in **15.0 seconds**; Phase1COhlcv **25**, Phase2AdaptiveAcquisition **9**, ConfigurationLifecycle **84** passed (118 focused checks). Two CS8625 nullable-reference warnings were reported in the OHLCV test project; the build and suites still passed.

**User-supplied archived TestMode evidence:**

- PTMagic-_data-GeorgeLong-2026-11-21T14-37-11Z.zip; PTMagic-Logs-GeorgeLong-2026-11-21T14-37-06Z.zip
- PTMagic-_data-GeorgeShort-2026-11-21T14-53-40Z.zip; PTMagic-Logs-GeorgeShort-2026-11-21T14-53-37Z.zip

The raw user archives remain user-provided evidence, **not repository attachments**. The following results were rechecked against their decision-history JSONL, LastRuntimeSummary, latest MarketTrendAnalytics snapshot and application logs.

| Acceptance criterion | GeorgeLong | GeorgeShort |
|---|---:|---:|
| Fresh, determinate decisions selecting DIAG_G09_PATH_EFFICIENCY | **13** | **16** |
| Latest TestMode | **true** | **true** |
| Latest delivery status | **TestMode unchanged** | **TestMode unchanged** |
| Selected global medians valid (M30 / H1 / H4) | **3/3** | **3/3** |
| Latest M30 asset efficiency available | **726/729** | **722/729** |
| Latest H1 asset efficiency available | **729/729** | **729/729** |
| Latest H4 asset efficiency available | **729/729** | **729/729** |
| ERROR/CRITICAL application log entries | **0** | **0** |

The final global medians satisfy the existing 90% eligible-cohort coverage gate. Each latest accepted G09 decision references the contemporaneous pinned closed-candle endpoint. The three SMS13 asset triggers are recorded separately for each market; current M30 availability was 726 or 722 respectively, not 729. **Do not equate the number of retained active SMS settings with the count of current positive trigger evaluations:** SMS13 has no OffTriggers and existing active settings may persist.

**Known nonblocking case:** a source-verified fully flat path yields an undefined 0/0 efficiency, correctly **UNAVAILABLE**, not zero. Such cases were grouped as warnings in the observed logs. Cleaner classification is a separate reporting issue, not a reason to reject the metric or rerun this acceptance.

## Final scope and continuation

**Close the path-efficiency metric implementation and acceptance milestone.** Catalogue: **45 names (31 global-capable, 14 asset-only)**. The single TestMode analyzer remains **Tests/Settings/settings.analyzer.json**; no second fixture is authorized.

The next metric-development work package is **temporal observation and regime transitions**, assessed independently of ProfitTrailer trading performance and predictive returns. See the [temporal metric information audit](2026-11-22-temporal-metric-information-audit.md).

This is a documentation-only acceptance record. No additional PTMagic source, runtime configuration, strategy, retention, or native data-acquisition changes are made.
