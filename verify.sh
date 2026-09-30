#!/usr/bin/env bash
set -u
CLAUDE_DIR="$HOME/.claude"; fail=0
ok(){ printf '  OK    %s\n' "$*"; }; bad(){ printf '  FAIL  %s\n' "$*"; fail=1; }
echo "== skills =="
for s in copywriting cro social design-taste-frontend impeccable karpathy-guidelines ponytail humanizer last30days obsidian-markdown docx pptx xlsx skill-creator; do
  if [ -d "$CLAUDE_DIR/skills/$s" ] || ls -d "$CLAUDE_DIR/skills"/*/"$s" >/dev/null 2>&1 || ls -d "$HOME/.agents/skills/$s" >/dev/null 2>&1; then ok "skill $s"; else bad "skill $s missing"; fi
done
echo "== plugins =="
claude plugin list 2>/dev/null | grep -qi superpowers && ok "superpowers" || bad "superpowers plugin"
claude plugin list 2>/dev/null | grep -qi claude-mem && ok "claude-mem" || bad "claude-mem plugin"
echo "== MCP =="
for m in playwright context7 sequential-thinking; do claude mcp list 2>/dev/null | grep -qi "$m" && ok "mcp $m" || bad "mcp $m"; done
echo "== files =="
grep -q "Karpathy" "$CLAUDE_DIR/CLAUDE.md" 2>/dev/null && ok "CLAUDE.md carries the coding discipline" || bad "CLAUDE.md"
jq -e '.hooks.PreToolUse' "$CLAUDE_DIR/settings.json" >/dev/null 2>&1 && ok "settings hooks" || bad "settings hooks"
[ -f "$HOME/ClaudeHQ/knowledge/README.md" ] && ok "knowledge base" || bad "knowledge base"
[ $fail = 0 ] && echo "ALL OK" || echo "Some checks failed: see SETUP.md step 2"
