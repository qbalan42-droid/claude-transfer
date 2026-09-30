# Signal engine methodology

How a level-based intraday engine is structured so that it is honest, measurable, and survivable. Written from a live system that fired nothing for three sessions, then was fixed. The families below are concepts; the implementation is the reader's.

## Families (the trades)
| Family | Trigger | Stop | Targets |
|---|---|---|---|
| **WALL fade** | Price pokes the Floor or Ceiling and closes back inside, in a long-gamma tape | Beyond the wall | TP1 = the first level in the way toward the Line; runner = the Line |
| **FLIP** | Price closes across the Line within 25 points of it | Beyond the Line | Next level in the path, at least 1.5R |
| **LINE REJECT** | From well below, price tags the Line and closes back under it, with the hour drifting down | Above the tag | 1.5R, no level inside it |
| **ASIA OTE** | The 0.705 retrace of the prior session's range in the direction of the 1H structure, placed as a resting limit at the Asia open | Beyond the 0.79 and the last five minutes' extreme | Bank half at equilibrium, runner to the range extreme |

## Grading: a 0 to 10 confluence checklist, not a prediction
Each family counts its own confluences: location on value (POC / value area), flow with the trade, tick extremes, exhaustion, divergence, a fair value gap on the level, higher-timeframe alignment, the day's gamma sign. A number the reader can argue with beats a "BUY" arrow. Every card shows its grade. Grades are frozen at fire time.

The gamma sign is a point, not a veto: in long gamma the fade earns one and the continuation loses one; in short gamma the reverse. This is the whole "regime picks the strategy" idea in one line of logic.

## Gates (what stops a fire)
- Session windows (the open, the afternoon, Asia). Trading the whole day is how discretionary systems bleed.
- Event blackout around scheduled prints (FOMC).
- Confirmed bar, live bars only. History preview re-grades old bars against today's levels; that is not a record.
- Cooldowns per family and a global one.
- **Never trade through a level**: the first level between entry and target becomes TP1; a level within 10 points of the entry blocks the trade until it is tapped.
- **Two attempts per wall per day.** The third fade at a corpse is not a trade.
- A wall that broke decisively this session stops being a fade candidate.

## The two lessons that cost three sessions
1. **A veto stack plus wide stops produces zero.** ATR stops at 39 points made every 1.5R target sit 60 points away through a dense map. Nothing qualified. The parallel shadow engine with 14-point stops fired eight times the same day with a real record. Stops were capped, and the trend and VWAP vetoes became grade points. The user's words: "I'd rather send signals and learn than none at all." A grade floor is a dial, not a religion.
2. **Every recompile wipes live cards.** The chart only draws live fires, and pushing new levels recompiles the script every eight minutes. Cards died before anyone saw them. Fix: the script exposes each fire's fields as status-line plot values; a daemon reads them every minute, files each fire once, and bakes the day's fires back into the script as frozen cards at their fire-time numbers. The chart engine now has its own ledger.

## Ledger discipline
- The record is the engine's own fires, captured as they happen, judged later at the levels live at fire time.
- Report R per trade next to win rate, always. A 70% column with 0.3R targets is a loss.
- Never backfill a fire that did not happen. Never curate.
- A separate server-side "shadow" engine can run on the live map for comparison, but it is a different engine and must be labeled as such.
