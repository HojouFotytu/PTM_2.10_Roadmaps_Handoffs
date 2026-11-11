# PTMagic 2.10 — DashboardTop refresh resolution

**Date:** November 11, 2026  
**Application repository:** [HojouFotytu/PTMagic](https://github.com/HojouFotytu/PTMagic)  
**Application branch:** `phase1/market-data-foundation`  
**Current inspected application HEAD:** `f108cd1ab39c44103bed91d1899f90f86a830eb4`  
**Implementation commit:** [`de5ecc8c3b8ef81d1a6305beebd075185342e395`](https://github.com/HojouFotytu/PTMagic/commit/de5ecc8c3b8ef81d1a6305beebd075185342e395)  
**Current `Monitor/Pages/Index.cshtml` blob:** `6b953a2abdd8478b01644f1ea735361ce41343bf`

## Change

The DashboardTop AJAX completion callback previously called `cleanupOrphanedTooltips()` unconditionally. The helper is defined in `Monitor/wwwroot/assets/js/custom.js`; however, the shared layout uses the PTMagic version as the static asset cache key, so a browser can retain an older script that does not expose the helper.

The callback now checks for the helper before invoking it:

```javascript
if (typeof cleanupOrphanedTooltips === 'function') {
  cleanupOrphanedTooltips();
}
```

Only `Monitor/Pages/Index.cshtml` changed in commit `de5ecc8`.

## Behavior deliberately preserved

- The existing `$("#dashboardTop").load(...)` request and callback.
- The existing five-second DashboardTop refresh interval.
- The existing request-running guard and callback-driven rescheduling.
- Tooltip initialization after the DashboardTop response.
- Existing `.text-autocolor(false)` profit coloring.
- DashboardTop/PBL/Positions retrieval, calculations and rendering.
- DashboardBottom refresh.
- The separate ticker refresh and ticker tooltip-preservation implementation.

No timeout, watchdog, new endpoint, custom AJAX replacement, count cache, or layout redesign was added.

## Verification

### Local build

After pulling the fix, the user supplied this result:

| Project | Result | Time |
|---|---|---:|
| Core | PASS | 4.0s |
| PTMagic | PASS | 0.6s |
| Monitor | PASS | 9.6s |
| **Solution** | **PASS** | **15.6s** |

The local output did not include a `git log` line. The fix commit was the branch head at that point in the conversation; record the local execution as following the pull of `de5ecc8`, not as a separately printed SHA.

### Runtime

The user subsequently confirmed: **“The topdashboard is now refreshing properly.”**

The original browser console error was not captured. The missing-helper path was identified during source inspection; the user's post-fix runtime confirmation establishes that the observed refresh problem is resolved.

The current remote branch head is `f108cd1ab39c44103bed91d1899f90f86a830eb4`. Its current `Index.cshtml` blob still contains the guard. The commits after `de5ecc8` through `f108cd1` concern derivative symbol/service/cache implementation and tests; they do not modify `Monitor/Pages/Index.cshtml`.

## PBL experiment rollback remains in force

The separate Possible Buys count endpoint, async count cache and replacement AJAX experiment remain withdrawn. The original behavior remains: `MaxDashboardBuyEntries=0` hides the entire Possible Buys card. This refresh fix did not change that setting behavior and did not separately validate live PBL count parity against PT.

## Disposition

**DashboardTop refresh: resolved.** No further dashboard refresh implementation is pending. The prior [November 11 investigation](2026-11-11-dashboard-refresh-history-and-current-state.md) remains unchanged as a historical record of the pre-fix state and is superseded by this resolution.
