# Vendor claims and win-rate math

Every indicator vendor sells one number: win rate. This is how to read it, check it, and explain it in one breath.

## The arithmetic
Win rate is set by the target-to-stop ratio, not by edge.

| Target vs stop | Breakeven win rate | What one loss costs |
|---|---|---|
| 0.10× | 91% | ten wins |
| 0.25× | 80% | four wins |
| 0.50× | 67% | two wins |
| 1.0× | 50% | one win |
| 1.5× | 40% | two thirds of a win |

A trailing-band system with a tiny target posts 90%+ by construction. Expectancy per trade is `win% × target − loss% × stop`. Ask for that number, in R, before anything else.

## The optimizer trick
A dashboard that "backtests 144 settings and shows the best win rate" is a machine for producing the headline. The maximum of 144 noisy numbers is always high. Checked on NQ:
- Best in-sample dial at 0.5× target: 75%. Same dial forward: 64%, at breakeven.
- **Random entries** (coin flip at random bars) through the same optimizer: 88% in sample at 0.25×, 98% at 0.1×. The machinery makes the number, not the entries.
- 88.89% is 8 of 9. The 95% interval for 8 of 9 runs from 56% to 98%. A coin-flip system shows 8 of 9 on at least one of 144 dials 94% of the time.

## The replication recipe
1. Rebuild the described pipeline from the vendor's own page. State your parameter choices.
2. Free intraday bars (Yahoo chart API gives 60 days of 5-minute, 7 days of 1-minute).
3. Split 60/40. Pick the best setting in sample, score it out of sample. Report both.
4. Run the random-entry control with the same stops and counts.
5. Convert the best dial to dollars per contract: "risk $88 to make $9" ends the conversation.

## Other claims checked
- **"TRAMA(20) on the 90-minute is tapped 94% of days, never more than 3 days in 500"**: on 60 days of NQ, 68 to 75% of days, four gaps of 3 to 5 days. The tap rate falls with distance, so the far-away swing trade the claim supports is its weakest case.
- **"Backtests prove it"**: every backtest shown was chosen after the fact. The only proof that costs the seller anything is a forward record they cannot edit.

## What is worth taking from these products anyway
- A defined ratchet trail for a runner after the first target, stated on the card so it is management, not discretion.
- Expectancy in R next to win rate on every scorecard.
- Multi-timeframe structure as a read, which any system already has if it tracks 1H and 4H structure.
