# Live level pipeline: architecture and failure modes

How to keep a charting-platform indicator fed with living levels without a human, and every way it broke.

## Architecture
```
data feed (1 s poll)  →  watcher  →  handoff file  →  stager  →  deploy daemon  →  chart
                          confirms a move twice,     bakes the map into the      pastes the script in the platform's
                          quarantines degenerate      script's input defaults     editor, saves, verifies the legend,
                          maps, writes {at, moved,    (also bakes frozen cards    dedupes instances, saves the layout,
                          levels}                     from the fire ledger)       screenshots every minute
```
- The chart instance pins to a script version: save is not deploy. Level pushes only land on the editor-linked instance.
- One visible browser owns the platform session; every tool attaches to it over the debug port. Two sessions fight over the layout.
- Pushes happen only in the cash-session window, throttled to one per 8 minutes unless a level moved 60+ points.

## Failure modes met, and the guard each one earned
| Failure | Symptom | Guard |
|---|---|---|
| Closing-solve echo | zero gamma equals spot, walls a few points apart, netGEX nonsense | Quarantine when zero == spot or the three majors sit inside 25 points; keep the last clean map |
| Stale handoff at Monday open | The window-open push staged the weekend echo | Handoffs older than 15 minutes fall back to the live tick, and the stager applies the degenerate rule to the final map, live or handoff |
| Combined-map collapse | Watcher passed two halves of a map in separate ticks; the combination had a 5-point spread | The collapse rule runs on the combined map at stage time, not per tick |
| Push hangs | Alerts step waited on 30-second locator timeouts until the whole push timed out; each timeout reloads the chart and can drop the instance | Bound every UI step; treat alerts as optional; never let a synchronous shell call block the event loop (a hung clipboard call froze the daemon for two hours) |
| Collapsed indicator legend | Rows have zero size; every hover control "does not exist" | Expand the legend before touching rows |
| Editor on the wrong tab | "Historical version" or an empty Untitled tab; saves silently return the same version | Verify the tab title, detect read-only banners, restore the version |
| Instance removed by dedupe | The new instance never appeared, the old one got removed, the layout autosaved without it | Only remove after the new version is confirmed on the chart; never save a layout that lost a study |
| Recompile wipes live cards | Every level push erased fired signals | Fire capture through status-line values, filed to a ledger, baked back as frozen cards |
| Duplicate instances after failed saves | A pinned copy plus a fresh linked one | Dedupe keeps the highest version; the fix path is remove-by-selection plus a layout save with a server timestamp check |

## Verification habits
- After every deploy: one instance, the dependent study still present, legend values equal to the staged map, layout timestamp moved.
- Read the full log for the paste and the version bump. A "compile clean" line without a version bump means nothing deployed.
- Screenshot the live window and look at it.
