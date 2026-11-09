# PTMagic 2.10 — Reused configured runtime evidence (LONG and SHORT)

**Reviewed:** November 9, 2026 (KST)  
**Evidence window:** November 8–9, 2026, ending around 11:27 KST  
**Disposition:** **Partial configured acceptance; no new runtime execution requested or claimed.**

This review reuses the user's earlier PT/PTM performance submissions (`logs.zip`, `_logs.zip` / `_logs(1).zip`, and `_data.zip`) through their previously published analyses and reproducible decision-audit CSVs. The underlying original ZIP files were **not** re-opened in this review; log-line-specific claims not preserved in those records remain **unverified**, not assumed. This document does not substitute for direct evidence of PT API acknowledgement or a newly executed instance.

## Preserved evidence sources

- [SHORT diagnostic and original-input inventory](https://github.com/HojouFotytu/Hojou-PT-PTM-Strategy/blob/main/PERFORMANCE/SHORT/Short_docs/PT_PTM_SHORT_diagnostic_2026-11-09.md)
- [SHORT 358-record decision audit](https://github.com/HojouFotytu/Hojou-PT-PTM-Strategy/blob/main/PERFORMANCE/SHORT/Short_data/ptm_short_decision_audit_2026-11-08_to_09.csv)
- [LONG diagnostic and original-input inventory](https://github.com/HojouFotytu/Hojou-PT-PTM-Strategy/blob/main/PERFORMANCE/LONG/Long_Performance_docs/L-Performance-1_PT_PTM_Analysis.md)
- [LONG 117-record non-TestMode raid timeline](https://github.com/HojouFotytu/Hojou-PT-PTM-Strategy/blob/main/PERFORMANCE/LONG/Long_Performance_docs/evidence/L-Performance-1/L-Performance-1_PTM_Raid_Timeline.csv)
- [Application change from tested SHORT engine to subsequent source](https://github.com/HojouFotytu/PTMagic/compare/86c7d2b213bd979173a453a4c602c2777f3def7c...87b9eaa1c865e39d8fff6a657e1b332012be8c16)

## What the SHORT configured TestMode evidence proves

The SHORT DecisionHistory-derived CSV contains **358 records**, all `TestMode=True`, across two exact source revisions: **238** at `a0b375cc9b2db469a48a31b713385f35500cc763` and **120** at `86c7d2b213bd979173a453a4c602c2777f3def7c`. All 358 have blank `confirmed_global_setting`; delivery statuses are **282 TestMode unchanged**, **70 TestMode preview**, and **6 Deferred**. **352** records have `decision_fresh=True`, and **6** are not fresh. The six deferrals comprise five age/staleness events and one I/O failure per the original diagnostic.

For the latest exact source `86c7d2b`, **118/120** records are fresh; delivery statuses are **84 TestMode unchanged**, **34 TestMode preview**, and **2 Deferred** (one stale, one IOException). All 120 retain `TestMode=True` and blank confirmed setting. The consecutive records begun at **11:15:54** and **11:20:54 KST on November 9** (recorded **11:17:43** and **11:23:06**) have identical source/configuration identity, `DecisionFresh=True`, `SelectionIndeterminate=False`, `missing_trigger_inputs=0`, and `TestMode unchanged` with no confirmed PT setting. These establish repeated completed **decision-history cycles** on the latest tested engine; they do **not** replace an independent check of `RAID SUMMARY` lines or the corresponding `LastRuntimeSummary.json` writes.

The original SHORT diagnostic confirms the last `MarketTrendAnalytics.json` contains nine horizons, **250/250 global** and **717/717 eligible-asset** observations, and complete listed history capacity/alignment. `StoreDataMaxHours=100`, versus up to **88 hours** recommended. All **29** SHORT GlobalSettings were evaluated and nine specialists selected. Four older records show simulated startup-SOM active/pending while analysis was deferred; there is **no PTM-confirmed SOM command** in TestMode. PT logs independently recorded global SOM flag changes around November 8 23:01, but the initiator was unknown and those changes must **not** be attributed to PTM.

GitHub comparison verifies the present application revision `87b9eaa1c865e39d8fff6a657e1b332012be8c16` is **one commit ahead** of the tested `86c7d2b`, modifying only `CHANGELOG-2.10.md` and **three NLog configuration files**. The analyzer/selection/delivery engine code was unchanged. The saved recent SHORT evidence therefore supports that engine's configured TestMode behavior; the changed console highlighting requires separate visual acceptance.

The six SHORT deferrals did not produce confirmed PT delivery. This supports the observed protection against unintended TestMode writes. Source inspection independently confirms `SendGlobalSellOnlyMode` simulates in TestMode, configuration delivery is simulated, and live acknowledgement checkpoints are not saved in that mode. Neither the decisions nor a simulation can establish actual native PT acceptance.

## What the LONG configured runtime evidence proves

The LONG performance analysis includes **497 DecisionHistory decisions**, split into **380 PTM TestMode** and **117 PTM non-TestMode** records. On November 9, the 117 non-test decisions show **36 Applied**, **80 Unchanged**, **1 Deferred**, and **116 fresh**. At around 11:15 KST, the PT log noted configuration changes after PTM selected `GL11_RECOVERY_BROAD`, corroborating a real delivery path, but this is **not TestMode** evidence. PT's own trading mode was TestMode, independent of PTM's mode. The stale decision above 300 seconds correctly deferred setting publication.

LONG has nine trend horizons, **250/250** global metric coverage, adequate 100-hour history, and an observed source-to-PT configuration transition. Its 117-entry raid timeline has no source-revision or PTM-TestMode columns; it cannot independently establish exact source provenance or pretend those 117 decisions were TestMode.

## Acceptance matrix based on already-supplied evidence

| Requirement | Disposition | Evidence / explicit limit |
|---|---|---|
| Configured SHORT TestMode recorded decisions | **PASS for tested engine** | 358/358 TestMode decisions, including 120 at latest tested `86c7d2b`; analyzer/delivery engine unchanged at current `87b9eaa` |
| Repeated fresh SHORT decisions | **PASS for recorded decision cycles** | Two adjacent fresh records at 11:15:54 and 11:20:54 KST, with zero missing inputs; literal paired `RAID SUMMARY` lines not re-examined |
| TestMode leaves PT confirmation unchanged | **PASS for recorded state** | Blank confirmed setting in all 358 SHORT records; 0 recorded confirmed delivery |
| TestMode startup SOM is simulation | **Supported** | Four older SHORT deferred-preview records; source contract simulates; native PT flag writes cannot be proven or ruled out from this evidence alone |
| Normalized metrics and sufficient history | **PASS for recorded latest SHORT snapshot** | 9 trends, 250/250 global, 717/717 assets, 100h retention vs max 88h listed recommendation |
| Freshness/safety during overload | **PASS for observed deferrals** | Five stale deferrals and one IOException; no confirmation; LONG >300s also deferred |
| Correct exact compiled PAIRS main market and absence of bare `symbol=USDT` | **PARTIAL** | Functional USDT-M analysis and completed decisions; no direct paired `Analysis main market: USDT` / invalid-symbol log excerpts in the retained audit |
| Same-source `LastRuntimeSummary.json` and `MarketTrendAnalytics.json` persistence on both chosen raids | **PARTIAL** | Latest MarketTrendAnalytics inspected in prior diagnostic; paired file-write and RAID SUMMARY lines not preserved in retrieved audit CSV |
| Native SOM enable/configuration/release acknowledgement | **NOT TESTED here** | PTM TestMode deliberately avoids native writes; a separate non-TestMode PT acceptance gate remains |
| Monitor browser editor and SMS activation/off-removal | **NOT TESTED here** | SHORT desired SMS count was zero; no browser save/reload evidence; LONG live setting changes do not cover these scenarios |
| Current `87b9eaa` console magenta visual behavior | **NOT TESTED here** | Only NLog config changed since the newer SHORT run; static/build checks are documented elsewhere |
| Warm-start performance before/after restart | **NOT TESTED here** | Evidence of 756 compressed cache series, but no controlled two-startup comparison or equivalent post-restart metrics |
| Clean end-to-end runtime with no fatal errors | **NOT ACCEPTED** | SHORT missing GS01 file earlier and GS29 file lock on November 9 with warning storm; exact cause and safe deployed remediation unverified |

## Disposition and next actions

**Do not request a repeat of the 358 SHORT recorded TestMode decisions, the 117 LONG non-TestMode decisions, or their already-reviewed metric coverage to satisfy the same acceptance claims.** Record the demonstrated portions as accepted at their tested sources; keep the strict remaining gates explicit rather than upgrading a past TestMode simulation to live PT acknowledgement.

For the PTMagic 2.10 application roadmap, the next unresolved acceptance questions are (1) direct compiled-market/paired RAID SUMMARY and export evidence if obtainable from already captured artifacts, (2) the configured PT delivery/SOM and Monitor browser tests, and (3) separately noted cache restart and TestMode console-color visual checks. Previously observed temporary preset-file failures remain reliability defects to investigate; exhausted AWS Lightsail burst CPU credits explain the late-run slowdown, not the file-lock error. Once these are appropriately dispositioned, proceed with Phase 2 derivatives ingestion. No new instance, API request, or trading action was performed in this review.
