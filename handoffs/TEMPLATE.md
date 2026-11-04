# PTMagic 2.10 — YYYY-MM-DD Development Handoff

**Application repo:** HojouFotytu/PTMagic  
**Branch:**  
**Last verified SHA:**  
**Source files reviewed:**  
**Target phase/task IDs:**

## Current state (verified versus reported)

## Work completed and commits

## Development and validation ownership (D-021 — required)

- **Assistant:** Source changes, code review, regression-test authoring and fixes for user-reported errors.
- **User:** Local .NET build, regression-harness runs and end-to-end PTMagic TestMode.
- **Joint review:** User supplies actual command output/logs; assistant diagnoses issues and commits fixes.
- **GitHub:** Source control, commits and roadmap/handoff documentation. Do not create or trigger GitHub Actions builds/tests without explicit user request.
- **Verification evidence:** State separately whether build, each harness, and each exchange TestMode was **passed**, **failed**, or **not run**. Never assume an authored test has been executed.

## Local PowerShell verification commands (D-022 — required in every future testing handoff)

Provide a **complete, copy-paste-ready PowerShell script** for the user to run in VS Code at the **PTMagic application repository root**. Always include `git pull --ff-only` followed by `dotnet build`, the **exact project paths** for all change-relevant test harnesses, and any new regression tests. Clearly identify required versus optional tests; update the commands to match the source at hand. Baseline example:

```powershell
git pull --ff-only
dotnet build
dotnet run --project Tests/Phase1SelectiveLegacy/Phase1SelectiveLegacy.csproj
dotnet run --project Tests/Phase1SmsSummaryIsolation/Phase1SmsSummaryIsolation.csproj
dotnet run --project Tests/Phase1COhlcv/Phase1COhlcv.csproj
dotnet run --project Tests/Phase1MetricWarnings/Phase1MetricWarnings.csproj
dotnet run --project Tests/Phase1TriggerLogic/Phase1TriggerLogic.csproj
dotnet run --project Tests/Phase1AReadiness/Phase1AReadiness.csproj
```

List additional TestMode/runtime steps, settings, snapshots or logs to inspect separately. Do not claim success before reviewing the actual user-run results.

## Test results / diagnostic files

## Known unresolved issues and hypotheses

## Architectural constraints / backwards compatibility

## Decisions made and still open

## Next exact steps, in order

## Validation gates before continuing

## Links to roadmap, status, issues and update notes
