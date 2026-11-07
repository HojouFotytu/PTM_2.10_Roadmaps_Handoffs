# PTMagic 2.10 — Market Analysis Expansion

**Current documentation checkpoint: November 7, 2026.**

PTMagic 2.10 expands deterministic market analysis and the configuration-management layer around ProfitTrailer. Its scope includes normalized market data, price and volume measurements, correlation, future derivatives and liquidity measurements, GlobalSetting/SMS integration, and native inspection and validation. It has no external AI layer.

| Item | Current authority |
|---|---|
| Application | [HojouFotytu/PTMagic](https://github.com/HojouFotytu/PTMagic) |
| Application branch | `phase1/market-data-foundation` |
| Published source checkpoint for this handoff | `a0b375cc9b2db469a48a31b713385f35500cc763` |
| Framework / application version | .NET 10 / 2.10.0 |
| Current technical plan | [roadmaps/CURRENT.md](roadmaps/CURRENT.md) |
| Current implementation and acceptance status | [STATUS.md](STATUS.md) |
| Cumulative effective 2.10 changes for PRs and merges | [CHANGELOG-2.10.md](CHANGELOG-2.10.md) |
| Current decisions and supersession register | [DECISIONS.md](DECISIONS.md) |
| Current handoff | [November 7 stabilization and correlation validation](handoffs/2026-11-07-stabilization-correlation-validation.md) |
| Concise user roadmap | [ROADMAP.md](ROADMAP.md) |

## Present checkpoint

The November 7 work implements configuration lifecycle corrections, startup global sell-only protection through ProfitTrailer's control API, delivery acknowledgement and retry handling, Monitor trigger preservation, configuration reference validation, pinned request boundaries, decision-age checks, history requirements, the Concentration ranking-window correction, Phase 1D correlation, and bounded decision-history recording.

The user superseded the initial startup-preset overlay with `POST /api/v2/globalSellOnlyMode`, using query parameters `token` and `enabled`. Startup protection changes that API state without submitting PAIRS, DCA, or INDICATORS. The normal configuration is delivered only after analysis; guard release has its own API acknowledgement. See [D-037](DECISIONS.md#d-037--direct-global-som-api-supersedes-the-startup-preset-overlay).

**All 272 checks across twelve harnesses now have passing user-local results: 193 checks in ten harnesses at `86c2ea3`, followed by 66 ConfigurationLifecycle and 13 DecisionHistory checks at `d331fbd`.** The latest continuation used .NET SDK 10.0.403 and built Core, PTMagic, and Monitor in 10.9 seconds. These are two recorded runs, not a single twelve-harness run at one revision. See [current evidence](updates/2026-11-07-completed-harness-validation.md).

The two Telegram fixture corrections are verified by native execution. Production code and assertions were unchanged between the tested revisions. The current `a0b375c` publication adds [the cumulative effective-change record](CHANGELOG-2.10.md), makes startup SOM explicit in both supplied general-settings templates, and clarifies the existing Monitor Application toggle with visible TestMode help. Engine code and test cases are unchanged. No new build or browser result is claimed, and this update alone requires no harness rerun. An explicit compiled-DLL launch reached a missing-preset validation error, and the user later reported a long initial run underway. Collect that result and source identity before requesting a repeat. TestMode simulates SOM, so actual PT acknowledgement and browser integration remain separate acceptance work. [Publication status](STATUS.md#publication-status).

The earlier pre-change `d0b0b87` baseline remains historical evidence: a user-run application build, 88 checks across six harnesses, and nine Binance Futures USDT TestMode raids. The deployed SHA was inferred from the workflow because those logs printed version 2.10.0 rather than a Git SHA. [Evidence](updates/2026-11-05-price-compatibility-nine-raid-testmode.md).

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

The current commands and acceptance matrix are in the [November 7 handoff](handoffs/2026-11-07-stabilization-correlation-validation.md). Run them from the **PTMagic application repository**, not this documentation repository.

## Sequencing

Local deterministic acceptance of the November 7 changes is complete. Finish the configured runtime, PT integration, and browser checks, then continue the remaining metric families. The dedicated performance program is **deferred until all approved new metrics have been completed**, including derivatives and liquidity. This supersedes earlier recommendations to perform startup, snapshot-cache, logging, or incremental-calculation optimization before correlation.

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
