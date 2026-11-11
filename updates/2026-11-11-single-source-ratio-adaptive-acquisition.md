# PTMagic 2.10 — Single-source ratio and adaptive derivative acquisition decisions

**Date:** November 11, 2026 (KST)  
**Documentation repository:** `HojouFotytu/PTM_2.10_Roadmaps_Handoffs`  
**Application repository:** `HojouFotytu/PTMagic`, existing branch `phase1/market-data-foundation`

## Owner decisions

### 1. Retain only the public global-account ratio

The only approved long/short ratio metric is:

- `GlobalLongShortAccountRatio`

Remove from the PTMagic 2.10 scope entirely:

- `TopTraderLongShortAccountRatio`
- `TopTraderLongShortPositionRatio`

The two top-trader feeds are not to remain as disabled, optional or credential-gated features. Their account-count versus position-size distinction is no longer part of the active ratio design.

The retained global-account endpoint is public and does not require the additional optional Binance Futures API key. The top-trader-only API-key dependency and authentication path are therefore unnecessary.

### 2. Remove user-configurable per-raid request budgets

These three values are application-level acquisition mechanics, not user-facing controls:

- `OpenInterestMaxRequestsPerRaid`
- `FundingMaxRequestsPerRaid`
- `LongShortRatioMaxRequestsPerRaid`

Remove them from the PTMagic analyzer configuration surface. Do not replace them with other arbitrary user-configurable static request ceilings.

PTMagic should manage derivative acquisition dynamically through the shared Binance rate-limit state, endpoint request weights, response headers and Binance 429/418 cooldowns. The scheduler should coordinate the enabled derivative families rather than treating each family as an independent static per-raid allowance.

Retain internal safeguards for endpoint pagination, per-symbol page progress, fair scheduling, incremental coverage, cache persistence, cancellation, retry/cooldown handling and UNAVAILABLE semantics. These remain application-owned mechanics.

### 3. Strict workstream separation

This decision is for PTMagic application development only. PTMagic application code, APIs, data acquisition, analytics, Monitor and PTM documentation are separate from ProfitTrailer LONG/SHORT strategy-settings development.

No PAIRS/DCA/INDICATORS strategy files, LONG/SHORT analyzers, strategy-setting repositories or settings-development documents are authorized or changed by this decision.

## Implementation status

These are approved design decisions, not claims of completed implementation.

The last user-tested application source before this decision is `f108cd1ab39c44103bed91d1899f90f86a830eb4`, where the .NET 10.0.403 solution build and all 17 offline harnesses / 384 checks passed. That test evidence predates these changes and validates the prior three-source ratio and static per-raid budget design. It does not validate the new single-source/adaptive-scheduling design.

No PTMagic application source or configuration files were changed as part of this documentation update.

## Next PTMagic application work

1. Remove the two top-trader metrics, endpoints, source variants and API-key-only path from PTMagic application code.
2. Retain the global-account ratio data model, calculation, cache and public endpoint.
3. Remove the three user-configurable per-raid budget properties from PTMagic application configuration and runtime binding.
4. Implement a shared adaptive derivative acquisition scheduler driven by Binance's actual rate-limit state, endpoint weights and cooldowns. Preserve internal fairness and progress safeguards without reintroducing arbitrary user-facing static limits.
5. Add focused tests, run the full offline suite, then continue configured Unicode-market raid and two-startup persistence acceptance.

See [D-051 and D-052 in the decision register](../DECISIONS.md), [current status](../STATUS.md), [current roadmap](../roadmaps/CURRENT.md), and the [active handoff](../handoffs/2026-11-10-som-enable-only.md).
