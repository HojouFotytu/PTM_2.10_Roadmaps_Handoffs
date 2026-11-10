# PTMagic 2.10 — Startup SOM enable-only safety handoff

**Date:** November 10, 2026 (KST)  
**Application source:** `8b6ad114ff86f3468f84f0adf2f1bbf2d69d3b24` · existing branch `phase1/market-data-foundation`  
**Current verification:** **PENDING** local .NET build and regression run after code changes. Earlier verified `49f2aab` funding/OI 332/332 results apply only to that earlier code.

## Owner-approved behavior

Startup Global SOM is **enable-only**. With `StartupSellOnlyMode=true`, PTMagic issues `enabled=true` before the initial disruptive startup analysis; it NEVER sends `enabled=false` automatically, including after successful configuration delivery, later raids, restarts or changes to the Startup Global SOM option. The user turns SOM OFF manually from ProfitTrailer when ready to allow buying. This deliberately avoids reading an unavailable global-SOM ownership state or overriding previously user-enabled SOM.

This mechanism only controls PT's native global switch; it never sends a temporary PAIRS/DCA/INDICATORS shadow preset. ProfitTrailer new buys and DCA buys remain blocked while global SOM is enabled; sells continue. TestMode does not send SOM requests.

The API helper itself refuses disabled=false requests, preventing accidental legacy call sites from disabling global SOM. Schema 1 `PendingRelease` checkpoints are migrated into manual-review state; they cannot authorize an API disable. Schema 2 records pending enable and acknowledgement but does not claim to read the live PT flag. A failed or ambiguous enable does not silently allow an unprotected disruptive bootstrap; it requires review. On a new process startup, configured protection may be re-asserted for the new startup cycle; within the same cycle, no additional guard command is sent.

## Two-raid notification

- The first two completed RAID SUMMARY reports after startup protection include a clear `PT: SOM WARNING (startup raid 1/2)` or `(2/2)` message, instructing manual release in ProfitTrailer.
- The Monitor's top ticker row has a **red `PT: SOM`** item beside the existing global-setting, SMS and PT health tickers during those first two raids; the `(i)` tooltip describes why PTMagic enabled global SOM and explicitly says it will not turn SOM off.
- The red ticker automatically disappears after the second raid. It is an informational startup notice, not a live PT status signal or confirmation that the user has switched SOM off.
- The summary retains manual-review status for troubleshooting even after the temporary ticker disappears. No automatic off request is sent when it disappears.

## Source changed

- `Core/Main/PTMagic.cs`: enable-only lifecycle, fail-closed uncertainty, per-process two-raid summary warning and summary flags.
- `Core/ProfitTrailer/GlobalSellOnlyModeAPI.cs`: rejects requests to disable global SOM.
- `Core/ProfitTrailer/StartupSellOnlyModeState.cs`: v2 checkpoint; safe migration from v1 auto-release intent.
- `Core/DataObjects/PTMagicData.cs`: summary properties for manual-review and transient warning visibility.
- `Monitor/Pages/_get/TickerWidgets.cshtml`: red `PT: SOM` ticker and explanation tooltip.
- `Monitor/Pages/_Layout.cshtml`: ticker insertion/removal across the existing periodic AJAX refresh.
- `Monitor/Pages/SettingsGeneral.cshtml`: manual-release help text.
- `Tests/ConfigurationLifecycle/Program.cs`: reverse legacy auto-release assertions and add migration, restart, warning-count, and uncertainty tests.

## Mandatory development verification

Run from PTMagic repository root:

```powershell
git switch phase1/market-data-foundation
if ($LASTEXITCODE -ne 0) { throw "Branch switch failed" }

git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull failed" }

& ".\Tests\Phase2OpenInterestIncremental\Run-Phase2Validation.ps1"
```

The runner builds Core, PTMagic and Monitor and executes all 16 existing deterministic test projects, including ConfigurationLifecycle. No configured PT APIs are contacted by tests. Publish exact source SHA and actual failures/successes; do not inherit a previous `PASS` across this safety change.

**Separate later acceptance:** live PT API acknowledgement, multi-target partial enable reporting and actual Monitor browser tooltip behavior. Earlier Phase 1 configured integration work remains deferred as explicitly decided, without waiving normal offline development tests.

[Current technical roadmap](../roadmaps/CURRENT.md) · [Status](../STATUS.md) · [Decisions](../DECISIONS.md).
