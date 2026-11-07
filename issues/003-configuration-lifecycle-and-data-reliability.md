# Issue 003 — Configuration lifecycle and analytical reliability

**Opened:** November 7, 2026

**Source reviewed before changes:** PTMagic `d0b0b877d6157b0db44cc4d1d2ac4b0cb0799abc`

**Implementation checkpoint:** `86c2ea3ff430b62e654f929a222935ec53ea8fa6`

**Status:** Build and eight harnesses passed at `78967a7`; the next harness failed, and complete regression/runtime acceptance remains open.

This issue records the actionable findings from the November 7 review and their current disposition. It does not claim that every defect was introduced by 2.10. Several findings concern long-standing configuration lifecycle code that new metrics make more consequential.

## Latest execution evidence

The user-local build at exact source `78967a7703ab9f57fece40d488fc538b1caf393b` passed for Core, PTMagic, and Monitor with SDK 10.0.403 in 9.6 seconds. Eight harnesses completed with 125 passing checks. TriggerConfigurationValidation printed 23 PASS results, then failed case 24, “timed and volume off-triggers need no trend,” for OffTrigger #2 with an empty MarketTrend name. The three remaining harnesses did not run. The Razor compilation correction is confirmed; this issue remains open.

A separate runtime excerpt shows a Binance Futures ticker request with `symbol=USDT`, blank MainMarket, and an aborted raid. Its stack locations match the older `d0b0b87` baseline and it lacks the current Source revision line, suggesting an older running binary without identifying its exact SHA. [The dated evidence record](../updates/2026-11-07-build-and-partial-harness-validation.md) preserves this inference and the incomplete regression results.

The failing validator case was a fixture defect: double.MaxValue minus 1 rounds back to the unbounded sentinel. The corrected fixture uses a finite cap and adds boundary controls; production validation is unchanged. Bootstrap source corrections preserve default-file assignments when property groups are null, require the exact valid market property before exchange I/O, and use the USDT price identity. The current authored inventory is 272 groups across twelve projects, including 40 validator and 66 lifecycle groups. These corrections are published and require the user-local rerun and restart of the updated configured instance. [Publication status](../STATUS.md#publication-status).

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

These additions have their own new acceptance cases; they are not implicitly validated by the old 88-check baseline.

## Deferred and excluded work

Dedicated performance work is deferred until all approved new metrics, including derivatives, higher-order states, and liquidity, are complete. The historical snapshot-reuse proposal is retained as future work, not a prerequisite for correlation.

Personal strategy development is independent and excluded. Neutral configuration fixtures verify application behavior without importing a strategy project into the release scope.

## Closure policy

Keep this issue open until the user-supplied evidence resolves each applicable row. Record actual source SHA, environment, configuration identity, case, and result. A source commit, a console test authored in the repository, or a TestMode run without PT writes is not evidence of successful real PT delivery.

[Current status](../STATUS.md) · [Current decisions](../DECISIONS.md) · [Current technical roadmap](../roadmaps/CURRENT.md) · [Verification handoff](../handoffs/2026-11-07-stabilization-correlation-validation.md)
