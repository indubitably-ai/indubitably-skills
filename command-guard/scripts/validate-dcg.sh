#!/usr/bin/env bash
# Validate command-guard installation and configuration

set -euo pipefail

echo "=== command-guard Installation Validation ==="

# Check if command-guard is installed
if ! command -v command-guard &> /dev/null; then
    echo "ERROR: command-guard not found in PATH"
    echo "Install from: https://github.com/anthropics/destructive-command-guard"
    exit 1
fi

echo "✓ command-guard binary found: $(command -v command-guard)"

# Check version
command-guard_VERSION=$(command-guard --version 2>&1 | awk '/command-guard v/ { for (i = 1; i <= NF; i++) if ($i ~ /^v[0-9]/) { print $i; exit } }')
if [[ -z "$command-guard_VERSION" ]]; then
    command-guard_VERSION="unknown"
fi
echo "✓ Version: $command-guard_VERSION"

# Check if hook is installed
if command-guard doctor &> /dev/null; then
    echo "✓ Hook installed correctly"
else
    echo "⚠ Hook may not be installed. Run: command-guard install"
fi

# Test pattern detection
echo ""
echo "=== Pattern Detection Tests ==="

test_command() {
    local cmd="$1"
    local expected="$2"
    local result

    if command-guard test "$cmd" &> /dev/null; then
        result="allow"
    else
        result="block"
    fi

    if [ "$result" = "$expected" ]; then
        echo "✓ '$cmd' → $result (expected)"
    else
        echo "✗ '$cmd' → $result (expected: $expected)"
        return 1
    fi
}

# Commands that SHOULD be blocked
test_command "rm -rf /" "block"
test_command "rm -rf ./build" "block"
test_command "git reset --hard HEAD" "block"
test_command "DROP DATABASE production" "block"

# Commands that SHOULD be allowed
test_command "git status" "allow"
test_command "find . -maxdepth 1 -type d" "allow"
test_command "ls -la" "allow"

echo ""
echo "=== Configuration ==="

# Check for project config
if [ -f ".command-guard.toml" ]; then
    echo "✓ Project config found: .command-guard.toml"
else
    echo "○ No project config (.command-guard.toml)"
fi

# Check for allowlist
if [ -f ".command-guard/allowlist.toml" ]; then
    echo "✓ Allowlist found: .command-guard/allowlist.toml"
else
    echo "○ No allowlist (.command-guard/allowlist.toml)"
fi

echo ""
echo "=== Validation Complete ==="
