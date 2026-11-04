# PTMagic 2.10 — Pinned candle boundary fix verified on Binance Futures

Date: 2026-11-05 KST
Application: HojouFotytu/PTMagic
Source commit: 0c31e58451a563406c214dee3438f0812e980ae6
TestMode: enabled, no ProfitTrailer writes
Prior local validation: Core/PTMagic/Monitor .NET 10 build PASS, all 82 regression tests PASS

## Background

Prior Binance Futures cold-start raid crossed a 5m close while downloading historical candles and subsequently expected a too-new closed endpoint for series fetched earlier. This produced 179/250 global and 365/519 asset valid returns, with 31 warning groups, despite no failed Binance fetches. Fix pins the analysis as-of timestamp to the start of the normalized refresh.

## User-supplied runtime evidence

### First raid (00:32:04–00:46:03 KST)

- Legacy first-seen checks and full legacy market-data reconstruction consumed most of the 13m59s elapsed time.
- Normalized refresh started at 00:43:58.0709779 KST and finished at 00:46:02.192 KST, crossing the 00:45 five-minute boundary.
- 756/756 series refreshed; 872,424 candles received; 0 skipped; 0 failed; store capacity 1154 candles/series for `StoreDataMaxHours=96`.
- Log: `normalized MarketTrends evaluate as of 2026-11-04T15:43:58.0709779+00:00 (pinned to kline refresh start)`.
- Expected closed endpoint for every configured MarketTrend: `2026-11-04T15:39:59.9990000+00:00`, correctly fixed to last close preceding the refresh start.
- Across return-based MarketTrends: global returns 250/250 (100%) and asset returns 519/519 (100%), or filtered 1/1 and 2/2 where configured. No global or asset invalid return reasons.
- Seven expected diagnostic metric-warning groups: SOL excluded by IgnoredMarkets, asset-only ATRP requested by GlobalSetting, explicit PriceTrend not enabled, and four deliberately insufficient eight-hour metrics.
- `DIAG_Global_All15AndImplicit` triggered and was selected; PT writes suppressed by TestMode.

### Second raid (00:46:04–00:46:14 KST)

- 404/756 series refreshed; 352 skipped; 1,212 candles received; 0 fetch failures.
- Pinned as-of: `2026-11-04T15:46:04.7275780+00:00`.
- Expected closed endpoint: `2026-11-04T15:44:59.9990000+00:00`.
- Full coverage retained, 250/250 global and 519/519 asset; same seven expected diagnostic warnings.
- No GlobalSetting switch or reapplication; no ProfitTrailer config update.

## Acceptance result

**Binance Futures live cold-start boundary-consistency: PASS.** Previous false missing-endpoint issue does not recur despite a refresh spanning a 5m boundary. Existing 82/82 local regression pass remains valid for this source commit. All seven remaining warnings are intentional diagnostic exclusions/scope/history cases.

## Still outstanding

- Shared normalized runtime live verification on Binance Spot and Binance US.
- Positive SMS OffTrigger deactivation case.
- Startup duration optimization, particularly legacy full-history reconstruction and Binance rate-limit pauses.
- Four insufficient 8h indicator warnings are by design with 96h of retained data.
