# Claude agent transfer kit

This repo turns a fresh Claude Code install into the same kind of agent Alan runs: the same skills, plugins, MCP servers, coding discipline, memory system and working principles, plus a knowledge base covering the trading system, the research method and the tooling lessons learned the hard way.

**If you are the friend receiving this:** open Claude Code in your home directory and paste this one line:

> Read `SETUP.md` in https://github.com/qbalan42-droid/claude-transfer and follow it step by step. Run `install.sh`, then `verify.sh`, fix anything that fails, then read `knowledge/README.md` and set up my memory from `claude/memory/`. Report what is installed and what is missing.

Your Claude will clone the repo, install everything from the original sources, write the global instructions, and load the knowledge base. Nothing here needs an API key. Nothing here contains anyone's private data.

## What is in here

| Path | What it is |
|---|---|
| `SETUP.md` | The walkthrough your Claude executes, with a verification checklist |
| `install.sh` | Idempotent installer: plugins, skills, MCP servers, global instructions, settings, knowledge base |
| `verify.sh` | Checks every piece landed |
| `claude/CLAUDE.md` | Global coding discipline (Karpathy's four rules) and design skill defaults |
| `claude/settings.additions.json` | Hooks (audit log, desktop notification), status line, safe permission allowlist |
| `claude/memory/` | The persistent memory system: index plus typed memory files |
| `knowledge/` | The knowledge base: operating principles, research method, trading system, vendor-claim math, pipeline architecture, video editing |
| `tools/` | Small scripts referenced by the knowledge base (win-rate math, Asia OTE levels, the vlog edit pipeline) |

## What is deliberately not in here

API keys, tokens, anyone's personal or financial data, client data, the SNOOZER Pine source (sold commercially), Daymark (someone else's build), and any paid course material. The trading knowledge is methodology written from scratch, with public sources attributed.

## Licenses

Scripts in `tools/`: MIT. Documents in `knowledge/`: CC BY-NC-SA 4.0. Every third-party skill and plugin installs from its own repository under its own license, listed in `SETUP.md`.
