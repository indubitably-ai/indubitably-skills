#!/usr/bin/env bash
# Validate agent-session-history installation and basic functionality

set -euo pipefail

echo "=== agent-session-history Session Search Validation ==="
echo

# Check agent-session-history is installed
if ! command -v agent-session-history &> /dev/null; then
    echo "ERROR: agent-session-history is not installed or not in PATH"
    echo "FIX: Install agent-session-history from https://github.com/your/agent-session-history"
    exit 2
fi

if ! command -v jq &> /dev/null; then
    echo "ERROR: jq is not installed or not in PATH"
    echo "FIX: Install jq to parse agent-session-history JSON output"
    exit 2
fi

echo "✓ agent-session-history found: $(command -v agent-session-history)"

# Check agent-session-history status
echo
echo "Checking agent-session-history status..."
if ! STATUS=$(agent-session-history status --robot-format json 2>/dev/null); then
    echo "ERROR: agent-session-history status failed"
    echo "FIX: Run 'agent-session-history doctor' to repair"
    exit 2
fi

# Check if index is fresh
if ! FRESH=$(jq -r '.index.fresh // false' <<< "$STATUS" 2>/dev/null); then
    echo "ERROR: agent-session-history status returned invalid JSON"
    exit 2
fi
REBUILDING=$(jq -r '.index.rebuilding // .rebuild.active // false' <<< "$STATUS")
if [ "$REBUILDING" = "true" ]; then
    echo "WARNING: Index rebuild is in progress"
    echo "FIX: Wait for the rebuild to finish, then rerun validation"
elif [ "$FRESH" = "true" ]; then
    echo "✓ Index is fresh"
else
    echo "WARNING: Index is stale"
    echo "FIX: Run 'agent-session-history index --json'"
fi

# Check conversation count
CONVOS=$(jq -r '.database.conversations // 0' <<< "$STATUS")
echo "✓ Indexed conversations: $CONVOS"

if [ "$REBUILDING" != "true" ] && [ "$CONVOS" -eq 0 ]; then
    echo "WARNING: No conversations indexed"
    echo "FIX: Run 'agent-session-history index --full --json' to rebuild index"
fi

# Test basic search (should not panic)
echo
echo "Testing basic search..."
if agent-session-history search "*" --json --limit 1 --fields minimal > /dev/null 2>&1; then
    echo "✓ Basic search works"
else
    echo "ERROR: Basic search failed"
    exit 2
fi

# Test aggregation (the most common pitfall)
echo
echo "Testing aggregation..."
if agent-session-history search "*" --json --aggregate agent --limit 1 --fields minimal > /dev/null 2>&1; then
    echo "✓ Aggregation works"
else
    echo "ERROR: Aggregation failed"
    exit 2
fi

echo
echo "=== Validation Complete ==="
echo "agent-session-history is ready to use"
exit 0
