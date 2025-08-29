#!/bin/bash
#
# Automated Sync Cron Job for GitHub Classroom Assignment
#
# This script is designed to run as a cron job to automatically sync
# the template repository with GitHub Classroom and push tokens to
# student repositories as they accept assignments.
#
# Usage: ./scripts/cron-sync.sh [config-file]
#
# Cron Example (every 4 hours):
# 0 */4 * * * /path/to/assignment/tools/scripts/cron-sync.sh >/dev/null 2>&1
#

set -euo pipefail

# Script directory and paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOOLS_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
REPO_ROOT="$(cd "$TOOLS_ROOT/.." && pwd)"
DEFAULT_CONFIG="$REPO_ROOT/assignment.conf"

# Source shared logging utility
source "$TOOLS_ROOT/utils/logging.sh"

# Configuration
CONFIG_FILE="${1:-$DEFAULT_CONFIG}"
LOG_FILE="$REPO_ROOT/tools/generated/cron-sync.log"

# Logging function for cron jobs
log_cron() {
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] $*" >> "$LOG_FILE"
}

# Function to rotate log file if it gets too large (>10MB)
rotate_log() {
    if [[ -f "$LOG_FILE" ]] && [[ $(stat -f%z "$LOG_FILE" 2>/dev/null || stat -c%s "$LOG_FILE" 2>/dev/null || echo 0) -gt 10485760 ]]; then
        mv "$LOG_FILE" "${LOG_FILE}.old"
        log_cron "INFO: Log file rotated"
    fi
}

# Main cron sync function
main() {
    # Ensure log directory exists
    mkdir -p "$(dirname "$LOG_FILE")"
    
    # Rotate log if needed
    rotate_log
    
    log_cron "INFO: Starting automated sync job"
    log_cron "INFO: Using config file: $CONFIG_FILE"
    
    # Change to repository root
    cd "$REPO_ROOT"
    
    # Check if config file exists
    if [[ ! -f "$CONFIG_FILE" ]]; then
        log_cron "ERROR: Configuration file not found: $CONFIG_FILE"
        exit 1
    fi
    
    # Source configuration to validate it's readable
    # shellcheck source=/dev/null
    if ! source "$CONFIG_FILE" 2>/dev/null; then
        log_cron "ERROR: Failed to load configuration file: $CONFIG_FILE"
        exit 1
    fi
    
    # Check if we're in a git repository
    if [[ ! -d ".git" ]]; then
        log_cron "ERROR: Not in a git repository: $REPO_ROOT"
        exit 1
    fi
    
    # Run the orchestrator with sync step only, non-interactive mode
    local orchestrator_cmd="$TOOLS_ROOT/scripts/assignment-orchestrator.sh"
    local orchestrator_args=(
        "$CONFIG_FILE"
        "--step" "sync"
        "--yes"
        "--verbose"
    )
    
    log_cron "INFO: Executing: $orchestrator_cmd ${orchestrator_args[*]}"
    
    # Capture both stdout and stderr for logging
    if "$orchestrator_cmd" "${orchestrator_args[@]}" >> "$LOG_FILE" 2>&1; then
        log_cron "SUCCESS: Sync completed successfully"
    else
        local exit_code=$?
        log_cron "ERROR: Sync failed with exit code: $exit_code"
        exit $exit_code
    fi
    
    log_cron "INFO: Automated sync job completed"
}

# Error handling for cron environment
trap 'log_cron "ERROR: Script failed with exit code $?"' ERR

# Execute main function
main "$@"
