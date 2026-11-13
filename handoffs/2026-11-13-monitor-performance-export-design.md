# PTMagic 2.10 Monitor — Handoff: On-demand Performance Export ZIP

**Date:** 2026-11-13  
**Status:** Design handoff only — NOT implemented or runtime-verified  
**Application repository / branch:** [HojouFotytu/PTMagic](https://github.com/HojouFotytu/PTMagic/tree/phase1/market-data-foundation) / `phase1/market-data-foundation`  
**Application branch HEAD inspected for this handoff:** `5f09cd3d2da1bc87ccfca990170f7d24dc047767`  
**Documentation repository:** `HojouFotytu/PTM_2.10_Roadmaps_Handoffs` / `main`  
**Existing Monitor handoff:** [DashboardTop refresh resolved](2026-11-11-monitor-dashboard-refresh-resolved.md)  
**Current roadmap:** [roadmaps/CURRENT.md](../roadmaps/CURRENT.md) · **Status:** [STATUS.md](../STATUS.md) · **Decisions:** [DECISIONS.md](../DECISIONS.md)

## 1. Decision and objective

Create a **Performance Export** page inside the existing PTMagic 2.10 Monitor. On explicit user request, PTMagic obtains available ProfitTrailer (PT) records through its existing locally configured connection(s), adds relevant current configuration/runtime context, and delivers **one downloadable ZIP** for subsequent AI performance analysis.

This replaces the earlier idea of a continuously running external data collector, full analytics application, or giving ChatGPT unrestricted PT API access. **No AI-to-PT connection** is required or authorized. No scheduled export, upload, GitHub publication, strategy change, or trading action is part of the initial feature.

The desired workflow is: **Open Monitor → select bot/data scope → Generate ZIP → download locally → upload ZIP into an AI analysis conversation**. AI analyzes the records, compares them against LONG/SHORT strategies and GitHub development history, and *recommends* adjustments. The AI does not operate PT or deploy changes.

This handoff documents the requested feature; it does **not** change the currently approved implementation order in the PTMagic roadmap. Schedule its implementation deliberately within the Monitor/performance workstream.

## 2. Existing source context and boundaries

The inspected PTMagic branch has Razor Monitor pages including `BuyAnalyzer`, `SalesAnalyzer`, `BagAnalyzer`, `PresetFiles`, `Index`, and `_get/BuyList`. Secure page models already exist (for example, `Monitor/Pages/SalesAnalyzer.cshtml.cs` derives from `BasePageModelSecure`). `Core/ProfitTrailer/SettingsAPI.cs` implements **configuration delivery** to PT, including configured PT URL/license lists and retry behavior for 503 responses.

**Important:** an existing PT *settings-write* connection is **not evidence** that every requested *read* endpoint, pagination facility, record-retention period, or PT raw-property readback is already implemented. Audit the actual ProfitTrailer API and current PTMagic data caches before specifying endpoints or claiming complete coverage. Reuse existing configurations, clients and model/page conventions where suitable; add a narrowly scoped read/export layer only for confirmed sources.

Do not alter `DashboardTop`'s existing five-second refresh, the reverted experimental PBL count endpoint/caching arrangement, existing PBL/Positions behavior, chart/legend presentation, Analyzer selection, GlobalSettings/SMS decisions, or PT settings delivery logic. No new branches. No personal strategy files or Analyzer strategy edits.

## 3. Export datasets — initial proposed scope

Preserve the **original raw JSON payloads** whenever accessible, including full numeric precision, field names, notes and timestamps. Avoid lossy HTML scraping, rewritten values, or analytics-only summaries. Derivations can be added as separate clearly labeled data.

| Dataset | Intended content / interpretation | Availability caveat |
|---|---|---|
| **Buy history** | All available entry and DCA buy records; symbol, fill/transaction time, quantities, prices, fees and diagnostic notes/labels where PT records them | Verify endpoint, history pagination, retention and whether buy notes/CX/CY are returned |
| **Sell history** | All available sell records; time, quantity, proceeds, realized PnL, fees, sell notes/labels where present | Verify relationship between sell fills and earlier entry/DCA records; no fabricated joins |
| **Current PBL** | Current Possible Buys information, candidate eligibility and related readings where available | Point-in-time snapshot; not historical candidate evidence; don't introduce prior PBL count experiment |
| **Current PAIRS / open positions** | Open PAIRS positions, costs, quantities, unrealized performance and exposure | Point-in-time; distinguish raw PT response from PTMagic-calculated data |
| **Current DCA pairs** | Open DCA positions and recovery state, levels, costs, quantities and exposure | Point-in-time; do not infer historical DCA states |
| **Funding cashflows** | Actual settled funding receipts/payments, symbols, times and amounts where provided by PT or another already authorized source | Different from PTMagic's FundingRate/FundingSum **market metrics**; never substitute market metrics for actual account funding charges |
| **Current PT property files** | PAIRS, DCA, INDICATORS configuration, version/date/timestamp headers | Prefer effective PT-side readback if supported; otherwise label as PTMagic's generated/sent copy and explicitly mark readback unavailable |
| **Current PTMagic context** | Active GlobalSettings, SMS definitions, Analyzer configuration/selection and relevant data identity, when available without credentials | Sanitize aggressively; do not export wholesale general/application settings containing secrets |
| **Optional later** | Relevant logs, decision history, metric readings at activation, other PT datasets explicitly requested | Not initial requirements; add only after source/scope agreement |

**Bot scope:** support the current instance's PT target without guessing. LONG and SHORT must be separately identified. If one Monitor instance can securely access both configured bots, an optional combined ZIP may include both; otherwise each Monitor exports its own bot and the user can submit two ZIPs. Never silently treat a multi-license setting-delivery configuration as proof of multi-bot historical read access.

**History window:** default to **all records the selected source can actually return**, with optional 7-day/30-day windows when endpoint support permits. Be explicit about server-side truncation, pagination limits, timezones and earliest/latest available records. One export is not presumed to represent all lifetime trading activity.

## 4. CX/CY and analysis attribution

The strategy project's established label convention reserves:

- **CX = active PTMagic GlobalSetting**: LONG `GLnn` / SHORT `GSnn` / `DEFAULT`.
- **CY = active PTMagic SingleMarketSetting**: LONG `SLnn` / SHORT `SSnn` / `N/A`.
- PAIRS BUY/SELL and DCA have their **separate scope-appropriate CX/CY label definitions**. Labels are diagnostic/attribution metadata; the slots remain disabled as trading conditions.

These labels provide the **classified market/regime state**, not the full underlying metric values. They are valuable for grouping performance by GlobalSetting and SMS. Actual PT buy/sell API JSON must be inspected to confirm whether the labels survive into exported transaction records; a property definition alone does not prove that. Export the original transaction notes/codebook fields as well. Where a historical record lacks CX/CY, record that attribution as **unknown**, not current-state inference.

Current CX/CY or current Monitor selection cannot be retroactively assigned to an older trade. Buy/sell label values also do not reconstruct regime transitions during periods with no fills. PTMagic's already persisted decision/activation history may be useful later, but no continuous settings snapshots are required for the initial exporter.

The existing **unified LONG/SHORT diagnostic notes codebook** should be the downstream AI interpretation contract. Keep raw notes untouched so later codebook revisions can reinterpret them. Export metadata identifying a known codebook version if available; do not manufacture an unknown version.

## 5. Historical settings: GitHub is the preferred archive

**Do not continuously capture, duplicate or ZIP every historic Analyzer/preset/property revision.** The user's strategy repository [Hojou-PT-PTM-Strategy](https://github.com/HojouFotytu/Hojou-PT-PTM-Strategy) already has version-controlled LONG/SHORT DEFAULT, GlobalSetting and SMS development history. AI should use GitHub commit history and the settings' version/date/timestamp headers to compare configurations across time.

Crucial limits:

1. A Git commit or `SetTimestamp` establishes source/edit history, **not necessarily PT's actual activation time**.
2. A working/development file is not automatically the effective runtime file; distinguish working, archived and deployed versions.
3. PTMagic may have pending delivery, retries, missing acknowledgments or later manual PT changes. The current property snapshot can help audit differences but cannot prove the exact configuration of all prior trades.
4. When actual activation/deployment evidence is missing, mark the trade-to-version association as **approximate or unverified**, rather than claiming a precise match.

**Optional narrow future enhancement:** record **only on actual configuration changes/delivery** a tiny deployment event with UTC time, target/bot ID, Global/SMS IDs, effective property hashes/version metadata, associated source Git SHA *if known*, delivery/ack/readback state, and any uncertainty. No continual copying of Analyzer/properties files, no database requirement, and no GitHub write requirement. This is a provenance improvement to consider after the first exporter, not an initial dependency.

This separation is intentional: **PT export = trading/runtime evidence; strategy GitHub = historical strategy definitions**. Neither alone proves a deployed historical state without timing evidence.

## 6. Proposed ZIP contract (illustrative names; exact API mapping TBD)

```text
PT-Performance-YYYY-MM-DDTHH-mm-ssZ.zip
├── manifest.json
├── LONG/
│   ├── buy-history.json
│   ├── sell-history.json
│   ├── possible-buys.json
│   ├── pairs.json
│   ├── dca-pairs.json
│   ├── funding-cashflows.json
│   └── settings/
│       ├── PAIRS.properties
│       ├── DCA.properties
│       └── INDICATORS.properties
├── SHORT/
│   └── (same structure, only if this Monitor has confirmed access)
└── PTMagic/
    ├── analyzer-current.json
    ├── global-settings-current.json
    └── sms-settings-current.json
```

**Do not create fake/empty JSON and present it as successfully collected data.** Optional/missing datasets should be absent or unambiguously marked as unavailable in the manifest.

The `manifest.json` is mandatory and should be machine-readable, with at least:

- `schema_version`, `export_id`, export start/end timestamps **UTC ISO 8601**, timezone/offset metadata, PTMagic application version and verified Git SHA **when available**.
- Each selected bot's stable **nonsensitive** alias/role, source type, and data freshness/collection time. Avoid secrets, full authentication URLs, license IDs and machine-identifying details unnecessary for analysis.
- For each dataset: requested/available/failed/skipped status; internal ZIP path; raw/derived and PT/PTMagic provenance; collection timestamp; record count if valid; earliest/latest source timestamp if known; pages requested; completeness/pagination/truncation flags; source hash if useful.
- Each settings file's origin: confirmed PT readback vs PTMagic sent/generated copy vs local file; version/date/timestamp and content hash when known.
- Error codes/messages **sanitized** of credentials, query strings, tokens, URLs containing credentials, and raw exception contents that may disclose secrets. Never claim that a partially successful export is complete.
- Optional references to known repository/branch/revision and diagnostics/codebook versions, only if verified.

A **consistent, versioned manifest** is more important than prematurely forcing all source payloads into one custom analytics schema. Preserve raw responses alongside any later normalized results.

## 7. Monitor interface and processing

Add a dedicated **Performance Export** page under the existing Monitor navigation and styling, following the current secure Razor-page conventions. The initial UI needs only:

1. Source selection: this bot, or LONG/SHORT/both when confirmed reachable and correctly mapped.
2. Trade-history range: all available (default); optionally last 30/7 days.
3. Dataset checkboxes, with buy/sell always included; additional options for live positions/PBL, funding, current property files, PTMagic context.
4. **Generate / Download ZIP** action and a concise dataset-by-dataset result/error summary.

Server side: use the locally configured PT connection and whitelisted **read-only** operations; bound total execution time, concurrency, response size and paging, handle 429/503/timeout failures without affecting Analyzer raids or live trading. Retain a clear success/partial/failure manifest. Stream ZIP when practical, avoid holding unlimited history in memory, and clean up any temporary server files. Never expose an arbitrary URL/proxy or permit user-specified PT API paths. Browser download must be initiated by an authorized user action, not by background uploads.

**Authentication:** An export reveals sensitive trading/account information even without passwords. Enforce access control on the page and on the download/generation endpoint independently; don't rely on mere menu visibility or an optional public Monitor password setting. Use the existing secure Monitor infrastructure and standard request validation/CSRF protections; decide explicitly how to disable exports if the Monitor is not adequately protected. No direct link to unauthenticated ZIPs or persistent publicly reachable archives.

## 8. Security boundary — nonnegotiable

- PT password/license and exchange API keys remain inside the user's controlled environment and are **never** entered into ChatGPT, shipped to a new AI service, included in the ZIP, committed to GitHub, or placed in URLs/logs.
- Allowlist known read operations. No order placement, bot control, property POST, DCA change, sell/buy execution, or any PT write operation through the exporter.
- Sanitize exported configuration carefully: PTMagic general config can contain licenses, tokens, URLs, notifier credentials and other secrets. **Default deny** for unrecognized configuration fields; prefer a purpose-built permitted-field projection.
- Validate TLS and destination allowlists; do not copy a certificate-validation bypass from an unrelated settings-delivery path into the new exporter.
- Private trading data stays with the user until they **manually** choose to upload a sanitized ZIP to an AI conversation. The feature must not auto-publish performance archives to the public PTM documentation repository or private strategy repository.
- ZIP filename, manifest and error messages must not expose credentials or sensitive connection material.

**Threat model:** ChatGPT cannot access a privileged PT endpoint. The Monitor backend can, but never delegates its authority to AI, an arbitrary remote URL, or a public unauthenticated export route.

## 9. Performance-analysis purpose and output

The ZIP is meant for AI-assisted longitudinal reviews of **LONG vs SHORT** and successive strategies:

- Entry pathways and diagnostic notes; regime `CX` and `CY` grouping; trade count, win rate, net realized results and fees.
- DCA trigger/spacing/sizing outcomes; leverage versus actual exposure/margin; funding cashflows; open/unrealized risk and time-in-position.
- Current PBL/position context, clearly **not** historical PBL/position evidence.
- Comparison to versioned DEFAULT/Global/SMS definitions in GitHub; distinguish correlation from causality and note uncertain deployment boundaries.
- Proposed targeted changes with supporting trade evidence, expected side effects and tradeoffs. Never implement or send recommended changes automatically.

A user can submit one or multiple exports to AI for cross-period comparison. The exporter itself is **data packaging**, not a trading optimizer or score generator.

## 10. Implementation staging and verification

**Stage A — Source audit (before coding).** Inventory actual PT API endpoints, authentication, all-history pagination, fields for notes/CX/CY, funding *transactions*, live PBL/positions and config readback; inspect which fields PTMagic's data model already has and whether the raw payload remains available. Map source and correctness for each proposed ZIP member. Explicitly flag unavailable fields.

**Stage B — Minimal first implementation.** Add a secure Monitor page, read/export service and manifest. Start with verified buy/sell records, live position/PBL and readable current properties; add other verified endpoints (including settled funding) when available. No database, scheduled crawler or GitHub retrieval code needed.

**Stage C — Focused correctness/security checks.** Verify downloadable readable ZIP and schema, exact unmodified source payloads, pagination/window bounds, bot separation, source timestamps, errors and partial exports, credential redaction, secure endpoint access, no PT writes and no interference with DashboardTop/PBL/Analyzer. Test 429/503/timeouts using bounded fake transport; do not rely on uncontrolled broad synthetic campaigns.

**Stage D — User-run acceptance.** The user performs the local .NET build and a controlled Monitor/browser export on their own PT environment; inspect the ZIP/manifest for correct data and absence of secrets. Treat unrun checks as **NOT VERIFIED**. Follow established D-021/D-022 verification ownership and provide the exact PowerShell commands with any implementation handoff.

| Evidence layer | Current status |
|---|---|
| Feature requirements/design | **Documented** |
| Read-endpoint availability and semantics | **Not yet audited** |
| PTMagic implementation | **Not implemented** |
| Build / focused tests | **Not run for this feature** |
| Native PT/browser/ZIP acceptance | **Not run** |

## 11. Explicit non-goals and next action

Not in initial scope: external AI API integration, automated/scheduled review, direct ChatGPT API credentials, cloud publication, local historical-trade database, continuous settings snapshots, live-trading changes, new Analyzer regimes, replacement of GitHub history, and unrelated Monitor redesign.

**Next development action:** audit PT/PTMagic's real read-access capabilities and data shapes for the requested datasets; then implement only the supported secure on-demand ZIP exporter, showing unavailable components accurately in `manifest.json`. Do not proceed on assumptions about undocumented PT API endpoints or exact historical deployment attribution.

**Repository/change-management rule:** Before any PTMagic source or documentation GitHub change, explain the exact intended files, behavior and side effects. Do not create a branch or modify unrelated strategy/application code.
