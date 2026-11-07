# Issue 003 — Configuration lifecycle and analytical reliability

**Opened:** November 7, 2026

**Source reviewed before changes:** PTMagic `d0b0b877d6157b0db44cc4d1d2ac4b0cb0799abc`

**Implementation checkpoint:** `fac346c88b2c634439083e7515193d756ac3d186`

**Status:** Deterministic acceptance complete: 193 checks at `86c2ea3` plus 66 lifecycle and 13 history checks at `d331fbd`, totaling 272 across twelve harnesses. Configured runtime, actual PT API, and browser acceptance remain open.

This issue records the actionable findings from the November 7 review and their current disposition. It does not claim that every defect was introduced by 2.10. Several findings concern long-standing configuration lifecycle code that new metrics make more consequential.

## Latest execution evidence

The latest user-local build at exact source `d331fbd059041241069646c3bb82ac6549423a70` passed for Core, PTMagic, and Monitor with SDK 10.0.403 in 10.9 seconds. ConfigurationLifecycle passed all 66 checks and DecisionHistory passed all 13. Together with 193 passing checks in ten harnesses at `86c2ea3ff430b62e654f929a222935ec53ea8fa6`, the current 272-check inventory is complete. This combines two recorded runs; production code and assertions were unchanged between them. [Latest exact-source evidence](../updates/2026-11-07-completed-harness-validation.md).

A later runtime log repeats the bare `symbol=USDT` request and blank MainMarket after a first completed raid selects a non-default setting. The failing raid loads only 13/12/11 property lines. Both raids lack the current unconditional Source revision and Analysis main market logs and follow the older Core code path. This establishes execution of pre-fix Core behavior; the exact running SHA and loaded DLL path remain unknown. Its separate runtime working directory alone does not identify the assembly. The reported PT update and absent TestMode banner are not acceptance of the new startup API lifecycle. The next check explicitly launches the rebuilt DLL with that existing runtime directory and TestMode configuration, then verifies source identity. [Current evidence](../updates/2026-11-07-completed-harness-validation.md) preserves this distinction without publishing the raw private runtime log.

The earlier volume-cap fixture defect is resolved by the 40/40 validator result. Both qualified Telegram fixture references are now verified by native execution. Passing lifecycle cases establish exact main-market parsing/inheritance, invalid-input boundaries, fake-transport guard/configuration ordering, acknowledgement/retry behavior, freshness, SMS transitions, and TestMode isolation. Passing history cases establish bounded file behavior and production capture/checkpoint handling in their fixtures. Configured runtime still needs to show the intended market, a completed raid, actual PT acknowledgement and native SOM behavior, and browser integration. [Publication status](../STATUS.md#publication-status).

## Findings and acceptance

| ID | Observed failure path or inconsistency | Required correction | Closure evidence |
|---|---|---|---|
| CFG-01 / assessment 2A | A final SMS removal can leave zero active SMS entries without triggering a PT update, preserving a stale pair override | Treat nonempty-to-empty desired SMS state as a meaningful change and retain it until acknowledged | Production-component test across repeated raids, failed send then retry, configured runtime showing final override removed and remaining absent |
| CFG-02 / assessment 2B | Delivery errors can be logged/swallowed while internal state advances; the same desired setting is then treated as unchanged | Distinguish desired, pending, and confirmed state; expose failure; retry until acknowledgement | API/file transport failure tests, confirmed checkpoint unchanged on failure, retry of identical desired configuration, actual PT response |
| CFG-03 / assessment 2C | Monitor editing keys trigger rows too coarsely when several metrics or tags share one MarketTrend | Preserve the full supported identity and persisted values in load/edit/save | Production serialization round trip plus browser save/reload of activation and OffTrigger rows |
| CFG-04 / assessment 2D | Startup can replace the remembered setting with DEFAULT before a conclusive analysis; the first guard draft also reapplied a full preset before analysis | Default-on direct global SOM API guard without properties upload; normal configuration must be fresh, conclusive, and acknowledged before the separate release | Enable/configuration/release ordering, token/base-path handling, per-target failure and retry, restart and opt-out behavior, configured PT acknowledgement |
| CFG-05 / assessment 2E | Missing MarketTrend references can be converted to false or omitted from composed expressions | Validate references and preserve unavailable state defensively instead of deleting operands | Missing global/SMS/OffTrigger reference tests, negation and AND/OR behavior, actual configuration rejection |
| DATA-01 / assessment 3 | A raid pin can be used for evaluation while requests made later in the refresh select/retain a newer window, losing the earliest required reference under tight retention | Carry the pinned boundary into acquisition/request bounds and retained-window semantics | Regression crossing a source close with minimally sufficient capacity, then successful advancement next raid |
| DATA-02 / assessment 3 | A complete pinned snapshot can be too old when the configuration decision is finally made | Enforce MaxAnalysisAgeSeconds against the raid pin, independently of a metric's bar duration | Missing/future/expired pins, inclusive freshness boundary, slow bootstrap, valid completed multi-hour bar |
| DATA-03 / reported bootstrap failure | A runtime excerpt has a blank MainMarket; source review found null property groups discard inherited default assignments, and quote extraction can accept market-prefixed keys | Preserve inherited assignments, resolve and normalize the exact market property, reject invalid input before exchange I/O, and apply USDT price identity | Lifecycle regressions plus a configured run from the recorded new Source revision that resolves the intended market and completes a raid |
| METRIC-01 / assessment 5 | History settings do not explain actual ATR/volume/correlation and UTC-alignment requirements | Export per-metric current-raid and all-alignments requirements, capacity, and warnings | Exact period/slot expectations at multiple UTC alignments, dependency reporting, insufficient retention without fabricated values |
| METRIC-02 / assessment 5 | Return Concentration ranks by fixed 24-hour volume while the compared return uses TrendMinutes | Rank on the same trailing TrendMinutes endpoint/window; keep Top10-minus-remainder percentage-point meaning | Window-sensitive fixtures, minimum eleven markets, complete eligible ranking/returns and deterministic tie ordering |
| DOC-01 / assessment 6 | Current documentation exposes incompatible legacy contracts and several stale “latest” handoffs | One current roadmap/status/handoff, explicit supersession, preserved historical snapshots | Relative-link/static review and source-contract cross-check |
| TEST-01 / assessment 7 | Existing passing tests do not cover all delivery, repeated-raid, startup, editor, freshness, and runtime cases | Author meaningful production-component coverage and enumerate environment-dependent checks honestly | User build/harness results plus separately recorded runtime/browser/PT evidence |

The November 5 pinned-time regression remains accepted for its demonstrated case. DATA-01 extends that fix to request-window and retention consistency; it does not erase earlier evidence.

## Accepted startup policy

The user superseded the initial unpublished preset overlay with direct global SOM API control:

- Application.StartupSellOnlyMode defaults to true.
- Call POST /api/v2/globalSellOnlyMode with token and enabled=true before slow exchange bootstrap. No PAIRS, DCA, or INDICATORS are uploaded to acquire the guard.
- The user clarified that native global SOM stops new buys and DCA buys while allowing sells.
- Do not claim protection reached PT until the guard delivery succeeds.
- If guard delivery fails, abort that raid before the long bootstrap and retry at the next interval.
- Missing, stale, or otherwise indeterminate analysis keeps the guard.
- Deliver the normal configuration after a fresh conclusive full raid, then request enabled=false only after configuration acknowledgement. Release has its own acknowledgement and retry state.
- StartupSellOnlyMode=true assigns the flag to PTM for startup; there is no readback/restoration of an unknown prior global SOM value. A pre-existing true is still requested false after the release prerequisites.
- Disabling the option prevents a new guard but does not abandon matching pending PTM-owned recovery work. It does not authorize sending DEFAULT when analysis is indeterminate: retain a known confirmed setting or explicitly defer when the prior configuration is unknown.
- TestMode simulates the state transitions, makes no SOM API calls, and writes neither live acknowledgement checkpoint.

The native buying/selling behavior is the user's supplied contract, not a claim that this new implementation has already passed configured PT validation. Endpoint/token and per-target runtime checks remain open.

## Delivery and history boundaries

The confirmed-delivery checkpoint is `_data/ConfigurationDeliveryState.json`. It records configuration identity and payload hash, not the raw PT payload or secrets. A failed send must not advance it. TestMode never writes it.

Global SOM metadata is stored separately at `_data/StartupSellOnlyModeState.json`. Enabling the guard does not mark a preset as applied. A failed release preserves normal configuration acknowledgement and leaves guard release pending. Application.ProfitTrailerServerAPITokenXtra supports aligned additional-target tokens; its empty default explicitly shares the primary token. Neither checkpoint stores tokens.

The separate bounded decision history records analyzed/evaluated inputs, validity, source/configuration hashes, chosen state, startup protection, and delivery outcome. A successful history append is not a PT acknowledgement.

## Work authorized alongside these fixes

Phase 1D adds CorrelationToBTC, MeanCorrelationToBTC, and MedianCorrelationToBTC. Default N=30; valid range 3–1000. Pearson uses simple returns on exact synchronized complete UTC TrendMinutes endpoints with all required underlying source observations. Missing history and zero variance are unavailable. Global coverage is 90% of the exact selected global population.

Minimal decision history defaults to enabled, 30-day retention, and 256 MiB total quota. JSONL segments rotate at 16 MiB; pruning removes whole oldest files. No license, token, raw general configuration, raw PT payload, or raw exception strings are part of the audit record.

These additions have explicit passing deterministic evidence: 21 correlation checks at `86c2ea3` and 13 decision-history checks at `d331fbd`. Configured data, export/Monitor integration, and runtime provenance remain separate acceptance work.

## Deferred and excluded work

Dedicated performance work is deferred until all approved new metrics, including derivatives, higher-order states, and liquidity, are complete. The historical snapshot-reuse proposal is retained as future work, not a prerequisite for correlation.

Personal strategy development is independent and excluded. Neutral configuration fixtures verify application behavior without importing a strategy project into the release scope.

## Closure policy

Keep this issue open until the user-supplied evidence resolves each applicable row. Record actual source SHA, environment, configuration identity, case, and result. A source commit, a console test authored in the repository, or a TestMode run without PT writes is not evidence of successful real PT delivery.

[Current status](../STATUS.md) · [Current decisions](../DECISIONS.md) · [Current technical roadmap](../roadmaps/CURRENT.md) · [Verification handoff](../handoffs/2026-11-07-stabilization-correlation-validation.md)
