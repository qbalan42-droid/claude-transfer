#!/usr/bin/env bash
# Claude agent transfer kit installer. Idempotent: safe to run again.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
CLAUDE_DIR="$HOME/.claude"
KB="$HOME/ClaudeHQ/knowledge"
ok()   { printf '  \033[32mOK\033[0m   %s\n' "$*"; }
warn() { printf '  \033[33mWARN\033[0m %s\n' "$*"; }
step() { printf '\n== %s ==\n' "$*"; }

step "0. prerequisites"
for c in claude node npm git jq; do command -v "$c" >/dev/null 2>&1 && ok "$c" || warn "$c missing (see SETUP.md step 0)"; done
command -v uv >/dev/null 2>&1 && ok "uv" || warn "uv missing: the time MCP server will be skipped"
mkdir -p "$CLAUDE_DIR/skills" "$KB"

step "1. plugin marketplaces"
for m in anthropics/claude-plugins-official thedotmack/claude-mem; do
  claude plugin marketplace add "$m" >/dev/null 2>&1 && ok "marketplace $m" || warn "marketplace $m (may already exist)"
done

step "2. plugins"
for p in superpowers@claude-plugins-official frontend-design@claude-plugins-official firecrawl@claude-plugins-official claude-mem@thedotmack; do
  claude plugin install "$p" >/dev/null 2>&1 && ok "plugin $p" || warn "plugin $p (already installed, or install by hand: claude plugin install $p)"
done
echo "  note: apollo, postiz and imessage plugins exist on claude-plugins-official; install only with those accounts."

step "3. skills (global, from original repositories)"
SKILL_REPOS="coreyhaines31/marketingskills leonxlnx/taste-skill pbakaus/impeccable multica-ai/andrej-karpathy-skills DietrichGebert/ponytail blader/humanizer mvanhorn/last30days-skill kepano/obsidian-skills anthropics/skills garrytan/gstack bradautomates/claude-video"
for r in $SKILL_REPOS; do
  if npx -y skills add "$r" --global --yes --agent claude-code >/dev/null 2>&1; then ok "skills from $r"
  else
    # fallback: clone and link every folder that carries a SKILL.md
    tmp="$(mktemp -d)"; if git clone --depth 1 "https://github.com/$r" "$tmp/repo" >/dev/null 2>&1; then
      n=0; while IFS= read -r sk; do d="$(dirname "$sk")"; name="$(basename "$d")"; [ "$name" = "repo" ] && name="$(basename "$r")"
        rm -rf "$CLAUDE_DIR/skills/$name"; cp -R "$d" "$CLAUDE_DIR/skills/$name"; n=$((n+1)); done < <(find "$tmp/repo" -name SKILL.md -not -path '*/node_modules/*' -not -path '*/.git/*')
      ok "skills from $r (cloned, $n skill folders copied)"
    else warn "skills from $r: npx skills failed and clone failed; install by hand"; fi
    rm -rf "$tmp"
  fi
done

step "4. MCP servers (user scope)"
claude mcp add -s user playwright -- npx -y @playwright/mcp@latest --browser chromium >/dev/null 2>&1 && ok "playwright" || warn "playwright (exists?)"
claude mcp add -s user context7 -- npx -y @upstash/context7-mcp >/dev/null 2>&1 && ok "context7" || warn "context7 (exists?)"
claude mcp add -s user sequential-thinking -- npx -y @modelcontextprotocol/server-sequential-thinking >/dev/null 2>&1 && ok "sequential-thinking" || warn "sequential-thinking (exists?)"
if command -v uv >/dev/null 2>&1; then claude mcp add -s user time -- uvx mcp-server-time >/dev/null 2>&1 && ok "time" || warn "time (exists?)"; fi

step "5. global instructions"
MARK_A="<!-- claude-transfer:start -->"; MARK_B="<!-- claude-transfer:end -->"
if [ ! -f "$CLAUDE_DIR/CLAUDE.md" ]; then cp "$HERE/claude/CLAUDE.md" "$CLAUDE_DIR/CLAUDE.md"; ok "wrote ~/.claude/CLAUDE.md"
elif grep -q "$MARK_A" "$CLAUDE_DIR/CLAUDE.md"; then ok "~/.claude/CLAUDE.md already carries the transfer block"
else { printf '\n%s\n' "$MARK_A"; cat "$HERE/claude/CLAUDE.md"; printf '%s\n' "$MARK_B"; } >> "$CLAUDE_DIR/CLAUDE.md"; ok "appended the transfer block to ~/.claude/CLAUDE.md"; fi

step "6. settings (hooks, status line, safe allowlist)"
S="$CLAUDE_DIR/settings.json"; [ -f "$S" ] || echo '{}' > "$S"
cp "$S" "$S.bak.$(date +%Y%m%d%H%M%S)"
if command -v jq >/dev/null 2>&1; then
  jq -s '.[0] as $cur | .[1] as $add
    | $cur
    | .hooks = (($cur.hooks // {}) * $add.hooks)
    | .permissions.allow = ((($cur.permissions.allow // []) + $add.permissions.allow) | unique)
    | .statusLine = ($cur.statusLine // $add.statusLine)' "$S" "$HERE/claude/settings.additions.json" > "$S.new" && mv "$S.new" "$S" && ok "merged settings (backup kept)"
  command -v ccusage >/dev/null 2>&1 || npm i -g ccusage >/dev/null 2>&1 && ok "ccusage status line" || warn "ccusage not installed; status line will be blank until: npm i -g ccusage"
else warn "jq missing: merge claude/settings.additions.json into ~/.claude/settings.json by hand"; fi

step "7. knowledge base"
cp -R "$HERE/knowledge/." "$KB/" && ok "knowledge -> $KB"
cp -R "$HERE/tools" "$HOME/ClaudeHQ/" && ok "tools -> ~/ClaudeHQ/tools"
grep -q "ClaudeHQ/knowledge" "$CLAUDE_DIR/CLAUDE.md" || printf '\n## Knowledge base\nRead ~/ClaudeHQ/knowledge/README.md at the start of any task it covers (research, trading, marketing deliverables, video). Memory: see ~/ClaudeHQ/knowledge/memory-system.md.\n' >> "$CLAUDE_DIR/CLAUDE.md"

printf '\nDone. Now run: bash verify.sh\n'
