# PTMagic 2.10 — Dashboard refresh history and current state

**Recorded:** November 11, 2026 (KST)

## November 11 — Dashboard refresh investigation and current owner direction

**Current application branch:** `HojouFotytu/PTMagic`, `phase1/market-data-foundation`.  
**Inspected application branch head:** `27da292158687bc0bf1aa3b990d06f53237b42d9`.  
**Dashboard rollback baseline:** `438acbe8e40241cd190e45385dffbee5637b3eb8`.  
**Last full offline acceptance:** `fb94373d8928b681e3ebe1f7209bd1439db42e72`, 16/16 harnesses and 337/337 groups PASS twice. That acceptance is earlier than subsequent Monitor edits and the dashboard rollback; it is not current DashboardTop runtime acceptance.

### Dashboard/PBL state — fully rolled back

The owner directed a complete rollback of every Possible Buys/dashboard layout and count experiment. Current source files were checked against the baseline Git blobs:

| File | Current blob | Baseline blob | Result |
| --- | --- | --- | --- |
| `Monitor/Pages/Index.cshtml` | `520f94d549a6b5d728f3688e1e82a93cc1add582` | same | Exact match |
| `Monitor/Pages/_get/DashboardTop.cshtml` | `914f18da75ec44213e061fb5613d7af276e79b44` | same | Exact match |
| `Core/DataObjects/ProfitTrailerData.cs` | `c725ddba129ad8013be9b07c4f876086d244b091` | same | Exact match |

The separate `PossibleBuysCount` endpoint and async count cache are absent; the experimental dashboard test was removed. The original `BuyLog` zero-limit short-circuit is restored. Therefore `MaxDashboardBuyEntries=0` again hides the entire Possible Buys card, and the PBL getter does not fetch a new PBL response in that mode. The requested compact count card above full-width Positions is **not implemented**; that experiment was withdrawn.

The original DashboardTop jQuery `.load()` method, tooltip cleanup/initialization, and `.text-autocolor(false)` post-load call are present. No new local build or browser verification has been supplied after the rollback.

### Refresh defect — still open after rollback

The owner reports that the top dashboard remains stale (reported as 12 minutes since its last update), including PBL/Positions data. Restoring the PBL-related files to their pre-experiment blobs did **not** restore observed refresh behavior. The PBL experiment was therefore not the only possible cause.

Git history identifies the November 2 refresh rewrite:

- `ec19a5eff1e2389c638b6cd71435a525fb99a8f2` — `Optimize dashboard AJAX polling`: replaced the previous interval-driven DashboardTop polling in `Monitor/Pages/Index.cshtml` with a request-running flag and a one-shot timer scheduled only from the `.load()` completion callback; added `document.hidden` gating.
- `26ce2d80a66e392d389fff11a07cfd9ad3dc3260` — `Preserve active dashboard tooltips during refresh`: inserted `cleanupOrphanedTooltips()`, tooltip initialization and profit autocoloring in the callback **before** clearing `dashboardTopRequestRunning` and scheduling the next request.

The current `Index.cshtml` is byte-identical to the November 2 post-tooltip version at `26ce2d8`. Ticker tooltip preservation was implemented separately in `Monitor/Pages/_Layout.cshtml` and `Monitor/Pages/_get/TickerWidgets.cshtml`; those ticker changes are not the same code path as DashboardTop polling.

**Source-level risks, not runtime-confirmed causes:**
1. The current `.load()` request has no explicit timeout; if it never completes, the callback never schedules another refresh.
2. The next refresh is scheduled only at the end of the completion callback.
3. Tooltip cleanup, tooltip initialization, and autocoloring run before the request-running flag is reset and the next refresh is scheduled. An exception in any of those operations can prevent subsequent polling.
4. The `document.hidden` guard pauses refresh while the browser tab is hidden and triggers an immediate request when the tab becomes visible.

No runtime log, failed HTTP response, or browser trace confirms which failure path is occurring. Do not state that the ticker tooltip fix itself caused the dashboard failure.

### Current owner requirements for the next implementation

- The data in **Possible Buys (PBL)** and **Positions** must refresh. The entire dashboard does not need to be re-rendered if a narrower update is sufficient.
- Preserve the existing DashboardTop jQuery `.load()` request method unless the owner explicitly approves a different one.
- Do not reintroduce the experimental PBL count endpoint, async count cache, or custom AJAX replacement.
- Do not alter the separate ticker tooltip-preservation code as a side effect.
- Preserve existing PBL/Positions calculations and profit coloring.
- **Explain the exact proposed change, files, and scope before editing any files.** The owner specifically corrected the workflow after an attempted premature update.
- No implementation for this refresh correction has been agreed or committed. The current source remains the exact rollback state above.

**Next action:** review the November 2 callback-dependent polling path and propose the smallest change that keeps PBL and Positions refreshing while preserving the original `.load()` call and ticker tooltip behavior. Wait for the owner's review of the explanation before changing source.



## Monitor changes in this conversation that remain in source

- **Market Metrics History Requirements panel:** removed from the Market Metrics page; diagnostic calculations and history readiness behavior remain active.
- **Global Settings Log:** exactly two market-data columns, Market Trends and Market Metrics. All configured trends/metrics are listed. Trend coloring: positive PriceTrend green; otherwise referenced white and unreferenced gray. Metric coloring: unused gray, used white, used-and-TRUE green. No separate Activation Triggers column or TRUE/FALSE indicator text in the market-data lists.
- **Market-Wide Metrics page:** the 17 market-wide metrics are grouped into seven comparative columns with a separate uppercase white group-title row and gray metric-name row; all columns and header/value content are centered. The separate Per-Market Metrics table and metric calculations remain unchanged.
- **Global Setting header tooltip:** compact four-line maximum: instance, selected setting, Delivered to PT / Not Delivered to PT, and Startup SOM only when the acknowledged startup-enable flag is present. It is not a live PT SOM readback.

The user supplied a .NET solution build PASS (15.7s) and ConfigurationLifecycle **75/75 PASS** after the Market Metrics page-local formatting update. That run predates the final dashboard rollback and does not verify current dashboard refresh behavior. The build/test output did not print a source SHA. Live Monitor browser rendering of the Market Metrics styling and actual PT PBL count were not established by that run.

## Documentation authority

This report is the detailed evidence record for the November 11 dashboard discussion. Current implementation/evidence state is summarized in `STATUS.md`; next-step instructions are in `handoffs/2026-11-10-som-enable-only.md`; accepted owner direction is in `DECISIONS.md`. The old PBL attempts are retained here as history, not as current behavior.
