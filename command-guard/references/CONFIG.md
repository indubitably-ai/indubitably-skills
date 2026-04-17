# command-guard Configuration Reference

## Configuration Hierarchy

Settings are loaded in this order (highest to lowest priority):

1. **Environment Variables** (`command-guard_*` prefix)
2. **Explicit Config File** (`command-guard_CONFIG` env var)
3. **Project Config** (`.command-guard.toml` in repo root)
4. **User Config** (`~/.config/command-guard/config.toml`)
5. **System Config** (`/etc/command-guard/config.toml`)
6. **Compiled Defaults**

---

## Environment Variables

| Variable | Purpose | Example |
|----------|---------|---------|
| `command-guard_PACKS` | Enable optional packs | `"database.postgresql,kubernetes"` |
| `command-guard_DISABLE` | Disable specific packs | `"kubernetes.helm"` |
| `command-guard_BYPASS` | Skip all checks (escape hatch) | `1` |
| `command-guard_VERBOSE` | Verbosity level | `0-3` |
| `command-guard_FORMAT` | Default output format | `text`, `json`, `sarif` |
| `command-guard_CONFIG` | Explicit config path | `/path/to/config.toml` |

---

## Project Config (.command-guard.toml)

```toml
# Pack configuration
[packs]
enabled = [
    "database.postgresql",
    "kubernetes.kubectl",
    "cloud.aws"
]

# Override patterns (evaluated before packs)
[overrides]
allow_patterns = [
    "rm -rf ./node_modules",
    "rm -rf ./build",
    "git clean -fd ./generated"
]
block_patterns = [
    "rm -rf /custom/dangerous/path"
]

# Heredoc scanning configuration
[heredoc]
enabled = true
max_size_bytes = 1048576  # 1MB
max_lines = 10000
tier2_budget_ms = 200
tier3_budget_ms = 5000

# Supported languages for AST analysis
languages = ["bash", "python", "ruby", "javascript", "typescript", "go", "php"]
```

---

## Agent-Specific Profiles

Configure different trust levels and rules per agent:

```toml
# Claude Code - high trust, additional allowlist
[agents.claude-code]
trust_level = "high"
additional_allowlist = [
    "npm run build",
    "cargo build --release"
]

# Gemini CLI - medium trust
[agents.gemini-cli]
trust_level = "medium"

# Unknown agents - paranoid mode
[agents.unknown]
trust_level = "low"
extra_packs = ["paranoid"]
```

### Trust Levels

| Level | Behavior |
|-------|----------|
| `high` | Core packs only, faster evaluation |
| `medium` | Standard evaluation (default) |
| `low` | Extra scrutiny, more packs enabled |

---

## Allowlist Configuration

### Project-Level Allowlist (.command-guard/allowlist.toml)

```toml
[[rules]]
id = "core.git:reset-hard"
reason = "CI cleanup requires hard reset"
expires = "2025-12-31"  # Optional expiration

[[rules]]
id = "core.filesystem:rm-rf-dangerous"
path = "./build"  # Scope to specific path
reason = "Build directory cleanup"
```

### User-Level Allowlist (~/.config/command-guard/allowlist.toml)

```toml
[[rules]]
id = "containers.docker:system-prune"
reason = "Regular Docker cleanup on dev machine"
```

---

## Heredoc Three-Tier Architecture

command-guard scans inline scripts (`bash -c`, `python -c`, heredocs) with progressive depth:

### Tier 1: Trigger Detection (<5μs)
- Ultra-fast RegexSet screening
- Detects heredoc operators (`<<EOF`, `<<'EOF'`)
- Detects inline script flags (`python -c`, `bash -c`, `ruby -e`)

### Tier 2: Content Extraction (<200μs)
- Parse heredoc body between delimiters
- Bounded by `max_size_bytes` and `max_lines`
- Budget controlled by `tier2_budget_ms`

### Tier 3: AST Pattern Matching (<5ms)
- Parse with language-specific grammars (tree-sitter/ast-grep)
- Match structural patterns for destructive operations
- Budget controlled by `tier3_budget_ms`

**Fail-open behavior:** If any tier exceeds its budget, remaining tiers are skipped and command is ALLOWED with a warning logged.

### Tune Heredoc Settings

```toml
[heredoc]
# Increase for large scripts
max_size_bytes = 2097152  # 2MB

# Increase budgets if seeing "budget exceeded" warnings
tier2_budget_ms = 500
tier3_budget_ms = 10000

# Disable for performance (not recommended)
enabled = false
```

---

## CI Integration

### GitHub Actions

```yaml
- name: command-guard Pre-commit Scan
  run: command-guard scan --git-diff origin/main..HEAD --fail-on error
```

### Pre-commit Hook

```bash
# Install hook
command-guard scan install-pre-commit

# Hook checks staged files before each commit
# Blocks commit if destructive patterns found
```

### GitLab CI

```yaml
command-guard-scan:
  script:
    - command-guard scan --format sarif > command-guard-results.sarif
  artifacts:
    reports:
      sast: command-guard-results.sarif
```

---

## Hook Protocol

command-guard integrates with Claude Code via the PreToolUse hook:

### Registration (~/.config/claude-code/settings.json)

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "command-guard hook"
      }]
    }]
  }
}
```

### Input (JSON on stdin)

```json
{
  "tool_name": "Bash",
  "tool_input": {"command": "git reset --hard"}
}
```

### Deny Response (JSON on stdout)

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "BLOCKED by command-guard: ...",
    "allowOnceCode": "ab12",
    "ruleId": "core.git:reset-hard"
  }
}
```

### Allow Response

Exit code 0 with no output.
