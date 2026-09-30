# GEX levels: the glossary and how they behave

Options dealers hedge what they sell. The aggregate of that hedging, by strike, is gamma exposure (GEX). Where it concentrates tells you where price gets pinned and where it gets pushed. These are the levels an intraday index-futures system is built on. Everything below is in the futures' own points (Nasdaq: NQ / MNQ), converted from the index chain with a basis.

| Level | What it is | How price behaves there |
|---|---|---|
| **Zero gamma, "the Line"** | The strike where dealer gamma flips sign. Above it dealers are net long gamma; below, net short. | Above: dealers sell rallies and buy dips, moves get dampened. Below: dealers chase, moves get amplified. Crosses of the Line are regime changes, not just levels. |
| **Call wall, "Ceiling"** | Largest positive gamma strike above spot. | Rallies stall into it in a long-gamma tape. In a short-gamma tape it can break and become support. |
| **Put wall, "Floor"** | Largest negative gamma strike below spot. | Mirror of the Ceiling. |
| **OI walls** | The same idea computed from open interest rather than volume: slower, structural. | Hold longer, move less; the tape respects them across sessions. |
| **Micro walls** | Fast intraday walls from volume. | Wiggle a few points all day. Useful as targets, never as triggers. |
| **Magnet** | The strike with the highest absolute gamma. | Price gravitates to it into expiry and in quiet tapes. |
| **Dark pool prints** | Large block levels reported off-exchange. | Institutional interest; reaction levels, not walls. |
| **Net GEX sign** | Sum of dealer gamma. | Positive: fade moves, walls hold, the Line pulls price back. Negative: trade breaks, walls are speed bumps. This one sign picks the strategy for the day. |

## The rules that came from living with them
1. **Levels are living.** Gamma moves as the chain trades; the map is re-solved every minute during the cash session. A level printed at the open can be forty points away by 10:30. Never trade a stale map; never pin a card to a level that has moved.
2. **A trade is placed on the levels current at fire time.** When the map moves later, the trade stands as placed. Nothing is re-graded after the fact.
3. **The closing solve is garbage.** Around the cash close the chain thins and the solver echoes spot: zero gamma equals spot, the walls collapse to within a few points of each other. Quarantine any map where zero equals spot or the three majors sit inside 25 points. Keep the last clean map instead.
4. **Monday mornings and roll weeks rebuild the chain.** Expect the map to swing for the first 30 to 60 minutes; re-push every 8 to 10 minutes and do not chase every wiggle.
5. **Contract roll changes every converted level by the new basis.** Nothing moved. Quarantine until the basis is confirmed.
6. **Regime is the first read.** Before any setup: which side of the Line, what sign is net GEX. A wall fade in a short-gamma tape and a Line break in a long-gamma tape are the two most common ways to lose.
