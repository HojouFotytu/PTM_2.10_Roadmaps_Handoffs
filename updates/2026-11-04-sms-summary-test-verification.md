# 2026-11-04 — SMS summary list-isolation regression verification

**Application:** `HojouFotytu/PTMagic`, branch `phase1/market-data-foundation`  
**Fix commit:** [`0e8ab70`](https://github.com/HojouFotytu/PTMagic/commit/0e8ab7056d32f16d1095a519ac4a1e87a29a4188)  
**Task:** `P1C-SMS-SNAPSHOT-ALIAS`.

## User-executed verification

```powershell
git pull --ff-only
dotnet build
dotnet run --project Tests/Phase1SmsSummaryIsolation/Phase1SmsSummaryIsolation.csproj
dotnet run --project Tests/Phase1COhlcv/Phase1COhlcv.csproj
dotnet run --project Tests/Phase1MetricWarnings/Phase1MetricWarnings.csproj
dotnet run --project Tests/Phase1TriggerLogic/Phase1TriggerLogic.csproj
dotnet run --project Tests/Phase1AReadiness/Phase1AReadiness.csproj
```

- Git: **Already up to date**.
- Core net10.0 **0.3s**, PTMagic net10.0 **0.1s**, Monitor net10.0 **4.3s**; total `dotnet build` **succeeded in 5.9s**.
- SMS isolation: **5/5 passed**.
- Phase1COhlcv: **13/13 passed**.
- Metric warnings: **7/7 passed**.
- Tri-state triggers: **29/29 passed**.
- Phase1A readiness: **4/4 passed**.
- **58/58 deterministic checks passed**.

**Verification boundary:** The corrected production helper is compiled and all deterministic tests pass, including list separation and JSON serialization. A deployed TestMode raid using two or more simultaneously active SMS per market, followed by inspection of each setting's persisted `TriggerSnapshot.MatchedTriggersContent` in `_data/SingleMarketSettingSummary.json`, has not been supplied. This is the final outstanding issue-specific runtime check for Phase 1C closeout. Previous live analytics/trigger TestMode and Monitor content evidence remains valid.

## Uploaded TestMode follow-up (19:05–19:07 KST)

The user supplied a later deployed TestMode log and JSON exports. The eight SMS entries still contain old activation timestamps from 18:32 KST and `RefreshOffTriggers=false`; the first BTC/ETH/SOL entries retain old foreign trigger lines. They were **loaded and resaved**, not freshly generated. This leaves the new runtime list-copy fix **unconfirmed by live JSON**, but does not contradict the 58/58 passing tests. See [detailed validation](2026-11-04-sms-postfix-retained-snapshots.md).
