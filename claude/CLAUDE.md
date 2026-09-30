# Global instructions (~/.claude/CLAUDE.md)

## Coding discipline — Karpathy's guidelines (follow these on every coding task)

Bias toward caution over speed; for trivial tasks, use judgment.

### 1. Think Before Coding
Don't assume. Don't hide confusion. Surface tradeoffs.
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them; don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

### 2. Simplicity First
Minimum code that solves the problem. Nothing speculative.
- No features beyond what was asked. No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

### 3. Surgical Changes
Touch only what you must. Clean up only your own mess.
- Don't "improve" adjacent code, comments, or formatting. Don't refactor things that aren't broken.
- Match existing style. If you notice unrelated dead code, mention it; don't delete it.
- Remove imports/variables/functions that YOUR changes made unused; leave pre-existing dead code unless asked.

### 4. Goal-Driven Execution
Define success criteria. Loop until verified.
- Turn tasks into verifiable goals ("fix the bug" → "write a test that reproduces it, then make it pass").
- For multi-step tasks, state a brief plan with a verify check per step.

## Workflow
- Every new substantial task starts with a short implementation spec (assumptions and defaults stated) before building.
- Verify, don't trust "done": read the log, open the output, look at the screenshot. A "compile clean" line alone proves nothing.
- Report outcomes faithfully. If tests fail, say so with the output. If a step was skipped, say that.

## Design — default skills
For any frontend / UI / landing-page / redesign / visual work, use the taste-skill stack as the primary, not the basic `frontend-design` skill:
- `design-taste-frontend` first on UI/landing/portfolio/redesign work.
- `impeccable` for design audits, polish passes, live-browser iteration, and design-system/token work.
- Specialized variants when they fit: `minimalist-ui`, `industrial-brutalist-ui`, `high-end-visual-design`, `gpt-taste`, `redesign-existing-projects`, `image-to-code`, `imagegen-frontend-web`/`-mobile`, `brandkit`, `stitch-design-taste`.

## Deliverables
- Anything the user will read at length is a styled HTML page opened in the browser, not raw markdown in the terminal.
- Reports lead with the outcome. Numbers go in tables. Commands go in code blocks. No filler.
