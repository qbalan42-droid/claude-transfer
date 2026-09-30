# Asia OTE: the resting-limit strategy

Source: a public YouTube walkthrough by the trader "Aval" (Mind Over Market), "This Asia Session Strategy…", September 2026. The rules below are his, distilled; the implementation choices are ours.

## The rules, as taught
- **Why Asia**: the New York session stopped delivering over the summer; the moves came overnight. Asia open is 8:00 PM ET.
- **The tool**: a Fibonacci over a range. 0.705 is the entry (OTE). 0.79 is where the stop goes, just beyond. 0.5 is equilibrium.
- **Which range**: bearish, top to bottom; bullish, bottom to top. The prior session's range (New York cash), or the Asia range as it forms. Bigger ranges react best.
- **Direction**: the narrative from the 15-minute and 1-hour structure; look left for the draw on liquidity. Never counter-narrative even if the fib lines up.
- **Entry**: a limit exactly at the 0.705, sometimes a hair shy to guarantee the fill. No trigger candle.
- **Stop**: beyond the 0.79 and beyond a nearby 5-minute candle or gap.
- **Target**: an unfilled 15-minute fair value gap or the session high or low being drawn to. Bodies, not wicks.
- **Confluence**: OTE plus a 15-minute or 5-minute fair value gap is "much stronger than a stand-alone OTE". Also sweeps, session highs and lows, order and rejection blocks.
- **Management**: no instant breakeven at the level. Trail once it moves; partial at inner liquidity, runner to the draw. 2R base, up to 8R.
- **Invalidation**: price beyond the 0.79 and lingering.

## Our implementation
- Two ranges watched every night: the NY cash session frozen at the close, and the Asia range as it builds. Each places at most one limit per night; one limit rests at a time; when both qualify, the one price can reach first.
- The limit is **placed on the mechanics alone**: narrative set (1H structure not flat), range at least 40 points, retrace not yet at the 0.705, at least 1.5R to the draw. The grade sizes the order; it does not gate it. A grade gate here produced zero placements in a week while the method fired every night.
- The card draws grey from the cash close ("planned, rests at 20:00 ET"), gold when it rests, blue when it fills, and stays as the record. It is pulled at the window's end, on a narrative flip, or when price closes through the 0.79 first (that range is then done for the night).
- An Asia-range limit follows the range as it builds; the placed grade never changes.
- The stop is set at the fill: beyond the 0.79 and beyond the last five minutes' extreme, whichever is further.

## The grade (sizes it, does not gate it), max 10
Base mechanics 3 · 4H agrees with 1H 1 · 15-minute gap on the limit 2 · range over 100 points 1 · over 2R to the draw 1 · range extreme swept the prior session's extreme 1 · 0.705 within 8 points of the last 1H swing 1 · limit on value 1 · unfilled 15-minute gap between limit and draw 1.

## What the replay said before shipping
Five nights, one rule, no cherry-picking: one fill in three tradable nights on the NY-range version, and it paid (equilibrium banked, runner to the high). That is evidence the mechanics behave, not evidence of an edge. The forward record decides.

## Nights on record so far
Three placements filed, zero fills: two sells that never got their retrace, one buy pulled when the 1H flipped. A resting limit that does not fill is the strategy working, not failing.
