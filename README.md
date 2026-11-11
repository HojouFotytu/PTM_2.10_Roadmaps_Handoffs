# PTMagic 2.10 — Market Analysis Expansion

**Current documentation checkpoint: November 11, 2026.**

PTMagic 2.10 expands deterministic market analysis and the configuration-management layer around ProfitTrailer. Its scope includes normalized market data, price and volume measurements, correlation, future derivatives and liquidity measurements, GlobalSetting/SMS integration, and native inspection and validation. It has no external AI layer.

| Item | Current authority |
|---|---|
| Application | [HojouFotytu/PTMagic](https://github.com/HojouFotytu/PTMagic) |
| Application branch | `phase1/market-data-foundation` |
| Current application branch head | `27da292158687bc0bf1aa3b990d06f53237b42d9` |
| Last fully verified application source | `fb94373d8928b681e3ebe1f7209bd1439db42e72` (337/337) |
| Framework / application version | .NET 10 / 2.10.0 |
| Current technical plan | [roadmaps/CURRENT.md](roadmaps/CURRENT.md) |
| Current implementation and acceptance status | [STATUS.md](STATUS.md) |
| Cumulative effective 2.10 changes for PRs and merges | [CHANGELOG-2.10.md](CHANGELOG-2.10.md) |
| Current decisions and supersession register | [DECISIONS.md](DECISIONS.md) |
| Current handoff | [November 10 SOM safety and dashboard refresh investigation](handoffs/2026-11-10-som-enable-only.md) |
| Concise user roadmap | [ROADMAP.md](ROADMAP.md) |

## Present checkpoint

The latest full offline acceptance is **16/16 harnesses and 337/337 groups**, passed twice at exact application source `fb94373d8928b681e3ebe1f7209bd1439db42e72`. It includes SOM and Monitor lifecycle changes, but predates later Monitor edits and the full dashboard rollback at current branch head `27da292`. No post-rollback local build or live Monitor browser result is recorded.

**Phase 2:** OI metrics (`OpenInterestChange`, `OpenInterestValueChange`) and settled funding metrics (`FundingRate`, `FundingSum`) are implemented. Funding is the latest completed metric family. The next family is the three separate global-account, top-trader-account and top-trader-position long/short ratio feeds.

**Open Monitor item:** Possible Buys and Positions are not refreshing reliably. Preserve the original jQuery `.load()` request and limit any correction to scheduling in `Monitor/Pages/Index.cshtml`. Do not change PBL/Positions data retrieval, DashboardTop rendering, DashboardBottom, ticker refresh, tooltips or autocoloring. The zero-limit PBL card/count experiment remains withdrawn; the current original behavior hides the entire card when the PBL limit is zero.

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

Continue with the Phase 2 global-account and top-trader account/position ratio metrics. The specific remaining Phase 1 configured integration checks and live PT/Monitor acceptance remain open but do not block the approved Phase 2 development sequence. The dedicated performance program is **deferred until all approved new metrics have been completed**, including derivatives and liquidity. This supersedes earlier recommendations to perform startup, snapshot-cache, logging, or incremental-calculation optimization before correlation.

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
