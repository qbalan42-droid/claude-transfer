# Research method

How to run a deep dive on a course, a vendor, a competitor, or a claim, and come out with something buildable.

## 1. Get the primary material, legally
- Courses and videos: read the caption tracks the player serves; never rip protected media. Public YouTube: use the transcript. Paid material on someone else's account: read only, take no actions on their account.
- Products: the public listing, the docs, the reviews (all platforms, with dates), the pricing page, the company's own disclaimers. Disclaimers are where vendors tell the truth.

## 2. Extract, don't paraphrase
- Rules with numbers and timestamps: "stop at protected high or 10 pts past the imbalance [14:11]".
- Worked examples with entry, stop, target, outcome.
- Every statistical claim verbatim.
- For long material, split extraction across parallel subagents by source file, then cross-check attribution with grep before trusting a quote.

## 3. Check what can be checked
- Any claim with a number gets a replication on data you control (free daily/intraday bars are enough). Report in-sample and out-of-sample separately.
- Run a control: random entries through the same machinery. If the control matches the claim, the claim measures the machinery, not the edge.
- State your own parameter choices and why the conclusion does not depend on them.

## 4. Write the page
- One styled HTML page: what they teach, what is new versus what you already have, claims checked with the numbers, what to build natively ranked with effort, what not to build and why, and a "read it straight" verdict on the business side.
- Attribute public sources. Do not reproduce paid material; distill it in your own words.

## 5. Build only what survived
- Ranked build list, smallest first. Compile-check on a copy, deploy through the pipeline, verify on the live output, record the change in memory.
- Never copy vendor code into a product that is sold.

## Habits that saved hours
- Screenshots of the live thing beat log lines.
- A sandbox copy for any generator that writes into a live file. Synthetic test records never touch real ledgers.
- When a tool hangs with no output, check for a stuck UI state (a dialog, a collapsed panel, a wrong tab) before rewriting the tool.
