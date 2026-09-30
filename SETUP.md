# Setup walkthrough

You are a Claude Code agent setting up a new machine. Work through the steps in order, verify each one, and do not skip a verification because a step "looked fine". Assume macOS unless the shell says otherwise; Linux notes are inline.

## Step 0. Prerequisites

Check, and install only what is missing:

```bash
command -v claude || echo "install Claude Code: https://docs.claude.com/en/docs/claude-code/setup"
command -v node && command -v npm || echo "install Node 20+: https://nodejs.org or brew install node"
command -v git || echo "install git"
command -v jq || echo "brew install jq   (Linux: apt install jq)"
command -v uv || echo "optional, for the time MCP server: curl -LsSf https://astral.sh/uv/install.sh | sh"
command -v gh || echo "optional: brew install gh"
```

Then clone this repo somewhere permanent, for example `~/claude-transfer`, and `cd` into it.

## Step 1. Run the installer

```bash
bash install.sh
```

It is idempotent. Run it again after fixing anything. It does, in order:

1. Plugin marketplaces: `anthropics/claude-plugins-official`, `thedotmack/claude-mem`.
2. Plugins: superpowers, frontend-design, firecrawl, claude-mem. (Apollo, Postiz and iMessage are also on the official marketplace; install them only if you have those accounts.)
3. Skills, from their original repositories, global scope, Claude Code agent:

   | Skill set | Source | What it adds |
   |---|---|---|
   | Marketing skills (43) | `coreyhaines31/marketingskills` | copywriting, CRO, SEO, ads, emails, social, pricing, offers, launch, and the rest |
   | Design taste family | `leonxlnx/taste-skill` | anti-slop frontend, minimalist, brutalist, high-end visual, redesign, image-to-code, brandkit, stitch, full-output enforcement |
   | Impeccable | `pbakaus/impeccable` | design audit, polish, critique commands and a detector hook |
   | Karpathy guidelines | `multica-ai/andrej-karpathy-skills` | think before coding, simplicity, surgical changes, goal-driven execution |
   | Ponytail | `DietrichGebert/ponytail` | the laziest correct solution, YAGNI ladder |
   | Humanizer | `blader/humanizer` | removes AI-writing patterns from text |
   | last30days | `mvanhorn/last30days-skill` | what people actually said about a topic in the last 30 days |
   | Obsidian skills | `kepano/obsidian-skills` | Obsidian markdown, Bases, JSON Canvas |
   | Anthropic document skills | `anthropics/skills` | docx, pptx, xlsx, pdf, skill-creator, mcp-builder |
   | gstack | `garrytan/gstack` | CEO / eng manager / designer / QA / release review roles |
   | Claude video | `bradautomates/claude-video` | watch and summarize video |

4. MCP servers, user scope: playwright, context7, sequential-thinking, time.
5. Global instructions: `claude/CLAUDE.md` into `~/.claude/CLAUDE.md` (appended inside markers if a file already exists).
6. Settings: merges hooks, status line and the safe permission allowlist from `claude/settings.additions.json` into `~/.claude/settings.json`, after backing it up.
7. Knowledge base: copies `knowledge/` to `~/ClaudeHQ/knowledge/` and points `CLAUDE.md` at it.

## Step 2. Verify

```bash
bash verify.sh
```

Every line must say OK. If a skill is missing, install it by hand with the command printed next to it. If `npx skills` is unavailable, `git clone` the repo and copy or symlink its skill folders into `~/.claude/skills/`.

Then restart Claude Code and confirm, in a fresh session, that the skills appear in the available-skills list and `claude mcp list` shows all four servers connected.

## Step 3. Memory

Your harness gives you a persistent memory directory (the system prompt names it, under `~/.claude/projects/<project>/memory/`). Create it from `claude/memory/`:

1. Copy `claude/memory/MEMORY.md` there as the index.
2. Read `knowledge/memory-system.md` for the file format and the rules: one fact per file, frontmatter with `name`, `description`, `type`; index line per file; update rather than duplicate; never store secrets or anything the repo already records.
3. Write the first three memories from your user's own words in your first session: who they are, how they want you to work, what they are building. Ask nothing you can find out yourself.

## Step 4. Read the knowledge base

Read `knowledge/README.md`, then the operating principles and the research method in full. Read the trading documents when the user's work touches markets. Do not summarize them back to the user unprompted; use them.

## Step 5. Report

Tell the user, in plain language: what installed, what did not and why, what needs their account (Apollo, Postiz, iMessage, any API key), and that memory is initialized. Then get to work.

## Licenses of what you installed

marketingskills: see repo license · taste-skill: see repo · impeccable: Apache 2.0 · andrej-karpathy-skills: MIT · ponytail: MIT · humanizer: MIT · last30days: see repo · obsidian-skills: see repo · anthropics/skills: per-skill LICENSE.txt · gstack: see repo · claude-video: see repo · superpowers, frontend-design, firecrawl, claude-mem: plugin licenses in their repos.
