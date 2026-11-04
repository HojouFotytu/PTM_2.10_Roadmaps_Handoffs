# PTMagic 2.10 — Option C warning live TestMode validation

Date: 2026-11-05 (KST)
Application source: HojouFotytu/PTMagic, phase1/market-data-foundation
Validated user-local version: 2.10.0; working source HEAD before run: 9f88315e018db940d9816fdc991e8c444a47d02f
Input: Pasted text(20261104-151249).txt (631-line local Binance Futures log)

## Acceptance results

- Core, PTMagic and Monitor .NET 10 build previously passed; full local regression suite passed **81/81** on the same source branch.
- **Option C natural-language warning format: PASS** on Binance Futures. All seven second-raid groups are brief human-readable explanations with cause and actionable checks. Example: SMS \`DIAG_SMS_SOL_FilteredOut\` activation for \`SOLUSDT\` is blocked because \`FILTERED_1h\` explicitly excludes SOL via \`IgnoredMarkets\`, with instructions on how to allow it.
- Scope misuse is correctly identified: GlobalSetting \`DIAG_Global_RejectAssetScope\` cannot use asset-only \`ATRP\` from \`FULL_2h\`; recommendation \`MedianATRP\` is provided.
- Explicit metric not enabled: SMS \`DIAG_SMS_BTC_ExplicitDisabledPriceTrend\` requests \`PriceTrend\` from \`IMPLICIT_1h\`; explanation covers adding it or omitting the trigger's Metric to use implicit PriceTrend.
- History insufficiency is plainly explained: ATRP 11/15 and VolumeExpansion 11/21 eight-hour periods, and aggregate MedianATRP / MedianVolumeExpansion 0/250 valid vs 225 required.
- No repeated raw resolver dumps; multiple relevant SMS callers remain included as grouped examples. Some wording repeats the market symbol twice (e.g. 'for SOLUSDT ... SOLUSDT PriceTrend') — cosmetic only, non-blocking.

## Two-raid details

| | First cold raid | Second refreshed raid |
|---|---|---|
| Local time | 00:09:42–00:11:13 | 00:11:42–00:11:50 |
| Duration | 1m30s | 8s |
| Five-minute candle refresh | 756/756, 872,424 candles | 287/756, 861 candles; 469 skipped |
| Failed exchange fetches | 0 | 0 |
| Valid global returns | 179/250 (71.6%) | 250/250 (100%) |
| Valid asset returns | 365/519 | 519/519 |
| Warning groups | 31 | 7 |
| PT writes | None; TestMode active | None; TestMode active |

The second raid saw the expected 18 matched diagnostic triggers for \`DIAG_Global_All15AndImplicit\`, but flood protection prevented switching from Default until 15:13:12 UTC. No configuration was reapplied on the second raid. The first raid logged GlobalSetting selection indeterminate because required metric values were missing.

## Unresolved candle-boundary issue

- Refresh started at ~15:09:43 UTC and ended at ~15:11:11 UTC, crossing the expected five-minute candle close at **15:09:59.999 UTC**.
- The post-refresh evaluator demanded that endpoint across all series. Many were ingested before the endpoint was available, causing \`MissingEndpoint\` and temporary failure to meet market coverage limits.
- Repeated across several cold starts and cleared by subsequent refreshes. Fix by pinning refresh/evaluation as-of to a common closed-candle endpoint or reconciling any boundary-crossing series before evaluation. Requires separate implementation and deterministic cross-boundary test; not resolved by Option C work.

## Outstanding

- Binance Spot and Binance US TestMode parity.
- Positive threshold-crossing OffTrigger deactivation end-to-end.
- \`TrendCurrency: Fiat\` end-to-end parity (if still in final acceptance scope).
- Cold-start boundary consistency.
- No new source changes in this documentation-only verification.
