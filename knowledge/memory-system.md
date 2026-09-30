# The memory system

Persistent memory is a directory of small markdown files plus one index. The index loads into every session; the files load on demand.

## Layout
```
memory/
  MEMORY.md                      # index: one line per file, no content
  user-<slug>.md                 # who the user is: role, expertise, preferences
  feedback-<slug>.md             # how they want you to work; corrections and confirmed approaches, with the why
  project-<slug>.md              # ongoing work, goals, constraints not derivable from code or git; absolute dates
  reference-<slug>.md            # pointers to external things: URLs, dashboards, tickets
```

## File format
```markdown
---
name: <kebab-slug, same as the filename>
description: <one line used to decide relevance>
metadata:
  type: user | feedback | project | reference
---

<the fact. For feedback and project entries, follow with **Why:** and **How to apply:** lines. Link related memories with [[name]].>
```

## Rules
1. One fact per file. Update the existing file rather than adding a near-duplicate. Delete memories that turn out wrong.
2. The index line is `- [Title](file.md) — hook`. Never put content in the index.
3. Do not store what the repo already records (code structure, git history, CLAUDE.md), and never store secrets.
4. Convert relative dates to absolute ones when writing.
5. When a memory names a file, function or flag, verify it still exists before relying on it.
6. Write memory at the moment of learning, not at the end of the session. Sessions end without warning.

## What good memories look like
- A rule with its reason: "Never auto-reload his dashboard tab. Why: it wipes the chat. How to apply: the UI polls itself; tell him to refresh."
- A project fact with a date: "Sep 28 2026: learning mode replaced the 6/10 floor by the user's explicit instruction; hardFloor input is the way back."
- A pointer: "Deploy pipeline notes live in project-deploy.md; the chart pins to a script version, so save is not deploy."
