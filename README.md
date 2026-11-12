# PTMagic 2.10 — Market Analysis Expansion

**November 13, 2026 — Phase 2 Taker Flow focused verification PASS:** User-supplied execution at exact PTMagic source [`f7d802facfabb4611098d695d88a269d60daa278`](https://github.com/HojouFotytu/PTMagic/commit/f7d802facfabb4611098d695d88a269d60daa278) confirmed `dotnet build .\PTMagic.sln` **PASS (16.1s; Core, PTMagic, Monitor net10.0)** and all **33/33 focused offline groups PASS**: Phase1COhlcv **15/15**, NormalizedWarmStartCache **10/10**, Phase2AdaptiveAcquisition **8/8**, including the 26-metric registry (17 global-capable, nine asset-only). **Next:** configured Binance Futures TestMode raid using the updated 26-metric analyzer, verifying source taker-buy quote volume, both computed metrics, cache upgrade, and repeat-raid behavior. **Not yet established:** configured taker-flow runtime acceptance, actual PT delivery, or browser acceptance. Prior statements that the taker revision's build or focused tests are pending are superseded; earlier historical test reports remain source-specific. [Implementation record](updates/2026-11-12-phase2-taker-flow-implementation.md).

**Phase 2 Taker Flow implementation — November 12:** application source [`f7d802facfabb4611098d695d88a269d60daa278`](https://github.com/HojouFotytu/PTMagic/commit/f7d802facfabb4611098d695d88a269d60daa278) now contains **26 registered metrics** (17 globally evaluable, nine asset-only), including `TakerBuyRatio` and `TakerImbalance`. The existing kline reader retains index-10 taker-buy **quote** volume, an opt-in exact-period feature engine calculates both metrics, legacy OHLCV cache **v1** remains readable, and cache **v2** persists source-verified taker fields with targeted repair of old cache windows. The existing diagnostic TestMode analyzer was extended in place; Monitor labels/colors and focused tests were updated. **Published and source-inspected; .NET build, new focused test execution and configured taker-flow raid are PENDING.** The earlier D-053 PASS cannot be reattributed to this feature. [Implementation and verification handoff](updates/2026-11-12-phase2-taker-flow-implementation.md).

**Phase 2 Taker Flow — source assessment started November 12:** [Source/persistence review](updates/2026-11-12-phase2-taker-flow-source-review.md) confirms Binance kline index 10 is currently discarded by `BinanceKlineClient`; `MarketCandle` and version-1 normalized warm-start cache contain no taker-buy quote volume. Proposed new asset-only metrics `TakerBuyRatio=B/Q` and `TakerImbalance=2B/Q−1` will reuse the existing pinned 5m kline pipeline, sum exact complete TrendMinutes periods and keep missing data UNAVAILABLE. **Implementation is not yet published**; preserving existing OHLCV cache warm-start behavior while safely refreshing missing taker fields is the principal design requirement. D-053 is closed at configured TestMode level; Phase 2 Taker Flow is the active development track.

**2026-11-12 D-053 configured verification — PASS:** user-run `.NET 10` solution build **PASS (12.9s)** at application source `e31635a1e67347918ca1bbf94d0fb64809b1cea0`; **Phase2Funding 28/28** and **Phase2AdaptiveAcquisition 8/8** (**36/36 focused offline checks**). The user-supplied log and `_data` archive show **four completed TestMode raids**, 519 COIN markets, **519/519 funding history coverage**, **4,169/4,169 available trigger inputs** per decision, **zero completed-raid metric warnings**, successful bulk-only funding acquisition (6/1/1/1 pages; no failures) and fresh determinate decisions. Obsolete OI/ratio warnings preceded the corrected analyzer reload. **D-053 source, focused checks and configured TestMode acceptance are complete**; non-TestMode PT delivery, startup SOM enforcement and Monitor browser acceptance remain unverified. **Next development: Phase 2 taker-flow assessment and implementation; do not repeat retired OI/ratio validation.** [Full D-053 configured evidence](updates/2026-11-12-d053-configured-testmode-validation.md).

**D-053 implementation and removal-audit checkpoint — November 12, 2026:** PTMagic source [`892a5f1f4729a3fccd3cb477ba6ad22fbbe0918d`](https://github.com/HojouFotytu/PTMagic/commit/892a5f1f4729a3fccd3cb477ba6ad22fbbe0918d) contains the completed removal of `OpenInterestChange`, `OpenInterestValueChange` and `GlobalLongShortAccountRatio`, including their acquisition/services/active caches/registry/Monitor integrations. The source audit compared the **22-metric pre-introduction baseline** [`66629347`](https://github.com/HojouFotytu/PTMagic/commit/66629347f0dc9c7b68ea9f1c3f5bf536f3d7c427), **27-metric pre-removal** `d101b5a0` and current **24-metric** code: all 22 original metric identities and scopes survive; `FundingRate` and `FundingSum` also survive. A real shared Unicode symbol-validator dependency was temporarily broken by deleting OI, then repaired by [`02820822`](https://github.com/HojouFotytu/PTMagic/commit/02820822b9bb) and [`d7847c46`](https://github.com/HojouFotytu/PTMagic/commit/d7847c46190b). No further major/critical removal-related defect was established by source inspection; **current-revision local build, 15-harness test execution and configured runtime acceptance remain unverified**. The earlier 18-harness PASS at `d101b5a0` is strictly **pre-removal evidence**. [Full read-only audit](updates/2026-11-12-d053-removal-code-audit.md) (links relative to repository root). **This checkpoint supersedes all contradictory claims below that removal is pending, that retired OI/positioning is active, or that its tests/feature work remain required. Dated implementation evidence is retained as history.** No rollback and no strategy-settings work.


**Current documentation checkpoint: November 12, 2026. D-053 is the active metric scope; older dated text below is historical.**

PTMagic 2.10 expands deterministic market analysis and the configuration-management layer around ProfitTrailer. Its scope includes normalized market data, price and volume measurements, correlation, future derivatives and liquidity measurements, GlobalSetting/SMS integration, and native inspection and validation. It has no external AI layer.

| Item | Current authority |
|---|---|
| Application | [HojouFotytu/PTMagic](https://github.com/HojouFotytu/PTMagic) |
| Application branch | `phase1/market-data-foundation` |
| Current application branch head | `f7d802facfabb4611098d695d88a269d60daa278` (Phase 2 taker-flow source published; build/runtime not yet verified) |
| Last tested application source | `f7d802facfabb4611098d695d88a269d60daa278` (net10.0 solution build PASS 16.1s; 33/33 taker-flow focused groups PASS; TestMode runtime pending) |
| Framework / application version | .NET 10 / 2.10.0 |
| Current technical plan | [roadmaps/CURRENT.md](roadmaps/CURRENT.md) |
| Current implementation and acceptance status | [STATUS.md](STATUS.md) |
| Cumulative effective 2.10 changes for PRs and merges | [CHANGELOG-2.10.md](CHANGELOG-2.10.md) |
| Current decisions and supersession register | [DECISIONS.md](DECISIONS.md) |
| Current handoff | [November 11 SOM safety, Phase 2 derivatives and persistence](handoffs/2026-11-10-som-enable-only.md) |
| Concise user roadmap | [ROADMAP.md](ROADMAP.md) |

## Current scope — D-053 (November 12)

The PTMagic 2.10 owner has withdrawn OI and long/short positioning rather than scaling the shared historical-data quota. The three currently implemented metrics `OpenInterestChange`, `OpenInterestValueChange`, and `GlobalLongShortAccountRatio` and their source-specific network/cache/registry/Monitor features are to be removed. The approved **post-removal 24-metric** catalogue retains **17 globally usable** metrics and **7 asset-only** metrics, including `FundingRate` and `FundingSum`. Remaining roadmap: taker-buy ratio/imbalance, funding and taker-flow market aggregates, transparent price/volume/flow analysis, liquidity/depth/stress, audit history and final performance work.

**Implementation not yet done.** Current app source is `d101b5a03e01f8f76acf8cc9a6bde7214ff34aa2`, user-local .NET 10.0.403 build PASS (14.8 seconds) and **18/18 offline harnesses PASS** with 80 ConfigurationLifecycle tests. Those tests verified the former 27-metric code, not the proposed removal. [D-053](DECISIONS.md#d-053--remove-binance-futures-open-interest-and-longshort-positioning-metrics-from-ptmagic-210) supersedes conflicting historical decisions; [current roadmap](roadmaps/CURRENT.md) is authoritative. Source cleanup and focused validation are next. Preserve strategy-settings separation.

## Present checkpoint

The latest user-executed application validation is source `875b4feb71104fbc609bd07dc3120405218d325f`: .NET SDK 10.0.403 solution build PASS in 17.4 seconds and **all 17 offline harnesses PASS**. Eight nonfatal nullable warnings were reported in two existing test projects. The current branch head is `66f88f73f46d5c7863ff27e55c00b98d6917cf83`; its two commits after the tested source only modify `RANDOM_THOUGHTS_AND_REMINDERS.md`, not application/runtime code.

**Phase 2:** Open Interest, settled funding and the three separate global-account, top-trader-account and top-trader-position long/short ratio metrics are implemented. Funding and ratio disk caches are integrated. The latest run passed 18 funding groups, 18 raw OI groups, 17 incremental OI groups and 29 ratio groups.

**Immediate next task:** add service-level restart tests proving newly constructed funding and ratio services restore persisted coverage and avoid duplicate provider requests. Then perform configured two-startup acceptance to verify request reduction and unchanged metrics. Live Binance/API-key and Monitor browser acceptance remain pending. Taker flow follows after persistence acceptance.

**Open Monitor item:** Possible Buys and Positions are not refreshing reliably. Preserve the original jQuery `.load()` request and limit any correction to scheduling in `Monitor/Pages/Index.cshtml`. Do not change PBL/Positions data retrieval, DashboardTop rendering, DashboardBottom, ticker refresh, tooltips or autocoloring. The zero-limit PBL experiment remains withdrawn.

## November 9 normalized OHLCV warm-start addition

PTMagic now has a disk-backed normalized five-minute candle cache under `_data/NormalizedOhlcvCache`. It restores validated closed bars before fetching missing history and is isolated by exchange/symbol. The expected benefit is avoiding a full normalized OHLCV redownload after a short restart. This targeted optimization was authorized under [D-040](DECISIONS.md#d-040--targeted-persistent-ohlcv-warm-start-now).

**Native verification passed:** eight new cache test groups passed at `925db7c`, alongside 16 analytics-reliability and 13 Phase 1C OHLCV checks (37/37); .NET SDK 10.0.403 solution build passed in 18.3 seconds. The 272 previously passing checks remain evidence for their earlier source revisions, not for `925db7c`. Legacy tick rebuilding is separate. [Current handoff](handoffs/2026-11-07-stabilization-correlation-validation.md).

## TestMode console visibility

The November 9 NLog presentation update colors all `TestMode`-identified console messages purple/magenta, matching the startup warning. Three application/Monitor/default logging configuration files are updated; severity and file-log content are unchanged. The user-local .NET 10 build passed in **15.1 seconds** and all **three NLog XML/rule checks passed** on November 9. **Visible Windows console color rendering remains unverified**. The test output did not print an exact `git rev-parse HEAD`. A deployed existing `nlog.config` must be updated for the change to appear.

## Scope boundary

This repository governs the PTMagic 2.10 application and its public capabilities. Personal trading strategies, strategy presets, long/short strategy roadmaps, and their trading results are independent projects. They are neither deliverables nor release gates for PTMagic 2.10.

The completed 2.9 modernization is historical context. Its performance results must not be presented as measurements of the expanded 2.10 pipeline.

## Read order and precedence

1. Read this README, [STATUS](STATUS.md), and the single current handoff.
2. Use [DECISIONS](DECISIONS.md) for accepted behavior and explicit supersession.
3. Use [the current technical roadmap](roadmaps/CURRENT.md) for the complete current and future scope.
4. Inspect the actual application branch before editing. Source determines what exists; execution evidence determines what has been verified. Neither silently changes the accepted contract.
5. Use earlier dated files for provenance. They are historical snapshots, even where their text originally called them “current.”

Current user instructions take precedence over earlier project decisions. Record such changes explicitly rather than leaving incompatible active instructions.

## Validation ownership

D-021, D-022, and D-038 remain active:

- The assistant implements source changes, reviews code, authors regression cases, and fixes reported failures.
- The user runs local .NET builds, regression harnesses, and configured PTMagic/ProfitTrailer runtime checks.
- The user has granted standing authorization to publish PTM 2.10 development changes to the application and documentation branches named in [D-038](DECISIONS.md#d-038--standing-authorization-to-publish-ptm-210-development). Do not request renewed conversational approval for those publications; actual tool restrictions still apply.
- A source commit, a written test, or a source review is not a passing execution result.
- GitHub is used for source control and documentation. Automatic GitHub Actions or remote build/test execution requires an explicit user request. The earlier automatic regression workflow was removed; do not restore it by following a historical handoff.
- Every source-change handoff supplies a complete, fail-fast PowerShell sequence with the exact current project paths and specific runtime checks.

The current commands and acceptance matrix are in the [active November 10 handoff](handoffs/2026-11-10-som-enable-only.md). Run them from the **PTMagic application repository**, not this documentation repository.

## Sequencing

Implement D-053 source removal of OI and long/short positioning first, then continue with validated funding and taker flow. The specifically deferred Phase 1 configured integration checks and live PT/Monitor acceptance remain open. The dedicated performance program is **deferred until all approved new metrics have been completed**, including derivatives and liquidity. This supersedes earlier recommendations to perform startup, snapshot-cache, logging, or incremental-calculation optimization before correlation.

Correctness work, bounded retention, and dependency validation continue as part of feature delivery. Do not use that exception to reintroduce a separate performance project ahead of the agreed gate.

## Release-change record for PRs and merges

[CHANGELOG-2.10.md](CHANGELOG-2.10.md) records only the resulting 2.10 changes that remain in effect, from the November 2 foundation through the current implementation. It is mirrored in the application repository so the file travels with code merges. Update both copies in the same development handoff, consolidate or remove superseded entries, and reference the relevant sections in PR, merge and release descriptions. Keep future work in the roadmap and preserve exact execution provenance. [D-039](DECISIONS.md#d-039--cumulative-effective-change-record-for-prs-and-merges) defines maintenance.

## Historical records

- [Historical roadmap index](roadmaps/README.md)
- [Historical handoff index](handoffs/README.md)
- [Dated implementation and evidence updates](updates/README.md)
- [Pre-reconciliation document snapshots](history/README.md)
- [Phase 0 architecture audit](audits/phase-0-architecture-audit.txt)
- [Change log](CHANGELOG.md)

The November 7 reconciliation preserves the original dated roadmap, handoff, issue, and update files. Earlier mutable current documents were captured under `history/2026-11-07-pre-reconciliation/` before being replaced.


## Latest Phase 2 validation — November 11

The current tested PTMagic source is `1a1f1804237288433ed046b30fb7d9b780a32066`. Both top-trader ratio feeds and their API-key path have been removed. Only public `GlobalLongShortAccountRatio` remains. Solution build PASS (18.2s); 17/17 offline harnesses and 377 checks PASS. Adaptive per-raid acquisition redesign remains the next implementation task. [Validation details](updates/2026-11-11-top-trader-ratio-removal-validation.md).
