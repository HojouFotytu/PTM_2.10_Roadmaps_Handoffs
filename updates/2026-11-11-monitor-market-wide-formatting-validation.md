# PTMagic 2.10 — Market-Wide Metrics formatting validation

**Recorded:** November 11, 2026 (KST)  
**Application branch:** `phase1/market-data-foundation`  
**Inspected remote head during documentation:** `44dd757e29808eaa8662fbdf8a63835efb02378a` (documentation-only commit following the Monitor page correction)  
**Local source SHA:** Not printed in the supplied PowerShell output. `git pull --ff-only` reported `Already up to date`. Treat remote branch head as a reference, **not as independent source identity evidence from the test runner**.

## User-run offline results

| Check | Result |
| --- | --- |
| `dotnet build .\\PTMagic.sln` | **PASS**, 15.7 seconds |
| Core (`net10.0`) | PASS, 4.7 seconds |
| PTMagic (`net10.0`) | PASS, 0.6 seconds |
| Monitor (`net10.0`) | PASS, 8.9 seconds |
| `dotnet run --project .\\Tests\\ConfigurationLifecycle\\ConfigurationLifecycle.csproj` | **75/75 PASS** |
| Reported warnings/errors | None |

The 75 checks include `market-wide metric headers have two centered rows with clear hierarchy`, `zero dashboard buy rows still refreshes the complete PT PBL for the count`, `dashboard zero buy-entry limit preserves count above full-width positions`, `global ticker tooltip uses compact delivery wording and only conditional startup SOM`, and SOM enable-only controls.

This validates the solution build and the focused source-level regression checks after the latest page-local Market-Wide Metrics formatting correction. It does not provide independent evidence of actual CSS presentation in a browser: **uppercase white group titles, muted-gray metric labels, and centered column content still require visual confirmation in the running Monitor**.

The full offline 16-harness **337/337** acceptance at exact source `fb94373d8928b681e3ebe1f7209bd1439db42e72` remains separate and should not be restated as a new full-suite execution.

**Disposition:** latest Monitor formatting fix: **offline build / focused harness PASS**; browser appearance and live PT PBL agreement remain unverified. No repeat of the already passing focused checks is needed without a relevant source change.

[Status](../STATUS.md) · [Roadmap](../roadmaps/CURRENT.md) · [Active handoff](../handoffs/2026-11-10-som-enable-only.md).
