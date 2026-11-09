# PTMagic 2.10 — Stabilization, correlation, and decision-history validation

**Date:** November 7, 2026

**Application repository:** HojouFotytu/PTMagic

**Branch:** `phase1/market-data-foundation`

**Application source checkpoint:** `87b9eaa1c865e39d8fff6a657e1b332012be8c16`

**Reviewed source tree:** `078de36bae9f9fcc2e439c8080feec548c8a0ec9`

**Current plan:** [roadmaps/CURRENT.md](../roadmaps/CURRENT.md)

**Current state:** [STATUS.md](../STATUS.md)

This is the sole current development handoff. Earlier dated handoffs remain historical. Begin with the actual application branch and source, then use the contracts and verification sequence below.

**Publication authorization:** [D-038](../DECISIONS.md#d-038--standing-authorization-to-publish-ptm-210-development) records the user's standing authorization to publish PTM 2.10 development changes to the named application and documentation branches without renewed conversational approval. Actual tool restrictions remain binding. The source checkpoint above is published. Deterministic validation is complete; configured runtime acceptance is next.

## November 9 reuse of previous configured LONG/SHORT captures

Previously supplied performance archives were reviewed through their published diagnostics and saved decision audits. SHORT has 358 PTM TestMode decisions (120 at source `86c7d2b`), including consecutive fresh cycles at 11:15:54 and 11:20:54 KST on November 9, with no recorded confirmed PT delivery; latest inspected metrics have sufficient history and complete sampled populations. The current application `87b9eaa` only changes logging configuration and changelog relative to that tested engine. LONG has a separate 117-decision **non-TestMode** application sample, which is not TestMode evidence. The retained decisions establish configured TestMode evaluation/no-confirmed-delivery behavior, **not** literal completed RAID SUMMARY evidence or actual native SOM acknowledgement. See [the existing evidence review](../updates/2026-11-09-reused-configured-testmode-evidence.md).

**Reuse rule:** do not ask the user to run the same decision/coverage validation again. Section 3A's process launch and Section 4's test matrix remain available **only for a genuinely missing scenario or a relevant new code change**, not as an automatic repeat. Existing files should be used first. PT API, Monitor browser, cache two-startup comparison, and console-color visual rendering remain separate acceptance gates.

## November 9 presentation change — TestMode console highlighting

Published application source `87b9eaa1c865e39d8fff6a657e1b332012be8c16` updates the three NLog console configurations to use the startup warning's purple/magenta color for any message containing `TestMode` (case-insensitive), including startup global SOM previews, configuration previews and RAID SUMMARY. Severity and file-log text remain unchanged.

**Local build and static config checks passed November 9:** the user's `git pull --ff-only` reported *Already up to date*, .NET 10 `dotnet build` passed in **15.1s** (Core, PTMagic and Monitor), and all three `nlog.config` XML/`highlight-row` assertions printed **PASS**. The supplied command did **not** print a Git HEAD SHA. **Visible console colors and live configuration deployment remain unverified.** Use the existing correct runtime directory when deploying `nlog.config`; recompiling the binary alone does not update an installed external config. Do not disturb a running instance solely to test this cosmetic change.

Focused verification (PowerShell, from the application repository after pulling the pinned branch):

```powershell
& {
  $ErrorActionPreference = "Stop"
  Set-Location -LiteralPath "G:\PTM Dev Bot\PTMagic Github Clone\PTMagic"
  git switch phase1/market-data-foundation
  if ($LASTEXITCODE -ne 0) { throw "Branch switch failed" }
  git pull --ff-only
  if ($LASTEXITCODE -ne 0) { throw "Git pull failed" }
  $Actual = (git rev-parse HEAD).Trim()
  if ($LASTEXITCODE -ne 0) { throw "Source identity failed" }
  if ($Actual -ne "87b9eaa1c865e39d8fff6a657e1b332012be8c16") { throw "Wrong source: $Actual" }
  dotnet build .\PTMagic.sln
  if ($LASTEXITCODE -ne 0) { throw "Build failed" }
  foreach ($path in @(
    "PTMagic/nlog.config",
    "Monitor/nlog.config",
    "PTMagic/_defaults/_default_settings_PT_2.x/nlog.config"
  )) {
    [xml]$doc = Get-Content -LiteralPath $path -Raw
    $ns = [System.Xml.XmlNamespaceManager]::new($doc.NameTable)
    $ns.AddNamespace("n", "http://www.nlog-project.org/schemas/NLog.xsd")
    $node = $doc.SelectSingleNode("//n:target[@name='Console']", $ns)
    if ($null -eq $node -or $node.GetAttribute("type", "http://www.w3.org/2001/XMLSchema-instance") -ne "ColoredConsole") {
      throw "Missing ColoredConsole target in $path"
    }
    $rules = $node.SelectNodes("n:highlight-row", $ns)
    if ($rules.Count -ne 1 -or $rules[0].GetAttribute("foregroundColor") -ne "Magenta" -or
      $rules[0].GetAttribute("condition") -ne "regex-matches('${message}', 'testmode', 'ignorecase')") {
      throw "Missing TestMode highlight rule in $path"
    }
    Write-Host "PASS: TestMode purple console rule - $path"
  }
}
```

Visual acceptance: after deploying the correct `nlog.config` and restarting normally, verify that the startup `TESTMODE ENABLED` warning, `TESTMODE: startup global SOM preview`, `TESTMODE: configuration evaluated`, and RAID SUMMARY entries containing `TestMode` all show the same magenta/purple color. Regular INFO and WARN log colors must remain unchanged, and plain-text `_logs` must remain uncolored.

## November 9 focused validation — normalized OHLCV warm start

The new source `925db7c153ee4d53cfe3b7bf736318e7a30bccf1` is published with a versioned, per-exchange/market compressed five-minute candle cache. It restores validated closed history before the pinned refresh, and only gaps/missing periods trigger additional fetches. Cache data is not an acknowledgement and cannot override completeness/freshness rules. The separate legacy one-minute MarketData reconstruction remains unchanged.

**Focused acceptance completed:** 8 warm-start checks, 16 analytics-reliability checks and 13 Phase 1C OHLCV checks passed (37/37) at `925db7c` with a successful 18.3-second solution build using .NET SDK 10.0.403. Earlier 272 passing checks were executed on previous revisions; do not label them as run on the current commit.

Run this exact PowerShell from any initial directory to validate the source and the focused tests:

```powershell
& {
  $ErrorActionPreference = "Stop"
  function Assert-NativeSuccess {
    param([string]$Step)
    if ($LASTEXITCODE -ne 0) { throw "$Step failed with exit code $LASTEXITCODE." }
  }

  Set-Location -LiteralPath "G:\PTM Dev Bot\PTMagic Github Clone\PTMagic"
  if (-not (Test-Path ".\PTMagic.sln")) { throw "PTMagic.sln not found." }

  git status --short
  Assert-NativeSuccess "git status"
  git switch phase1/market-data-foundation
  Assert-NativeSuccess "git switch"
  git pull --ff-only
  Assert-NativeSuccess "git pull"
  $ActualSource = git rev-parse HEAD
  Assert-NativeSuccess "git rev-parse HEAD"
  $ExpectedSource = "87b9eaa1c865e39d8fff6a657e1b332012be8c16"
  if ($ActualSource.Trim() -ne $ExpectedSource) {
    throw "Expected $ExpectedSource but got $ActualSource"
  }

  dotnet --version
  Assert-NativeSuccess "dotnet --version"
  dotnet build ".\PTMagic.sln"
  Assert-NativeSuccess "dotnet build"

  foreach ($Project in @(
    "Tests/NormalizedWarmStartCache/NormalizedWarmStartCache.csproj",
    "Tests/Phase1AnalyticsReliability/Phase1AnalyticsReliability.csproj",
    "Tests/Phase1COhlcv/Phase1COhlcv.csproj"
  )) {
    if (-not (Test-Path $Project)) { throw "Missing harness: $Project" }
    Write-Host "Running $Project"
    dotnet run --project $Project
    Assert-NativeSuccess $Project
  }
  Write-Host "Focused warm-start validation commands completed for $ActualSource"
}
```

Expected focused groups if every project runs: 8 new warm-start + 16 analytics reliability + 13 OHLCV = **37**. All 37 focused checks were executed and passed at `925db7c`; the subsequent `86c7d2` documentation update changes no executables. Configured cold/restart comparison remains open.

**Configured runtime acceptance:** With the same exchange, settings, symbol population and `StoreDataMaxHours`, run a cold startup to populate `_data/NormalizedOhlcvCache`; then shut down normally, restart shortly afterward, and compare the `Normalized warm-start restored ...` line and normalized kline counts. Warm restart should request only the gap/overlap when the retained history is complete. Verify no cross-exchange reuse and that missing/corrupted snapshots trigger full backfill without fabricated values. TestMode is suitable for the network/readiness check and continues to suppress PT configuration/SOM writes. Preserve the live instance's configuration and any running process; never start a second concurrent instance or delete its data files to force cold testing.

## 1. What is ready, and what is not yet accepted

The latest user run identifies exact source **`d331fbd059041241069646c3bb82ac6549423a70`**, using **.NET SDK 10.0.403**. Core, PTMagic, and Monitor built successfully in **10.9 seconds**. ConfigurationLifecycle passed all **66 checks**, and DecisionHistory passed all **13**. The continuation reached its successful completion message.

The preceding run at `86c2ea3ff430b62e654f929a222935ec53ea8fa6` built the solution in 15.8 seconds and passed **193 checks in ten harnesses**, including 40 TriggerConfigurationValidation and 28 MonitorSettingsRoundTrip checks. The two qualified Telegram fixture constructors were the only executable changes before the successful continuation; production source and assertions were unchanged. **All 272 checks across twelve projects now have passing results over these two recorded revisions.** This is not a single full-suite execution at `d331fbd`. [Latest exact-source evidence](../updates/2026-11-07-completed-harness-validation.md).

The current application checkpoint `a0b375c` adds [the cumulative effective-change record](../CHANGELOG-2.10.md) and its PR/merge maintenance requirement, makes StartupSellOnlyMode=true explicit in the development general-settings template (the packaged template already contained it), and clarifies the existing Monitor APPLICATION toggle with visible TestMode help. Engine code, projects, test cases and assertions are unchanged; no harness rerun is required solely for these documentation/template/static-view edits. The source was reviewed and the templates parsed; no new .NET build or browser result is claimed. Configured TestMode behavior, actual PT API acknowledgement/native SOM behavior, and browser integration remain separate acceptance work.

A subsequent runtime log repeats the bare `symbol=USDT` failure while using an existing configured runtime directory separate from the Git checkout. Its first raid completes and reports a non-default setting transition; the next loads only 13/12/11 property lines and fails with an empty main market. Both raids omit the current unconditional `Source revision` and `Analysis main market` lines and follow the older Core code layout. The process therefore executes pre-fix Core behavior; its exact SHA and loaded DLL path are not shown. The runtime working directory alone does not identify the loaded assembly. The log also lacks the TestMode banner and reports a PT update, so it is not configured TestMode evidence for the current code. [Deployment diagnosis](../updates/2026-11-07-completed-harness-validation.md#subsequent-configured-runtime-report-runtime-core-is-still-older).

A later explicit compiled-DLL launch reached preset validation and stopped on a missing file referenced by the Default setting. That is configuration-file resolution, before SOM enable and exchange loading. The user subsequently reported a long initial run underway and asked why SOM had not activated with TestMode enabled; no completed-raid output or remote SOM acknowledgement has been supplied for that run. Collect its result and source identity before requesting a repeat. TestMode deliberately simulates SOM and cannot establish the remote flag. Section 3A remains the complete launch procedure if another run is needed; it preserves the existing runtime folder and private files. The default-template and help-text update does not require interrupting the ongoing analysis.

The previous `78967a7` run and its sentinel-fixture failure remain in the earlier evidence record. At `86c2ea3`, the corrected finite cap and both added sentinel boundary checks passed. At `d331fbd`, main-market parsing/inheritance, invalid-input boundaries, guard/configuration orchestration, delivery retry, SMS transitions, and history checks also passed. The solution builds Core, PTMagic, and Monitor; each separate harness was compiled and executed by its own recorded `dotnet run` invocation.

The accepted pre-change evidence remains the November 5 .NET 10 build, 88 checks across six harnesses, and nine Futures USDT TestMode raids associated with d0b0b87. Those logs identify version 2.10.0 but not an exact source SHA. The 5,192 matching normalized export/runtime values establish internal consistency, not parity with the removed legacy calculation. Positive BTC OffTrigger followed by immediate reactivation did not establish lasting removal.

D-021 assigns local execution to the user. The assistant implements, inspects, authors cases, and fixes reported failures. No automatic remote CI is required or reinstated.

## 2. Current contracts to preserve

| Area | Contract |
|---|---|
| Final SMS removal | An applied nonempty SMS set becoming empty is a PT configuration transition |
| Delivery | Desired, pending, and confirmed state remain distinct; failures retain a retry even if the desired preset/payload is unchanged |
| Partial delivery | A partial multi-target failure leaves uncertainty; returning to an earlier desired configuration still requires delivery instead of trusting an old confirmed hash |
| Same-name reload | Current setting definitions and preset contents are recompiled even when the selected name remains the same |
| Confirmed checkpoint | `_data/ConfigurationDeliveryState.json`; identity and payload hash only; no raw PT properties/secrets; TestMode never writes it |
| Startup guard | `Application.StartupSellOnlyMode=true`; `POST /api/v2/globalSellOnlyMode` with query token and enabled=true before slow exchange bootstrap; no startup properties upload |
| Native behavior and ownership | User clarified: global SOM stops new buys and DCA buys while allowing sells. PTM owns the flag for the startup cycle; no prior-state readback/restoration is implemented |
| Guard failure/release | Enable failure aborts before slow bootstrap; after fresh conclusive analysis, normal configuration acknowledgement precedes a separate enabled=false request. Release failure retains the normal acknowledgement and pending guard release |
| Guard metadata/tokens | `_data/StartupSellOnlyModeState.json` is separate from configuration delivery. ProfitTrailerServerAPITokenXtra supplies aligned additional-target tokens; empty explicitly shares the primary token |
| Opt-out | StartupSellOnlyMode=false prevents a new guard; a matching pending PTM-owned guard checkpoint still resumes recovery. Indeterminate startup retains known confirmed configuration or defers unknown state; it does not force DEFAULT |
| Decision age | `MaxAnalysisAgeSeconds=300`, range 1–86400 seconds, compares decision time with the pinned analysis time; missing/future/expired pins unavailable |
| Acquisition | Request bounds and stored observations preserve the same pinned analytical window across candle closes |
| Trigger references | Missing/ambiguous identities and malformed expressions are fatal configuration errors; defensive evaluation remains unavailable |
| Main-market bootstrap | Preserve inherited assignments for null property groups; read and normalize the exact market property; reject missing/malformed values before exchange I/O; USDT identity conversion needs no ticker call |
| Diagnostic metrics | Unknown/disabled/wrong-scope metrics remain accepted warning-producing diagnostic inputs, not valid observations |
| Monitor | Ordered distinct rows, Metric/Tag, inactive fields, property types, and full precision survive save; stale revision refuses overwrite |
| Concentration | Top10 mean return minus remaining eligible mean return in percentage points; rank using the same TrendMinutes trailing volume window; min eleven and 100% coverage |
| Correlation | Asset CorrelationToBTC and global MeanCorrelationToBTC/MedianCorrelationToBTC; Pearson(simple returns), exact synchronized complete history, N=30 default, range 3–1000 |
| Correlation validity | No fill or shortened overlap; missing source observations or zero variance unavailable; exact selected population and 90% global coverage |
| History | Enabled by default; 30 days, 256 MiB total, 16 MiB JSONL segments under `_data/DecisionHistory/YYYY-MM-DD-NNNNNN.jsonl`; prune complete oldest files |

The user rejected the initial unpublished full-preset overlay. The current startup API call leaves PAIRS/DCA/INDICATORS unchanged. TestMode makes no SOM API calls or live checkpoint writes and cannot prove that the guard, normal configuration, or release reached ProfitTrailer. Enabling StartupSellOnlyMode assigns the global flag to PTM: a previously enabled global flag is still requested false after a successful startup cycle, because the setter contract does not expose prior-state ownership.

The history-requirement export distinguishes complete-period lower bounds from current-raid slots and all-alignments retention. Default 24-hour trends have conservative StoreDataMaxHours guidance of 384h for ATR(14), 528h for VolumeExpansion(20), and 744h for Correlation(30). It warns on insufficiency rather than silently extending retention.

## 3. Local commands and deterministic execution record

### A. When another run is needed — select the built DLL with the existing runtime configuration

The deterministic checks are complete. First collect the already-reported long run rather than interrupting it for this template/help update. If another run is needed, stop the previous PTMagic instance through its normal startup/stop procedure before starting another. Set `$PtmRuntime` below to the **existing configured PTMagic runtime folder**, and first confirm `GeneralSettings.Application.TestMode=true` in that folder's `settings.general.json`. Keep its existing analyzer and preset filenames.

Run the complete block below in PowerShell to pull the documentation checkpoint, record the source, build, and start the resulting **absolute DLL path** with the existing runtime directory as its working directory. This selects the updated binary directly instead of relying on the installed launcher. The script does not change TestMode, copy deployment files, or overwrite settings/presets/data.

Review the printed working-tree status. Local source changes must be recorded with the build's -dirty identity and cannot be reported as the clean checkpoint. Private configuration/preset differences are identified separately by the recorded configuration and payload hashes.

```powershell
& {
    $ErrorActionPreference = "Stop"

    $PtmRuntime = "<existing configured PTMagic runtime folder>"

    function Assert-NativeSuccess {
        param([string]$Step)
        if ($LASTEXITCODE -ne 0) {
            throw "$Step failed with exit code $LASTEXITCODE."
        }
    }

    Set-Location -LiteralPath "G:\PTM Dev Bot\PTMagic Github Clone\PTMagic"

    if (-not (Test-Path ".\PTMagic.sln")) {
        throw "PTMagic.sln was not found in the application repository."
    }

    git status --short
    Assert-NativeSuccess "git status"

    git switch phase1/market-data-foundation
    Assert-NativeSuccess "git switch"

    git pull --ff-only
    Assert-NativeSuccess "git pull"

    $ActualSource = git rev-parse HEAD
    Assert-NativeSuccess "git rev-parse HEAD"
    $ExpectedSource = "925db7c153ee4d53cfe3b7bf736318e7a30bccf1"
    Write-Host "Application source: $ActualSource"
    if ($ActualSource.Trim() -ne $ExpectedSource) {
        throw "Source differs from this handoff ($ExpectedSource). Record the actual source before continuing."
    }

    dotnet --version
    Assert-NativeSuccess "dotnet --version"

    dotnet build ".\PTMagic.sln"
    Assert-NativeSuccess "dotnet build"

    $PtmDll = Join-Path (Get-Location).Path "PTMagic\bin\Debug\net10.0\PTMagic.dll"
    if (-not (Test-Path -LiteralPath $PtmRuntime -PathType Container)) {
        throw "Set PtmRuntime to the existing configured PTMagic runtime folder."
    }
    $PtmRuntime = (Resolve-Path -LiteralPath $PtmRuntime).Path

    foreach ($RequiredFile in @(
        $PtmDll,
        (Join-Path $PtmRuntime "settings.general.json"),
        (Join-Path $PtmRuntime "settings.analyzer.json")
    )) {
        if (-not (Test-Path -LiteralPath $RequiredFile -PathType Leaf)) {
            throw "Required file was not found: $RequiredFile"
        }
    }

    Write-Host "Compiled application: $PtmDll"
    Write-Host "Runtime configuration folder: $PtmRuntime"
    Write-Host "Confirm TESTMODE ENABLED in the running application's log."
    Set-Location -LiteralPath $PtmRuntime
    dotnet $PtmDll
    Assert-NativeSuccess "PTMagic runtime"
}
```

### B. Complete twelve-project sequence — reference for later changes

The full sequence remains available for a later source change that requires regression execution. It is not an additional requirement for the current documentation-only update. Run this entire block in **PowerShell from the PTMagic application repository root**, not the documentation repository. It stops on a wrong branch/source, missing project, failed pull, build error, or failed harness. The exact SHA must match this handoff; a later source revision needs its own recorded identity and results.

```powershell
$ErrorActionPreference = "Stop"

function Assert-NativeSuccess {
    param([string]$Step)
    if ($LASTEXITCODE -ne 0) {
        throw "$Step failed with exit code $LASTEXITCODE."
    }
}

if (-not (Test-Path ".\PTMagic.sln")) {
    throw "Run this script from the PTMagic application repository root."
}

git status --short
Assert-NativeSuccess "git status"

$CurrentBranch = git branch --show-current
Assert-NativeSuccess "git branch"
if ($CurrentBranch.Trim() -ne "phase1/market-data-foundation") {
    throw "Expected branch phase1/market-data-foundation; found $CurrentBranch."
}

git pull --ff-only
Assert-NativeSuccess "git pull"

$ActualSource = git rev-parse HEAD
Assert-NativeSuccess "git rev-parse HEAD"
$ExpectedSource = "925db7c153ee4d53cfe3b7bf736318e7a30bccf1"
Write-Host "Application source: $ActualSource"
if ($ActualSource.Trim() -ne $ExpectedSource) {
    throw "Source differs from this handoff ($ExpectedSource). Record the actual source and reconcile before validation."
}

dotnet --version
Assert-NativeSuccess "dotnet --version"

dotnet build ".\PTMagic.sln"
Assert-NativeSuccess "dotnet build"

$Projects = @(
    "Tests/Phase1AReadiness/Phase1AReadiness.csproj",
    "Tests/Phase1COhlcv/Phase1COhlcv.csproj",
    "Tests/Phase1SmsSummaryIsolation/Phase1SmsSummaryIsolation.csproj",
    "Tests/Phase1TriggerLogic/Phase1TriggerLogic.csproj",
    "Tests/NormalizedPriceTrendMigration/NormalizedPriceTrendMigration.csproj",
    "Tests/Phase1MetricWarnings/Phase1MetricWarnings.csproj",
    "Tests/Phase1AnalyticsReliability/Phase1AnalyticsReliability.csproj",
    "Tests/Phase1DCorrelation/Phase1DCorrelation.csproj",
    "Tests/TriggerConfigurationValidation/TriggerConfigurationValidation.csproj",
    "Tests/MonitorSettingsRoundTrip/MonitorSettingsRoundTrip.csproj",
    "Tests/ConfigurationLifecycle/ConfigurationLifecycle.csproj",
    "Tests/DecisionHistory/DecisionHistory.csproj"
)

foreach ($Project in $Projects) {
    if (-not (Test-Path $Project)) {
        throw "Missing required harness: $Project"
    }
    Write-Host "Running $Project"
    dotnet run --project $Project
    Assert-NativeSuccess $Project
}

Write-Host "Build and all listed harness processes completed successfully."
Write-Host "Provide this output and the source SHA for review; runtime acceptance remains separate."
```

### Completed case inventory and provenance

All current authored groups have passing results. The source column preserves the actual revision used for each harness; no all-twelve-project run at one revision is claimed.

| Project | Passing checks/groups | Executed source |
|---|---:|---|
| Phase1AReadiness | 5 | `86c2ea3` |
| Phase1COhlcv | 13 | `86c2ea3` |
| Phase1SmsSummaryIsolation | 5 | `86c2ea3` |
| Phase1TriggerLogic | 29 | `86c2ea3` |
| NormalizedPriceTrendMigration | 18 | `86c2ea3` |
| Phase1MetricWarnings | 18 | `86c2ea3` |
| Phase1AnalyticsReliability | 16 | `86c2ea3` |
| Phase1DCorrelation | 21 | `86c2ea3` |
| TriggerConfigurationValidation | 40 | `86c2ea3` |
| MonitorSettingsRoundTrip | 28 | `86c2ea3` |
| ConfigurationLifecycle | 66 | `d331fbd` |
| DecisionHistory | 13 | `d331fbd` |

The completed inventory is **272 checks/groups across twelve projects**: **193 passed at `86c2ea3` and 79 at `d331fbd`**. The earlier `78967a7` partial run is preserved separately. The fixture qualification corrections are verified. The current `a0b375c` checkpoint adds the cumulative documentation, an explicit development-template default and static Monitor help; it changes no engine code or test assertions. Preserve all results under their executed sources.

The two added validator checks distinguish the adjacent representable volume cap from the exact unbounded sentinel. The ten added lifecycle groups cover exact/non-USDT market parsing; null, missing, blank, prefix-only, and malformed inputs; null PAIRS/DCA/INDICATORS inheritance; fresh-summary bootstrap with and without an acknowledged configuration; retention of an owned guard when the market is missing; and public Spot/Futures/US adapter identity and invalid-input boundaries using already-canceled tokens.

No removed selective-legacy project belongs in this sequence. Do not substitute an old total for the output of these current projects. Existing warning counts may change; capture warnings and failures accurately.

## 4. Runtime acceptance after deterministic checks

Use a configured deployment built from the exact recorded source. Confirm `GeneralSettings.Application.TestMode=true` before the initial runtime phase. Use application-owned neutral diagnostics; personal strategy presets and results are outside this task.

Section 3A selects the freshly built DLL and sets the working directory to `$PtmRuntime`. That command loads `$PtmRuntime\settings.general.json` and `$PtmRuntime\settings.analyzer.json`; exported data is under `$PtmRuntime\_data`. Keep the existing configured preset names. For logs, use console output or the active log file: the checked-in NLog path is based on the executable directory, so this Debug DLL normally writes under the checkout's `PTMagic\bin\Debug\net10.0\_logs` even though configuration/data come from the existing runtime directory.

For a permanently installed startup command, publish/update a coherent application bundle from the pinned source while preserving that installation's configuration, presets, data, and logs, then restart through its normal procedure. Do not copy only Core.dll or reuse the unchanged launcher as evidence that the updated application was selected. The direct DLL launch in section 3A is a validation run, not a permanent deployment update. Capture the raid's `Source revision` line and compare it with this handoff. A successful checkout build does not update or restart a separately deployed process; version 2.10.0 alone does not establish source identity.

The alternative `dotnet run --project .\PTMagic\PTMagic.csproj` from the repository root uses the project's RunWorkingDirectory, the checkout's `PTMagic` subdirectory. It therefore reads that subdirectory's settings and state. Use it only when that is the intended configured runtime, rather than assuming it reads a separate installation's settings.

Before accepting a new raid, confirm that the compiled PAIRS settings contain a valid `market` assignment. For the user's USDT configuration, expect `market = USDT` and `Analysis main market: USDT (compiled PAIRS for GlobalSetting '<actual setting>').` Missing or malformed values must produce a clear configuration error before exchange I/O. Null property-group inheritance and invalid direct adapter inputs already passed their deterministic checks; the configured runtime must now establish that the updated process resolves the intended market and completes a raid.

Capture startup and **two consecutive completed raids**, because the reported older-runtime pattern succeeded on its first raid and failed on the next after a setting transition. For both raids, verify the expected `Source revision`, `Analysis main market: USDT`, `Summary: LastRuntimeSummary.json saved.`, and `RAID SUMMARY` with `+ PT Config updated: No - TESTMODE active`; also retain the startup `TESTMODE ENABLED - No PT settings will be changed!` banner. Include any setting transition in the output without changing personal presets to force one. Confirm the former bare `symbol=USDT` invalid-symbol request is absent. If analysis is unavailable or stale, retain its diagnostics; a startup release preview is only expected after fresh conclusive analysis. `TESTMODE: startup global SOM preview; no PT API command was sent.` and the equivalent release preview are simulations, not native PT acknowledgements.

### A. Normalized data, history, and correlation

1. Exercise representative 1h/4h/24h trends with the selected metrics and sufficient configured retention. Check HistoryRequirements against the selected duration/lookbacks, current UTC alignment, configured capacity, and actual valid observations.
2. Include deliberately insufficient history. The affected values must be unavailable with clear reasons; sufficiently supported independent metrics must remain usable.
3. Confirm CorrelationToBTC, MeanCorrelationToBTC, and MedianCorrelationToBTC names, unitless values, timestamps, population counts, and coverage in MarketTrendAnalytics, trigger evaluation, and Monitor.
4. Check missing BTC history, missing asset history, constant returns, and an asset outside the global MaxMarkets cap. Missing values must not be replaced by zero correlation.
5. Check that Concentration uses the selected trailing volume window and the same normalized endpoint as the return; it must reject an incomplete eligible ranking population.
6. Observe a cold refresh that crosses a five-minute close. Its request/evaluation pin and earliest required reference must agree; the next raid advances normally.
7. Exercise a deliberately slow or delayed raid. An expired pin must prevent normal publication and keep any startup guard. A legitimately complete multi-hour bar is not stale solely because its own close is older than five minutes.
   Include a configuration using only volume, age, or time conditions: it still requires completed raid analysis and a fresh runtime pin before normal configuration delivery.
8. Repeat relevant migration checks on Binance Spot and Binance US when configured, and perform a real non-USDT Fiat conversion case with synchronized quote/USDT observations. The prior USDT identity case does not close that item.

### B. Repeated-raid selection and startup simulation

1. Begin with a known non-default confirmed identity, then produce an indeterminate raid. Check that selection, pending delivery, and confirmation are not mislabeled as DEFAULT application.
2. With startup protection enabled, verify the simulated global SOM enable occurs before slow exchange bootstrap. Assert that startup guard acquisition does not send a PAIRS/DCA/INDICATORS payload or change explicit pair properties.
3. Keep the raid indeterminate or stale, then make it fresh and conclusive. Confirm simulated ordering: global SOM enable, analysis, normal global/SMS configuration acknowledgement, then global SOM release. TestMode must call neither the SOM API nor the normal write transport.
4. Activate an SMS, then make its OffTrigger true while its activation is false. Verify an empty active SMS set is retained across a subsequent raid and the desired payload no longer contains its override.
5. Exercise missing MarketTrend references in global activation, SMS activation, and SMS OffTrigger via actual load/reload. Structural validation must reject them with useful context.
6. Preserve deliberate unknown/disabled/wrong-scope metric diagnostics. They should warn and resolve unavailable; NOT unavailable must not become true.
7. Verify opt-out separately from pending-guard recovery. With StartupSellOnlyMode=false and no owned pending marker, do not issue a new guard command; with a matching pending marker, complete recovery. An indeterminate startup must not publish a forced DEFAULT configuration in either case.
8. Make an existing ordinary SMS activation unavailable, including missing/future age or nonfinite/negative volume observations. It must remain active. Final unavailable SMS activation/OffTrigger expressions must keep initial selection indeterminate; conclusive true/false masking must still work.
9. Reload a changed setting definition or preset under the same name. The current definition must be compiled and the changed payload delivered/retried according to acknowledgement state.

The passing deterministic lifecycle harness uses controlled transports and failures for repeated raids, failed/partial delivery, retry, and checkpoint transitions. The configured runtime confirms integration with the actual configuration and observed data; real PT acknowledgement remains a separate step.

### C. Actual PT acknowledgement and failure recovery

TestMode deliberately prevents these observations. Record this gate as pending until the user conducts the controlled non-TestMode PT integration check.

Verify acknowledgement for initial guard delivery, release to a conclusive normal configuration, final SMS removal, and unchanged desired configuration after a failed attempt. Verify that a failed or partial send does not advance confirmed state, that the next interval retries, and that returning to a previously confirmed desired payload after a partial failure still repairs every configured target.

For startup API acquisition failure, confirm no claim of protection and no lengthy exchange bootstrap in that failed raid; the next interval retries. Verify the endpoint is resolved beneath each configured Monitor URL, including its path prefix, and uses the appropriate primary or additional API token without exposing that token in logs/history.

Observe global SOM=true before bootstrap. Per the user's native PT clarification, new buys and DCA buys must be stopped while sells remain allowed. Compare the existing PAIRS/DCA/INDICATORS before and after guard acquisition: this request must leave those sets unchanged. A compiled list or a successful request log alone does not establish native enforcement.

For a fresh conclusive raid, inspect the normal configuration acknowledgement before the enabled=false request. Rejecting or timing out the release must preserve the confirmed normal configuration and expose pending guard release. A subsequent fresh conclusive raid must retry release. Repeat with multiple PT targets and partial enable/release failures; per-target success must not be mistaken for complete success.

Verify the separate guard checkpoint at `_data/StartupSellOnlyModeState.json` and restart behavior after enabled or uncertain/pending release states. Confirm the ownership contract explicitly: StartupSellOnlyMode=true permits PTM to set global SOM=false after the release prerequisites even when the flag was already true before startup; the implementation does not claim to read or restore that prior value. StartupSellOnlyMode=false must not issue a guard setter merely to clear an untracked existing flag, but matching pending PTM-owned work must still be reconciled.

Failed/pre-bootstrap raids must remain visible in LastRuntimeSummary as well as their safe history record when services are ready.

Inject an intent-checkpoint write failure before enabled=true: no guard command or slow bootstrap may follow. A metadata write failure after a real API acknowledgement must be logged without falsely changing that acknowledgement to failure. Inspect StartupSellOnlyModeActive, StartupSellOnlyModePending, and StartupSellOnlyModeStatus separately from ConfigurationDeliveryStatus; a pending/uncertain release cannot be hidden by the last acknowledged active flag.

### D. Monitor browser preservation

Use at least two activation rows and two SMS OffTrigger rows on the same trend with different Metric/Tag values. Include full-precision thresholds, interleaved age/volume/time rows, unchecked checkboxes, and native property values.

Save without edits and compare parsed analyzer settings; then edit a second shared-trend row, add multiple rows/settings, remove one row, and save/reload. Confirm ordered identities, omitted/inactive fields, and untouched values. Formatting/comment preservation is not guaranteed by the existing JSON writer; semantic preservation is the criterion.

Load a page, change the underlying analyzer configuration separately, then attempt save. The revision check must refuse the stale overwrite. An incomplete AJAX section must keep save unavailable. Confirm correlation coefficients display without percent signs, history requirements remain visible, and status distinguishes selected from confirmed applied configuration.

ManageSMS uses the current mode's summary: SingleMarketSettingSummary.TestMode.json in TestMode and SingleMarketSettingSummary.json for live state. A reset request loaded before a mode change must be rejected. Verify that TestMode SMS inspection/reset cannot alter the live summary.

In General Settings, verify that the startup global SOM option and additional API token values save/reload correctly, including an unchecked option and empty extra-token value. Confirm that the UI communicates global-flag ownership and the native new-buy/DCA-buy/sell behavior, and that token-bearing URLs do not appear in logs or exported history.

Inspect the original Market Analyzer columns/graphs and historical continuity specifically. The form harness does not run a browser or Razor/JavaScript execution and cannot close those checks.

### E. Decision history

Inspect a normal raid, guarded raid, unavailable/stale decision, failed delivery, retry success, and TestMode record. Compare source/version, safe configuration/payload hashes, analysis/decision times, actual evaluated inputs and validity, selection, guard, and delivery outcome with corresponding logs.

Confirm the history never contains license/token values, raw general settings, raw PT payloads, or raw exception strings. Confirm segments rotate and oldest whole files are pruned under configured retention/quota in an isolated test directory. Confirm errors in history writing are visible without being mistaken for PT delivery success.

Do not treat a JSONL append as a checkpoint acknowledgement or a complete historical replay database. TestMode records must remain distinguishable and must not overwrite the real confirmed-delivery checkpoint.

## 5. Evidence to return and closeout rules

For the next configured TestMode run, provide startup and both consecutive raids' console/current-instance output, plus the current matching `$PtmRuntime/_data/LastRuntimeSummary.json` and `$PtmRuntime/_data/MarketTrendAnalytics.json`. Include `SingleMarketSettingSummary.TestMode.json` and matching DecisionHistory JSONL records if produced. Retain the source SHA, .NET version, and configuration identity with this evidence; the completed harness results need not be resubmitted. Add relevant checkpoint metadata and Monitor observations when conducting those later scenarios. Remove credentials from any shared deployment files; the history format itself is designed to omit them.

Record each scenario as pass, fail, or not run, with environment and source identity. Avoid one blanket “all validated” label when Spot/US, non-USDT, browser, or actual PT acknowledgement remains untested.

If a case fails, fix the implementation and rerun the directly affected checks plus any required regression gate. Do not broaden testing without a concrete remaining risk. Add a dated evidence update, then update STATUS and this handoff's successor.

## 6. Next development after acceptance

Continue the remaining metric program: raw derivatives, derivatives aggregates, higher-order market states, ongoing selection/Monitor integration, liquidity/depth/execution metrics, and full native historical analysis.

**Dedicated performance work starts only after all approved new metrics are complete.** Retain startup reconstruction, snapshot reuse, incremental calculations, log-volume improvements, and performance benchmarks in that later phase. The current correctness/retention fixes do not reopen an early performance project.

Personal strategy development, strategy repositories, preset tuning, and profitability evaluation are independent and excluded.

[Decisions](../DECISIONS.md) · [Issue 003](../issues/003-configuration-lifecycle-and-data-reliability.md) · [Implementation update](../updates/2026-11-07-stabilization-correlation-implementation.md) · [Current technical roadmap](../roadmaps/CURRENT.md)
