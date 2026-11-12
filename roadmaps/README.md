# PTMagic 2.10 Roadmaps

**D-053 implementation checkpoint — November 12, 2026:** PTMagic application source [`892a5f1f4729a3fccd3cb477ba6ad22fbbe0918d`](https://github.com/HojouFotytu/PTMagic/commit/892a5f1f4729a3fccd3cb477ba6ad22fbbe0918d) now removes the three OI/long-short positioning metrics, OI/ratio source acquisition and active cache integrations, obsolete tests, and UI labels. The **24 retained metrics** include 17 global-capable and seven asset-only measurements; settled funding remains with independent safe acquisition. A new user-local .NET build, the reduced **15-harness** offline suite and configured runtime checks are **pending**. The earlier `d101b5a0` 18-harness PASS is **pre-removal evidence**, not validation of the new code. This status **supersedes all earlier “source removal pending” or OI/positioning future-work instructions** in this document; past implementation and validation records are historical. The next step is local validation of `892a5f1f4729a3fccd3cb477ba6ad22fbbe0918d`, not further OI/positioning development.


**D-053 scope (November 12):** OI and long/short positioning metrics and their planned market aggregates/higher-order conditions are withdrawn. The [current technical roadmap](CURRENT.md) targets 24 remaining metrics. Source removal is pending at tested pre-removal source `d101b5a03e01f8f76acf8cc9a6bde7214ff34aa2`; older dated plans are historical.

## Current authority

**[CURRENT.md](CURRENT.md)** is the standalone current technical roadmap. [../ROADMAP.md](../ROADMAP.md) is its concise user-facing overview. Current implementation and execution evidence are in [../STATUS.md](../STATUS.md).

## Historical sources

| File | Historical role |
|---|---|
| [original.txt](original.txt) | Original market-analysis expansion proposal |
| [revised-2.9.1-2026-11-04.txt](revised-2.9.1-2026-11-04.txt) | Earlier version designation; superseded when this work became 2.10 |
| [revised-2.10-2026-11-04.txt](revised-2.10-2026-11-04.txt) | Earlier readiness/Phase 1C planning snapshot |
| [revised-2.10-2026-11-04-markettrend-timeframe.txt](revised-2.10-2026-11-04-markettrend-timeframe.txt) | Detailed November 4 plan with the TrendMinutes correction and appended acceptance history |

These files are preserved unchanged. They contain historical statements about a parallel legacy PriceTrend path, completed work, pending tests, metric names, and development order. **They do not override the current normalized contract, current decision register, or the November 7 deferral of performance work until all new metrics are complete.**

Do not resume from a historical “next action” or “current handoff” section. Start with the [current handoff](../handoffs/2026-11-07-stabilization-correlation-validation.md).
