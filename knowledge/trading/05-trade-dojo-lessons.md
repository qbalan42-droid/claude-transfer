# Lessons from a GEX-based discretionary course

Distilled from a full read of a paid options-dealer-positioning course and its live sessions, written in our words. No course material is reproduced here.

## What they teach, in one paragraph
Read the gamma condition first. Positive gamma means mean reversion: fade moves back into value with a tight stop. Negative gamma means trend: trade continuation off the profile's steep edges. Levels come from the dealer map (call resistance, put support, the largest gamma strikes, the hedging volatility level) plus a few blind-spot levels. The entry model at a level is absorption: a control tap, cumulative delta diverging from price, then an imbalance in the order flow. Stop at the protected swing or a fixed distance past the imbalance. Target the next level. Never trade through a level; a level within ten points means wait for the tap. First tap is the best tap; two attempts maximum at any level. Base hits, small stops, lock out on a winning day.

## What it confirmed rather than changed
Their model matched the autopsy of our own losses almost line for line: fade only in positive gamma without drift, tiny stops, two attempts, take the base hit. Confirmation is useful. It is not a new edge.

## What was worth building natively, in order
1. Target clipping at any level or point of control in the way, plus the ten-point tap rule.
2. An attempt counter per level and a grade point for a fresh (first-tap) level.
3. An absorption trigger from lower-timeframe volume delta, forward-test only. (Blocked on our platform tier: sub-minute volume needs a higher plan.)
4. Steep-edge zones from our own time-at-price profile, as a server job.

## What was not worth building
- Their moving-average "magnet" line: the claim failed replication.
- A repainting envelope indicator: our drift and range-position gates already do its job without repainting.
- Their proprietary box indicator: a moving target with discretionary rules and known bugs.
- A subscription to their data vendor: our own map covers the same levels.
- Anything that copies their code. Our signals stay ours.

## The business side, read straight
The teaching is coherent and mostly conservative. The numbers are unaudited: "2K every day", "94%", "almost 100% when we get the level". The live sessions show strings of small losses and blown evaluations on highlight days. Take the discipline, leave the marketing.
