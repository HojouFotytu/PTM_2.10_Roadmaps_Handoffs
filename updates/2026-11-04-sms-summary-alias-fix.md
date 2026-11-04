# 2026-11-04 — SMS summary list-sharing defect corrected in source

**Application:** `HojouFotytu/PTMagic`, branch `phase1/market-data-foundation`, commit [`0e8ab70`](https://github.com/HojouFotytu/PTMagic/commit/0e8ab7056d32f16d1095a519ac4a1e87a29a4188).

## Root cause

On the first activated SMS for a market, `matchedMarketTriggers.Add(marketPair, matchedSingleMarketTriggers)` retained the same mutable list that `smss.TriggerSnapshot.MatchedTriggersContent` later stored. When another SMS activated, `matchedMarketTriggers[marketPair].AddRange(...)` modified both the market-level list and the first setting's persisted snapshot. BTC showed 9 descriptions for 3 own triggers, ETH 5 for 4, and SOL 4 for 3.

## Correction

- `Core/Main/PTMagic.cs` now uses `MatchedMarketTriggerContent.Append` and `CopyForSnapshot` for aggregation and saved snapshots.
- `Core/Helper/MatchedMarketTriggerContent.cs` creates separate list instances, preserving PT comment ordering and content.
- Added 5 checks under `Tests/Phase1SmsSummaryIsolation`: first setting isolation, order, multiple markets, defensive list copies, and JSON export round-trip.

**Evidence boundary:** This commit is source-only. No .NET build or automated tests were run by the assistant. Rerun build, the five new checks, existing 53 tests, and a TestMode raid with two or more SMS settings per market. The user-provided Market Metrics page already confirmed Phase1C analytics/Monitor content. Do not mark Phase1C fully DONE until this corrective change is verified.
