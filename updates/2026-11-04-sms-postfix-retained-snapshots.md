# 2026-11-04 — Deployed post-fix SMS TestMode reused historical snapshots

**Application fix:** `0e8ab7056d32f16d1095a519ac4a1e87a29a4188`; prior user-run 58/58 deterministic tests passed.

**Uploaded evidence:** Console log 19:05:23–19:07:23 KST, `LastRuntimeSummary(3).json`, `MarketTrendAnalytics(3).json`, `SingleMarketSettingSummary(3).json`.

## Runtime checks

- Normalized futures market refresh: 756/756, 872,424 source candles, 0 failures. Six metric-enabled MarketTrends evaluated; 1h/2h/4h Phase1C metrics available. 8h MedianATRP and MedianVolumeExpansion unavailable as intended with 96h retained data.
- All 15 2h diagnostic GlobalSetting triggers matched; the setting switched, eight SMS across BTC/ETH/SOL built, and TESTMODE suppressed outbound PT writes.
- No ERROR or FATAL log lines. The 8h warnings were fully displayed.

## Critical finding

The newly uploaded `SingleMarketSettingSummary(3).json` still contains unrelated trigger content in each market's first SMS:

| Market | First setting own count | Saved descriptions | Foreign |
|---|---:|---:|---:|
| BTCUSDT | 3 | 9 | 6 |
| ETHUSDT | 4 | 5 | 1 |
| SOLUSDT | 3 | 4 | 1 |

But the `ActivationDateTimeUTC` of **all eight** SMS entries is **2026-11-04T09:32:23Z**, i.e. about 18:32 KST, before the current 19:05–19:07 raid. The configuration embedded in each saved SMS has `RefreshOffTriggers=false`. The runtime log confirms old summaries were loaded. Saving them again preserves the pre-fix descriptions. This run does not verify regeneration with the corrected code and does **not** establish a new code regression.

**To complete acceptance:** In a disposable diagnostics setting, temporarily set `RefreshOffTriggers=true` for at least two active SMS on the same market (prefer BTC first and second). Run one TestMode raid with those triggers matched; ensure `ActivationDateTimeUTC` becomes current; compare each setting's `TriggerSnapshot.MatchedTriggersContent` with its own setting name and trigger count; restore `RefreshOffTriggers=false` after acceptance. Use a backed-up settings copy and avoid resetting persistent real SMS/OffTrigger state. If fresh timestamps show foreign descriptions, re-open the source fix; otherwise close P1C-SMS-SNAPSHOT-ALIAS and Phase1C.

**Status:** Build + deterministic verification complete (58/58); specific fresh-snapshot runtime verification pending. No application changes in this documentation entry.
