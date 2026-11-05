# PTMagic 2.10 — PriceTrend compatibility live Binance Futures evidence

Date: 2026-11-05 KST
Sources: user-provided 2026-11-05.txt, MarketTrendAnalytics(7).json, LastRuntimeSummary(7).json, SingleMarketSettingSummary(7).json
Version: 2.10.0 in log. Git SHA not embedded; prior user build/test targeted app commit d0b0b877d6157b0db44cc4d1d2ac4b0cb0799abc.

## Environment and run

- Initial configuration attempts at 11:56 failed from unsupported Bittrex, empty server token, unreachable PT monitor. A later 12:03 attempt failed from missing PAIRS.properties. These attempts did not reach market evaluation and were corrected before the next start.
- Successful TestMode began 12:05:37 and completed nine RAID SUMMARY entries at 12:20:06, 12:20:55, 12:21:39, 12:22:39, 12:23:39, 12:24:39, 12:25:56, 12:26:39, 12:27:39 KST.
- First raid 14m28s overall; initial legacy history rebuilt for 756 markets over 96h from 12:05:55 to 12:17:54 (11m59s). First normalized refresh finished 12:20:04 with 756/756 series, 872,424 candles, 0 failures. Later 750/756 (2250 candles) and 756/756 (2268 candles) refreshes also reported zero failures.
- All requested return metrics had full valid coverage, 250/250 global markets and 519/519 asset markets (configured narrow/capped variants appropriately smaller). The initial normalized evaluation was pinned to refresh start. Seven warning groups remained steady across nine raids: intentionally excluded market, asset metric requested globally, explicitly disabled metric, and four insufficient-history cases.
- First raid GlobalSetting changed to DIAG_Global_AllP1C_AndPriceCompatibility; subsequent raids retained it without reapplication. TESTMODE prevented all ProfitTrailer configuration writes.

## Independent numerical validation at final 03:27:38 UTC snapshot

- Matched 5,192 asset PriceTrend values exported in MarketTrendAnalytics and LastRuntimeSummary.MarketSummary.MarketTrendChanges: **0 mismatches**.
- CAP_1h global population 10; LARGE_1h global 250; both independently preserve the asset population of 519.
- Final CAP_1h global PriceTrend arithmetic mean -0.0219008789444%; LARGE_1h global PriceTrend +0.6930364928286%, consistent with independently averaging respective exported valid global asset values.
- THRESHOLD_1h PriceTrend mean +0.4637067707251% vs LARGE_1h unfiltered +0.6930364928286%; independent filtering of the 250 global asset returns by absolute return <=5% reproduces +0.4637067707251%; 4 global assets excluded **from the mean**, not the population.
- Breadth 77.6%, MedianPriceTrend +0.47477688%, Dispersion 2.51580977, MeanMedianSpread +0.21825961% match exactly between LARGE_1h and THRESHOLD_1h. Confirms threshold isolation in a nontrivial market.
- FIAT_1h Market and LARGE_1h PriceTrend both +0.6930364928286% and individual asset PriceTrend matches for USDT quotes. This proves the USDT identity branch, NOT cross-quote fiat conversion.
- ETHUSDT activation snapshots: DIAG_SMS_ETH_Relative_Cap10 and DIAG_SMS_ETH_Relative_Cap250 each -0.4819078267948397%, while DIAG_SMS_ETH_Relative_Threshold5 -0.38482339078263805%; DIAG_SMS_ETH_Absolute_Cap10 +0.025921125717465188%. These show Relative invariance to MaxMarkets and independent TrendThreshold adjustment.

## OffTrigger evidence and caveat

One positive live exit signal: at 12:20:55.280 KST `DIAG_SMS_BTC_ActivationPriceExit` logged `off triggered!`; it was immediately followed by `triggered!` and summary saved during the same raid because activation conditions remained true. The final summary still lists it active, with activation timestamp 03:20:55 UTC. This demonstrates the true OffTrigger code path and reactivation, **not sustained deactivation**. DIAG_SMS_ETH_Relative_CrossExit did not exit in this recording.

## Remaining acceptance work

- Verify genuine non-USDT Fiat using a Binance Spot / Binance US quote such as ETHBTC and the aligned BTCUSDT conversion; missing reference should fail closed. Binance Futures test uses USDT quote and cannot demonstrate that conversion.
- Test a config that actually fails the TrendMinutes multiple-of-five validation before market-data recreation; deterministic tests already cover it.
- Test an OffTrigger true branch when activation is false, so a persistent inactive state can be observed.
- Binance Spot and Binance US runtime parity; legacy-vs-normalized calculation parity (historic data with matching endpoints).
- Separate performance: reduce legacy historical reconstruction at startup and excessive DEBUG logging (~196,738 lines / 19 MB in recorded file).

## Assessment

USDT-quoted Binance Futures PriceTrend migration and the four compatibility behavior changes pass live evidence where exercised. Source-level and deterministic tests passed 88/88 before this run. **Do not claim full cross-exchange Fiat or persistent OffTrigger acceptance from these files.**
