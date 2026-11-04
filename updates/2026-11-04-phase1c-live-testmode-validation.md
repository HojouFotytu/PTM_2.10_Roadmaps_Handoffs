# 2026-11-04 — Phase 1C live TestMode results

**Application:** `HojouFotytu/PTMagic`, branch `phase1/market-data-foundation`; source at `64d063c`.

User-provided second deployed TestMode session (18:18–18:32 KST) verifies the previous outdated-binary problem is resolved. No errors, fatal entries, or unknown metric names. 756/756 normalized Binance Futures market series refreshed, 872,424 5-minute candles received and zero failed, 519 COIN-eligible analyzer markets. The 1h, 2h and 4h Phase 1C global metrics were reported valid at 100% population coverage and exported with per-asset features.

**Timeframe correctness:** At 09:32Z, metric source close = 08:59:59.999Z for 1h, 07:59:59.999Z for 2h and 4h. These are fully closed trend periods, not the more recent normalized 5m source endpoint.

**Insufficient history:** `StoreDataMaxHours=96`; 8h ATR(14) needs >=120h, VolumeExpansion(20) needs >=168h, plus UTC alignment margin. Therefore 8h MedianATRP and MedianVolumeExpansion correctly invalid at 0/248; all other independent 8h metrics remain valid. The RAID SUMMARY shows both warning entries in full.

**Trigger behavior:** `DIAG_Global_P1C_All15Global` matched all 15 conditions on 2h and switched on first raid; second raid recognized it as active without reapplying. Eight diagnostic Single Market Settings across BTC, ETH and SOL activated, including the True OR Unavailable case; the invalid OffTrigger did not appear to deactivate the ETH setting. `TESTMODE` prevented any PT configuration updates. Full first raid (with 96h history recreation and Binance throttling) lasted 13m29s; next raid lasted ~1s.

**Confirmed independent export defect — P1C-SMS-SNAPSHOT-ALIAS:** `SingleMarketSettingSummary.json` includes other settings' trigger messages in the first SMS for each market: BTC first SMS 9 descriptions for 3 own triggers, ETH 5 for 4, SOL 4 for 3. `Core/Main/PTMagic.cs` shares a mutable `matchedSingleMarketTriggers` list between `matchedMarketTriggers.Add(marketPair, matchedSingleMarketTriggers)` and `smss.TriggerSnapshot.MatchedTriggersContent`; later `AddRange` calls mutate the original saved snapshot. The separate per-setting `RelevantTriggers` values are correct; this is an explanation/export issue rather than evidence of incorrect trigger truth. Correct by copying the list at first aggregation, with a regression test.

**Remaining acceptance:** Monitor *visual* rendering was not provided, and the SMS summary export defect remains unresolved. Source + deterministic tests (53/53) + live Phase1C metric/trigger evaluation are verified, but **do not mark Phase1C fully DONE or Phase1D active until these are dispositioned**. No application code changed in this documentation-only update.
