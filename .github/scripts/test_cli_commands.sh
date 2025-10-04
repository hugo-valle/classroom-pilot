#!/bin/bash
set -euo pipefail

# CLI command testing script
# Tests various CLI command combinations and scenarios

source "$(dirname "$0")/workflow_utils.sh"

CLASSROOM_PILOT_CMD="${1:-poetry run classroom-pilot}"

print_message "step" "Testing CLI commands and help system"

# Test main help command
print_message "step" "Testing main help..."
$CLASSROOM_PILOT_CMD --help

# Test version flag
print_message "step" "Testing version flag..."
$CLASSROOM_PILOT_CMD --version

# Test subcommand help
print_message "step" "Testing assignments help..."
$CLASSROOM_PILOT_CMD assignments --help

print_message "step" "Testing repos help..."
$CLASSROOM_PILOT_CMD repos --help

print_message "step" "Testing secrets help..."
$CLASSROOM_PILOT_CMD secrets --help

print_message "step" "Testing automation help..."
$CLASSROOM_PILOT_CMD automation --help

# Test specific command help
print_message "step" "Testing specific command help..."
$CLASSROOM_PILOT_CMD assignments orchestrate --help
$CLASSROOM_PILOT_CMD repos fetch --help
$CLASSROOM_PILOT_CMD secrets manage --help

# Test error conditions
print_message "step" "Testing error conditions..."
set +e

# Test invalid command
$CLASSROOM_PILOT_CMD invalid-command 2>/dev/null
if [[ $? -eq 0 ]]; then
    print_message "error" "Expected error for invalid command, but succeeded"
    exit 1
fi

# Test missing required arguments (should show help)
$CLASSROOM_PILOT_CMD assignments orchestrate 2>/dev/null
if [[ $? -eq 0 ]]; then
    print_message "warning" "Command succeeded without required arguments (may be using defaults)"
fi

set -e

print_message "success" "CLI command tests completed successfully"