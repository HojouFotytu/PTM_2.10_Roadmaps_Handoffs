# PTMagic 2.10 — D-053 post-removal build and configured TestMode evidence

**Date:** November 12, 2026 (KST). **Status:** D-053 source, focused offline, and configured TestMode verification **PASS**. Live PT setting delivery, startup SOM enforcement in non-TestMode, and Monitor browser acceptance **not verified**.

**Verified running application source:** [`e31635a1e67347918ca1bbf94d0fb64809b1cea0`](https://github.com/HojouFotytu/PTMagic/commit/e31635a1e67347918ca1bbf94d0fb64809b1cea0). Later commits updating `Tests/Settings` documentation are not runtime changes. Application software and independent user-specific LONG/SHORT strategy/settings development remain strictly separate.

## User-executed local build and focused checks

- `git pull --ff-only` — already up to date; `git rev-parse HEAD` printed exact source `e31635a1e67347918ca1bbf94d0fb64809b1cea0`.
- `dotnet build .\PTMagic.sln` — **PASS**, Core/PTMagic/Monitor net10.0, 12.9 seconds.
- `dotnet run --project .\Tests\Phase2Funding` — **28/28 offline groups PASS**.
- `dotnet run --project .\Tests\Phase2AdaptiveAcquisition` — **8/8 focused groups PASS**: 24-metric registry (17 global-capable, seven asset-only), funding five-minute quota, shared IP weight, 429/418 cooldowns, recoverable quota wait, cancellation, freshness/capacity deadline, and no fixed 60-page funding ceiling.
- **36/36 focused groups PASS**. The separate **15-project** full regression runner was **not** executed; do not claim its results.

## Configured runtime and supplied data-archive inspection

The user supplied the November 12 text runtime log and associated `_data` ZIP. The initial 21:23 and 21:24 launches used an older analyzer configuration: three expected warnings for retired `OpenInterestChange`, `OpenInterestValueChange`, and `GlobalLongShortAccountRatio`. After the corrected D-053 24-metric analyzer was loaded at approximately 21:28 KST, those warnings disappeared.

Four completed TestMode raids are recorded at **21:42:19, 21:43:48, 21:49:00 and 21:54:00 KST**:

| Evidence | Observed outcome |
|---|---|
| Running source | `e31635a1` logged on each raid |
| Selected exchange population | 519 eligible COIN USDT markets, other underlying types excluded |
| Selected setting | `DEFAULT`, 519 markets in both `TEST_SMS_01_BASELINE` and `TEST_SMS_02_FUNDING` |
| Completed-raid metric warnings | **None** |
| Funding history | **519/519** selected markets with provider-verified exact 1440-minute window in all four raids |
| Funding request counts | First raid: six bulk pages; later raids: one bulk page each; **zero** symbol-specific pages and **zero** failed funding requests |
| First raid duration | 13m 34s, during extensive 72-hour initial normalized history acquisition |
| Later raid durations | 3s, 15s, 15s |
| Binance rate-limit warnings | 24 pause messages during initial backfill; request throttling, not evidence of 429/418 errors |
| Decision-history records | Four source-stamped snapshots, each `DecisionFresh=true`, `SelectionIndeterminate=false` |
| Trigger metric inputs | Each snapshot: **4,169/4,169 available**, including 17 global triggers and 4,152 SMS-trigger evaluations; no invalid reasons |
| Persisted funding cache | 519 files in `_data/DerivativesFundingCache/BINANCEFUTURES` |
| Persisted normalized OHLCV cache | 519 files in `_data/NormalizedOhlcvCache/BINANCEFUTURES` |
| Retired cache families | No active OI/positioning cache families found in supplied archive |
| PT setting delivery | No changes made: **TestMode preview**; confirmed PT setting unknown |
| Startup SOM | **Inactive (TestMode preview)**; no real PT SOM API action demonstrated |

The archive contains four decision-history records in `_data/DecisionHistory/2026-11-12-000001.jsonl`, consistent with the four completed raid summaries.

## Acceptance, limitations, and forward work

**Acceptance:** D-053 removal is verified at source-review, compilation, directly affected offline checks, and configured TestMode analytics/funding levels. No new defect is established in this evidence. The first-raid backfill is a potential startup-performance consideration, not a removal failure. Preserve application-wide performance work for the scheduled later phase unless a concrete operational failure appears.

**Not established:** full 15-harness execution at this SHA; live, non-TestMode PT configuration delivery; actual SOM switch behavior; Monitor browser acceptance; or other-exchange integration.

**Next:** Phase 2 taker-flow source assessment, then implementation of `TakerBuyRatio` and `TakerImbalance`, using existing normalized Binance kline input if the source/retention semantics support it. Do not reintroduce OI or positioning, modify the trading strategy/settings repositories, or add unrequested repository directories.

[Removal code audit](2026-11-12-d053-removal-code-audit.md) · [Current status](../STATUS.md) · [Technical roadmap](../roadmaps/CURRENT.md)
