# PTMagic 2.10 Monitor — PT Data live pagination handoff

> **Superseded implementation checkpoint — November 17, 2026:** This file records historical November 13–15 behavior, not active Monitor acceptance or current code. The [current effective Monitor contract](../CHANGELOG-2.10.md#november-17-2026--monitor-current-behavior-and-acceptance-boundary) and [current decisions](../DECISIONS.md#november-17--effective-monitor-decisions-supersede-conflicting-november-1315-instructions) take precedence. PT Data is **schema 1.3** (PT's pages 1-based, 26/26 simulated CI PASS, real 1.3 acceptance still pending), not the older schema-1.2 repeated-page failure. All already-published per-asset metrics display irrespective of trigger/configuration/scope; the full-version tooltip uses the stamped `BuildIdentity.CommitBuildNumber`, not `PTMagic.dll ProductVersion`; Logs replay startup before raid 1 when no previous raid exists and provide complete PTMagic+Monitor log ZIP. Independent Monitor pages start before the first raid; dependent views show the Logs-linked wait message and retry once per minute. No application or strategy changes in this documentation entry.


**Date:** 2026-11-15 (KST). **Status: P1 BLOCKER, live multi-page Buy/Sell History NOT WORKING.**
**Authority:** This document supersedes the *PT Data export status and next steps* in `2026-11-15-monitor-5.md` and `2026-11-13-monitor-performance-export-design.md`; those retain historical design and unrelated Monitor topics. It does not supersede the separate Dev 9 analytics handoff.
**Application:** [PTMagic `phase1/market-data-foundation`](https://github.com/HojouFotytu/PTMagic/tree/phase1/market-data-foundation). **Exporter implementation:** [`3c7eddd9d4ce8694140c6210344253afef8eb41e`](https://github.com/HojouFotytu/PTMagic/commit/3c7eddd9d4ce8694140c6210344253afef8eb41e). Later inspected branch HEAD `77f5bbc4116cf18b663af6722107dd31e7933b9e` contains unrelated diagnostic TestMode analyzer commits `4645ab4` and `77f5bbc`; no later PT Data exporter change found.
**Documentation:** `HojouFotytu/PTM_2.10_Roadmaps_Handoffs` / `main`.
**Scope:** `Control → PT Data` only: read-only ProfitTrailer history collection, ZIP, and manifest. Do not modify Analyzer, DEFAULT settings, DCA strategies, TPS flags, unrelated Monitor UI, or external bot configuration.

## Executive state (do not misreport)

- **Fixed at source and verified offline:** Old schema-1.1 exporter (`618b628`) failed buys/sales with opaque `invalid_or_oversized_data`. Replacement [`3c7eddd`](https://github.com/HojouFotytu/PTMagic/commit/3c7eddd9d4ce8694140c6210344253afef8eb41e) uses small pages, preserves raw API responses and partial successful records, and returns specific error categories. [.NET 10 GitHub Actions](https://github.com/HojouFotytu/PTMagic/actions/runs/43665987850) **PASS: all 20 HTTP→JSON→ZIP simulated tests, Monitor Release build with 0 warnings and 0 errors**. These test an emulated PT API and do **not** establish real PT page advancement.
- **Verified on live exported PT data, still broken:** User-supplied `PT-Data-GeorgeLong-2026-11-15T03-00-33Z(2).zip` (actual manifest `exporter_version: paged-json-v2`, schema `1.2`, `history_range: all`) contains **10 buys and 10 sales**, then stops because each second raw response is byte-for-byte identical to the first. Both datasets have `status: partial`, `error_code: history_page_repeated`, `failed_page: 1`, `range_coverage_complete: false`.
- **Actual root cause still OPEN:** The archive proves PT API responses obtained at successive requested page numbers are identical. It does **not** establish whether PT ignores `page`, whether query parameter names/serialization/casing are wrong, whether backend pagination behaves differently, or another reason. Do not claim an API bug or a working fix without independently checking real PT requests.
- **Not oversized in this evidence:** 180,843 bytes per buy page and 120,514 bytes per sell page; page-size reductions = **0** for both. This is a **pagination/progress issue**, not proof of response size failure. Do not revive the generic error label.

## Confirmed ZIP evidence — 2026-11-15 03:00:33 UTC

Instance `GeorgeLong`; ZIP CRC integrity and all 11 JSON members checked. `manifest.json`: `overall_status: partial`, 4 available, 2 partial, 0 failed, funding skipped. Export duration ~0.19s; this is not a performance benchmark.

| Dataset | Manifest status | Actual rows | Data/diagnostics |
|---|---|---:|---|
| `Trades/buys.json` | partial | 10 | Exact first-page records retained including nested `extraInfo` |
| `Trades/sales.json` | partial | 10 | Exact first-page records retained including nested `extraInfo` |
| `CurrentPositions/pairs.json` | available | 29 | Raw snapshot |
| `CurrentPositions/dca.json` | available | 1 | Raw snapshot |
| `CurrentPositions/watchmode.json` | available | 0 | Raw snapshot, empty is valid |
| `CurrentPositions/pending.json` | available | 0 | Raw snapshot, empty is valid |
| `Funding/funding-updates.json` | skipped | — | Not selected |

For **each** of buys and sales, both files `Trades/{name}-pages/scan-00-page-00000.json` and `...page-00001.json` have the same bytes, including the `{hashcode,data}` envelope and 10 rows:
- Buys: 180,843 bytes/page; identical SHA-256 `a019deeecfaa01ab46d95d1e9aa6525745b7bd7f024de02417d7232a47022269`.
- Sales: 120,514 bytes/page; identical SHA-256 `26dbef49d97dd2744620bcc511aedb4fd9e10f4019696cc284a201a1f052259d`.
- `pages_retrieved: 2` is two **responses**, not 20 unique trades. `source_record_count: 10` and `included_record_count: 10` per history. Combined trade arrays exactly match first-page `data`. `duplicate_records: 0` is compatible with `history_page_repeated`, because the full-page repeat is rejected *before* individual rows on the repeated page are counted.
- This is George**Long** evidence; earlier November 14 schema-1.1 failures were from George**Short**. Do not conflate bot instances or revision-specific manifests.

## Historical source contract at `3c7eddd` (superseded exporter)

`Monitor/_Internal/PTDataExportService.cs`: GETs against the **configured PT target**:
- `/api/v2/data/buys?token=[REDACTED]&page=0&perPage=10&sort=BOUGHTDATE&sortDirection=DESCENDING`, then `page=1` (and onward).
- Sales analogous with `/api/v2/data/sales` and `sort=SOLDDATE`.
- On response size overflow only: reduce `perPage` **10 → 5 → 2 → 1**, restart pagination at page zero, deduplicate **exact record content**. This reduction was **not triggered** by the latest ZIP.
- Handles bare JSON arrays and `data`/`content` wrappers, saves unmodified raw history pages to ZIP, and aggregates dated trade records to `Trades/buys.json` and `Trades/sales.json`; selected UTC date windows remain `7d`, `1m`, `3m`, `6m`, `all`.
- Stops/report partial on repeated page, malformed JSON, HTTP errors, timeout, or other explicit errors; successful earlier rows remain available. Do not treat `status: partial` as successful complete history, and never infer that PT has only 10 trades.
- `range_coverage_complete` is a bounded exporter determination, not proof of complete retained/lifetime PT history. Current positions remain point-in-time snapshots; optional funding remains off by default.
- HTTP access is read-only with the configured API token, password-protected Monitor, no PT write operations or automatic external upload.

## Evidence and chronology — revision-specific

1. **Nov 13, schema 1.0:** Original first-response exporter included 23 buys/25 sales; confirmed PT connectivity and nested historical CV data, **not** complete multi-page coverage.
2. **Nov 14, `618b628`, schema 1.1:** Added date-window pagination at `perPage=25`; GeorgeShort `7d` and `all` ZIPs failed buys and sales with `invalid_or_oversized_data` while positions succeeded. Specific validation failure unobservable.
3. **Nov 15, `3c7eddd`, schema 1.2 (`paged-json-v2`):** New exporter; simulated 20/20 PASS and native Monitor Release build PASS in [workflow 43665987850](https://github.com/HojouFotytu/PTMagic/actions/runs/43665987850). Distinguish **synthetic/fake HTTP** from native PT behavior.
4. **Nov 15 GeorgeLong live ZIP:** Source-deployed replacement proven by manifest; **both real history page 1 responses repeat page 0**, resulting in only 10 records each and explicit partial status. Real multi-page acceptance FAIL. Latest source branch `77f5bbc` has no subsequent exporter fix.

## Historical November 15 schema-1.2 investigation order (superseded by 1.3 source)

1. **Verify raw PT pagination behavior:** Using the configured instance, inspect the precise actual HTTP requests (safe logging of path, parameter names, page index, per-page value and HTTP status; never token/URL-with-token). Compare GET page 0 versus page 1 for buys and sales directly, with identical sort, date scope and page size. Check the real PT Swagger definition for **exact parameter spelling/case** (`page`, `perPage` versus other accepted names), zero-based indexing, supported sorts, and any PT-specific pagination semantics. Screenshots documenting parameters are earlier evidence of declared API support, **not** live proof of advancement.
2. **Classify whether the problem is client query construction or PT backend behavior.** Compare independent API results for 0/1 requests. Do **not** automatically widen page size, paginate by inferred trade IDs, use unverified endpoints, or silently mark complete. Inspect source/response only on the read-only authenticated path.
3. **Make the smallest source correction supported by the observed behavior.** If backend ignores the paging parameter, investigate supported alternative retrieval and termination semantics explicitly rather than trusting the 20 simulated tests. Preserve every nested `extraInfo`, `BUYNOTE`/`SELLNOTE` and historical transaction-time `CV`, and preserve partial export if pagination cannot progress.
4. **Focused verification:** Test whatever actual bug is found against real-response-shaped fixtures + ZIP manifest output, then build .NET 10 and inspect actual live GET page 0/1 and export. For success require **different valid page contents**, >10 distinct trades (when PT has >10), no skipped/repeated transactions, correct UTC range, and unchanged positions. Report live acceptance only after direct PT evidence.
5. If API cannot page at all, **document limitation plainly** and leave manifest partial rather than misrepresenting first 10 as all records.

## Boundaries / continuity

- **Do not implement `/api/v2/data/misc` Account Information yet.** That deferred option is described in `2026-11-15-monitor-5.md`; history retrieval takes priority.
- Do not expand the export into PBL, automatic strategy archives, or combined LONG+SHORT without a separate decision.
- Keep the independent analytics roadmap/35-metric implementation and personal trading-strategy files out of this Monitor export task.
- User-directed workflow: preliminary design analysis, **proportionate actual HTTP/JSON/ZIP testing**, minimal unrelated testing, no new branch; **explain any GitHub edits before committing**. Documentation here is for AI continuity; precise distinctions between implemented, simulated, and live-verified states matter more than editorial prose.
- Related links: [Monitor 5 historical handoff](2026-11-15-monitor-5.md) · [early export design](2026-11-13-monitor-performance-export-design.md) · [STATUS](../STATUS.md) · [ROADMAP](../ROADMAP.md) · [app exporter source](https://github.com/HojouFotytu/PTMagic/blob/phase1/market-data-foundation/Monitor/_Internal/PTDataExportService.cs).
