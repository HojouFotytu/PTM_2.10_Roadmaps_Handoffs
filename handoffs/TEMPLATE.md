# PTMagic 2.10 — Handoff: <checkpoint>

**Date:** <YYYY-MM-DD; record the timezone of runtime evidence separately>

**Application repository / branch:** HojouFotytu/PTMagic / phase1/market-data-foundation

**Source HEAD:** <exact SHA, verified from source>

**Execution provenance:** <exact tested SHA, or clearly state inferred/not run>

**Current roadmap:** [roadmaps/CURRENT.md](../roadmaps/CURRENT.md)

**Current decisions / status:** [DECISIONS](../DECISIONS.md) · [STATUS](../STATUS.md)

## User-approved scope and constraints

Record the requested changes and any deferrals. PTMagic application development is independent of personal trading-strategy projects. Performance work remains after all approved new metric additions unless the user explicitly changes that order.

## What changed and why

Describe resulting behavior and relevant public settings. Include migration or default-behavior changes. Link source commits and implementation records.

## Evidence

| Layer | Status | Evidence |
|---|---|---|
| Source implementation/review | <state> | <commit/files> |
| .NET application build | Not run / Passed / Failed | <actual output> |
| Deterministic harnesses | Not run / Passed / Failed | <exact projects and results> |
| Configured runtime | Not run / Passed / Failed | <exchange, quote, TestMode, binary identity, log window> |
| Actual PT delivery/application | Not run / Passed / Failed | <acknowledgement and readback evidence; distinguish simulation> |
| Monitor/browser | Not run / Passed / Failed | <specific page/action> |

A previous accepted baseline does not validate a subsequent code change. State any inference about deployed SHA. Do not infer financial or strategy outcomes from engine tests.

## Complete local PowerShell

Run from the PTMagic application-repository root. Include branch check, `git pull --ff-only`, exact `git rev-parse HEAD`, `dotnet build`, and all relevant existing/new `dotnet run --project` paths, with exit-code checks after each command.

Replace this instruction with the complete actual script before publishing the handoff. Do not retain removed historical test project names.

## Runtime verification

Specify required configuration shape, deliberate input/failure conditions, expected state transitions, logs/exports, and what remains unproven. TestMode suppresses PT writes and cannot prove actual application of properties. Use local fake transports for deterministic delivery failures; actual endpoint checks remain user-owned.

## Remaining issues and next action

List blockers separately from later feature work. Identify the next task only once and link the current status table.

## Ownership

D-021: assistant owns source review, implementation, regression authorship, and fixes. User owns builds, harness execution, and configured runtime checks. No automatic CI without explicit request.

D-022: each verification handoff includes complete local PowerShell and explicit runtime instructions.
