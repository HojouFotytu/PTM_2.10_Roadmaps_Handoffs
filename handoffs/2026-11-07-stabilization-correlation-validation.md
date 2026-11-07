# PTMagic 2.10 — Stabilization, correlation, and decision-history validation

**Date:** November 7, 2026

**Application repository:** HojouFotytu/PTMagic

**Branch:** `phase1/market-data-foundation`

**Application source checkpoint:** `839dc9afe785523ddc7e551cb610b47a6a8acc34`

**Current plan:** [roadmaps/CURRENT.md](../roadmaps/CURRENT.md)

**Current state:** [STATUS.md](../STATUS.md)

This is the sole current development handoff. Earlier dated handoffs remain historical. Begin with the actual application branch and source, then use the contracts and verification sequence below.

## 1. What is ready, and what is not yet accepted

The source implements the November 7 fixes and additions. Regression cases are authored. **The new build, harness execution, configured runtime, actual PT delivery, and Monitor browser checks have not been run in this session.**

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
| Diagnostic metrics | Unknown/disabled/wrong-scope metrics remain accepted warning-producing diagnostic inputs, not valid observations |
| Monitor | Ordered distinct rows, Metric/Tag, inactive fields, property types, and full precision survive save; stale revision refuses overwrite |
| Concentration | Top10 mean return minus remaining eligible mean return in percentage points; rank using the same TrendMinutes trailing volume window; min eleven and 100% coverage |
| Correlation | Asset CorrelationToBTC and global MeanCorrelationToBTC/MedianCorrelationToBTC; Pearson(simple returns), exact synchronized complete history, N=30 default, range 3–1000 |
| Correlation validity | No fill or shortened overlap; missing source observations or zero variance unavailable; exact selected population and 90% global coverage |
| History | Enabled by default; 30 days, 256 MiB total, 16 MiB JSONL segments under `_data/DecisionHistory/YYYY-MM-DD-NNNNNN.jsonl`; prune complete oldest files |

The user rejected the initial unpublished full-preset overlay. The current startup API call leaves PAIRS/DCA/INDICATORS unchanged. TestMode makes no SOM API calls or live checkpoint writes and cannot prove that the guard, normal configuration, or release reached ProfitTrailer. Enabling StartupSellOnlyMode assigns the global flag to PTM: a previously enabled global flag is still requested false after a successful startup cycle, because the setter contract does not expose prior-state ownership.

The history-requirement export distinguishes complete-period lower bounds from current-raid slots and all-alignments retention. Default 24-hour trends have conservative StoreDataMaxHours guidance of 384h for ATR(14), 528h for VolumeExpansion(20), and 744h for Correlation(30). It warns on insufficiency rather than silently extending retention.

## 3. Required local build and regression commands

Run this entire block in **PowerShell from the PTMagic application repository root**, not the documentation repository. It stops on a wrong branch/source, missing project, failed pull, build error, or failed harness. The exact SHA must match the published handoff; a later source revision needs its own recorded identity and results.

The script does not launch the configured application or change TestMode.

Review the printed working-tree status. Local source changes must be recorded with the build's -dirty identity and cannot be reported as the clean checkpoint. Private configuration/preset differences are identified separately by the recorded configuration and payload hashes.

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
$ExpectedSource = "839dc9afe785523ddc7e551cb610b47a6a8acc34"
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

### Authored case inventory

These are expected source counts, not reported passes. Preserve each harness's actual output.

| Project | Case groups/checks expected | Current execution status |
|---|---:|---|
| Phase1AReadiness | 5 | New source rerun pending |
| Phase1COhlcv | 13 | New source rerun pending |
| Phase1SmsSummaryIsolation | 5 | New source rerun pending |
| Phase1TriggerLogic | 29 | New source rerun pending |
| NormalizedPriceTrendMigration | 18 | New source rerun pending |
| Phase1MetricWarnings | 18 | New source rerun pending |
| Phase1AnalyticsReliability | 16 | Authored; unexecuted |
| Phase1DCorrelation | 21 | Authored; unexecuted |
| TriggerConfigurationValidation | 38 | Authored; unexecuted |
| MonitorSettingsRoundTrip | 28 | Authored; unexecuted |
| ConfigurationLifecycle | 56 | Authored; unexecuted |
| DecisionHistory | 13 | Authored; unexecuted |

The authored inventory is 260 checks/groups across twelve projects. This is an expected inventory, not a passing total.

No removed selective-legacy project belongs in this sequence. Do not substitute an old total for the output of these current projects. Existing warning counts may change; capture warnings and failures accurately.

## 4. Runtime acceptance after deterministic checks

Use a configured deployment built from the exact recorded source. Confirm `GeneralSettings.Application.TestMode=true` before the initial runtime phase. Use application-owned neutral diagnostics; personal strategy presets and results are outside this task.

For a source checkout already configured with its required settings and presets, the application starts from the repository root with:

```powershell
dotnet run --project PTMagic/PTMagic.csproj
```

A configured deployed installation may use its existing startup command instead. Record which binary/source was actually launched. Do not assume that building a checkout replaced a separately deployed binary.

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

The deterministic lifecycle harness uses controlled transports and failures. It must cover repeated raids, failed/partial delivery, retry, and checkpoint transitions; the configured runtime confirms that orchestration calls those production paths.

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

Provide the console output with source SHA and .NET version, actual per-harness results, relevant raid logs, and the matching MarketTrendAnalytics, LastRuntimeSummary, SMS summary, history/checkpoint metadata, and Monitor observations. Remove credentials from any shared deployment files; the history format itself is designed to omit them.

Record each scenario as pass, fail, or not run, with environment and source identity. Avoid one blanket “all validated” label when Spot/US, non-USDT, browser, or actual PT acknowledgement remains untested.

If a case fails, fix the implementation and rerun the directly affected checks plus any required regression gate. Do not broaden testing without a concrete remaining risk. Add a dated evidence update, then update STATUS and this handoff's successor.

## 6. Next development after acceptance

Continue the remaining metric program: raw derivatives, derivatives aggregates, higher-order market states, ongoing selection/Monitor integration, liquidity/depth/execution metrics, and full native historical analysis.

**Dedicated performance work starts only after all approved new metrics are complete.** Retain startup reconstruction, snapshot reuse, incremental calculations, log-volume improvements, and performance benchmarks in that later phase. The current correctness/retention fixes do not reopen an early performance project.

Personal strategy development, strategy repositories, preset tuning, and profitability evaluation are independent and excluded.

[Decisions](../DECISIONS.md) · [Issue 003](../issues/003-configuration-lifecycle-and-data-reliability.md) · [Implementation update](../updates/2026-11-07-stabilization-correlation-implementation.md) · [Current technical roadmap](../roadmaps/CURRENT.md)
