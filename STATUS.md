# PTMagic 2.10 — Current Development Status

**As of:** 2026-11-04 — Phase 1A DONE (containment); Phase 1C NEXT; user-accepted MarketTrend timeframe rule D-016.
**Source:** [HojouFotytu/PTMagic](https://github.com/HojouFotytu/PTMagic), `phase1/market-data-foundation`.
**Last code HEAD verified for this update:** `89324bc5c8c5ea19ceb543b6ab5130899f2675dc` (merge commit; recheck before development).

| ID | Deliverable | Status | Evidence / next step |
|---|---|---|---|
| P0-AUDIT | Architecture audit | DONE | [Audit](audits/phase-0-architecture-audit.txt) |
| P1A-STORE | Shared normalized 5m OHLCV, incremental ingestion and Phase 0 universe | DONE | Cold-start, cleanup and idle raids verified |
| P1A-READY | Cold-start coverage, fail-closed normalized metrics and settings safeguard | **DONE — CONTAINED** | [Issue 001](issues/001-cold-start-readiness.md) closed; root cause not proven |
| P1B-RET | PriceTrend / MedianPriceTrend / MeanMedianSpread | DONE | Runtime exercised |
| P1B-BREADTH | Breadth / Dispersion | DONE | Coverage gated |
| P1B-RS | RelativeStrengthMarket / RelativeStrengthBTC | DONE | Scope preserved |
| P1B-CONC | Top10 return advantage Concentration | DONE | Current ranking uses fixed trailing 24h quote volume; 100% required |
| P1B-CONC-WINDOW | Align existing concentration-ranking window with MarketTrend.TrendMinutes | FOLLOW-UP | Known current 24h fixed-window exception; separate compatible code change/test |
| P1C-01 | Per-asset ATRP on MarketTrend.TrendMinutes candles | **NEXT** | Aggregate closed normalized 5m inputs to complete trend-duration OHLC; ATR(14), seed, history, invalidity |
| P1C-02 | MedianATRP on the same configured MarketTrend timeframe | NEXT after P1C-01 | Exact Phase 0 global universe, shared trend endpoint, 90% coverage |
| P1C-03 | Volatility breadth | PLANNED | Explicit threshold and coverage |
| P1C-04 | Recent quote-volume expansion | PLANNED | Comparable closed windows and zero baseline |
| P1C-05 | Volume-expansion breadth | PLANNED | Ratio thresholds and population |
| P1C-06 | Volume concentration | PLANNED | Volume share, distinct from existing return Concentration |
| P1C-07 | Registry/Monitor/trigger/test integration | PLANNED | Reuse existing infrastructure |
| P1D-CORR | Synchronized return correlation | PLANNED | TrendMinutes-based return cadence, not independent 5m/15m |
| P1E-INSPECT | Inspection and additional fault tests | PARTIAL | Carry non-blocking checks below |
| P2-RAW | Futures funding/OI/positioning/flow ingestion | PLANNED | Later |
| P2B-AGG | Futures market-wide aggregation | PLANNED | Later |
| P3-STATE | Deterministic higher-order states | PLANNED | Later |
| P4-TRIG | GlobalSetting / SMS / OffTrigger normalized metric routing | PARTIAL | First-generation routing works; extend per new metric |
| P5-LIQ | Liquidity/depth/stress | PLANNED | Later |
| P6-HIST | Feature history and validation | PLANNED | Later |

## Phase 1A closeout

**Code commits:** `3a2ba02` (90% global gate, 100% Concentration exception, coverage metadata and diagnostics); `c038a11` (unavailable normalized triggers fail closed, active GlobalSetting held on indeterminate fallback, SMS negation protection); `e002801` (four deterministic tests); `11d6e28` (raid summary distinguishes GlobalSetting switch from same-setting reapplication). All appear in the latest inspected branch.

**User-run tests:** `dotnet build` succeeded for Core/PTMagic/Monitor on .NET 10. `dotnet run --project Tests/Phase1AReadiness/Phase1AReadiness.csproj`: **4 tests passed**.

**User-supplied Binance Futures TestMode:** First raid fetched 756/756 normalized series (654,696 candles), but 4h global coverage was 32/250 (12.8%), with 218 MissingEndpoint; all dependent global features were unavailable and GlobalSetting triggers rejected. Second raid incrementally fetched 2,115 candles for 705 markets, recovered global coverage 249/249 and asset metrics 1,434/1,434. Third raid required **zero** normalized kline requests. After flood protection, `Default` switched to `DIAG_Global_AllMetrics` at 13:33 KST, with subsequent stable operation. Five-minute boundary raids downloaded ~2,268 incremental candles. TestMode sent no settings to PT.

**Policy:** Exact eligible GlobalSetting trend population is denominator; required valid count `ceil(0.9 * eligible)`, nonempty population. Existing `Concentration` requires 100% quote-volume-ranked population. Invalid, missing and stale metrics never substitute zero. Independent valid and legacy triggers may still operate; no forced cleanup raid, ingestion redesign or trading suspension.

**Root cause distinction:** A long cold-start fetch crossing 5m candle boundaries is plausible, **not proved**. The defect's *consequences* are contained and normal scheduled refresh repairs incompleteness. This is why P1A-READY is closed; it is not a claim that the first raid always has full data.

**Non-blocking follow-ups (P1E):** Verify retention of an already-active non-default GlobalSetting when coverage later falls below 90%; validate the revised raid summary wording in a new build/runtime; further partial-coverage, stale, sparse and boundary fault tests. The logs preceding the summary patch still say `Global setting changed`. Tested executable reported 2.9.1, whereas active product roadmap is 2.10.

## Accepted metric timeframe rule (D-016)

All derived metric analysis timeframes come from the configured `MarketTrend.TrendMinutes`. Normalized 5m is the source-data resolution only. P1C-01 `ATRP` and P1C-02 `MedianATRP` use complete, UTC-aligned trend-sized candles; 5m-fixed ATR/15m-fixed participation metrics are not valid Phase 1C designs. ATR(14) needs at least 15 complete trend candles; if `StoreDataMaxHours` is too short, metric is unavailable. This is an accepted **design requirement, not an implemented code change**. Existing return `Concentration` still uses fixed trailing 24h ranking and is recorded as a separate follow-up.

**Next:** [Corrected Phase 1C handoff](handoffs/2026-11-04-phase-1c-markettrend-timeframe-correction.md), starting with dynamic `ATRP` then `MedianATRP`.
