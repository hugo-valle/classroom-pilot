#!/bin/bash
#
# Cron Job Management Helper for GitHub Classroom Assignment
#
# This script helps install, remove, and manage the automated sync cron job.
#
# Usage: ./scripts/manage-cron.sh [install|remove|status|logs]
#

set -euo pipefail

# Script directory and paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOOLS_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
REPO_ROOT="$(cd "$TOOLS_ROOT/.." && pwd)"

# Source shared logging utility
source "$TOOLS_ROOT/utils/logging.sh"

# Additional logging functions for consistency
log_info() { print_status "$@"; }
log_success() { print_success "$@"; }
log_warning() { print_warning "$@"; }
log_error() { print_error "$@"; }

# Configuration
CRON_SCRIPT="$TOOLS_ROOT/scripts/cron-sync.sh"
LOG_FILE="$REPO_ROOT/tools/generated/cron-sync.log"
CRON_COMMENT="# GitHub Classroom Assignment Auto-Sync"
CRON_SCHEDULE="0 */4 * * *"  # Every 4 hours
CRON_COMMAND="$CRON_SCRIPT '$REPO_ROOT/assignment.conf' >/dev/null 2>&1"

# Help function
show_help() {
    cat << EOF
Cron Job Management Helper

USAGE:
    ./scripts/manage-cron.sh [command]

COMMANDS:
    install     Install the auto-sync cron job (runs every 4 hours)
    remove      Remove the auto-sync cron job
    status      Check if the cron job is installed
    logs        Show recent sync log entries
    help        Show this help

CRON JOB DETAILS:
    Schedule:   Every 4 hours (at minute 0 of hours 0, 4, 8, 12, 16, 20)
    Command:    $CRON_COMMAND
    Log file:   $LOG_FILE

EXAMPLES:
    # Install the cron job
    ./scripts/manage-cron.sh install
    
    # Check if it's running
    ./scripts/manage-cron.sh status
    
    # View recent logs
    ./scripts/manage-cron.sh logs
    
    # Remove the cron job
    ./scripts/manage-cron.sh remove

EOF
}

# Function to check if cron job exists
cron_exists() {
    crontab -l 2>/dev/null | grep -F "$CRON_SCRIPT" >/dev/null 2>&1
}

# Install cron job
install_cron() {
    log_info "Installing auto-sync cron job..."
    
    # Check if script exists and is executable
    if [[ ! -x "$CRON_SCRIPT" ]]; then
        log_error "Cron script not found or not executable: $CRON_SCRIPT"
        exit 1
    fi
    
    # Check if assignment config exists
    if [[ ! -f "$REPO_ROOT/assignment.conf" ]]; then
        log_error "Assignment configuration not found: $REPO_ROOT/assignment.conf"
        log_error "Please create the configuration file before installing the cron job"
        exit 1
    fi
    
    # Check if cron job already exists
    if cron_exists; then
        log_warning "Cron job already exists. Remove it first if you want to reinstall."
        log_info "Current cron job:"
        crontab -l | grep -A1 -B1 "$CRON_SCRIPT" || true
        return 0
    fi
    
    # Create the cron job entry
    local cron_entry="$CRON_COMMENT"$'\n'"$CRON_SCHEDULE $CRON_COMMAND"
    
    # Add to existing crontab or create new one
    if crontab -l >/dev/null 2>&1; then
        # Append to existing crontab
        (crontab -l; echo "$cron_entry") | crontab -
    else
        # Create new crontab
        echo "$cron_entry" | crontab -
    fi
    
    log_success "Cron job installed successfully!"
    log_info "Schedule: $CRON_SCHEDULE (every 4 hours)"
    log_info "Command: $CRON_COMMAND"
    log_info "Logs will be written to: $LOG_FILE"
    
    echo
    log_info "You can check the status with: ./scripts/manage-cron.sh status"
    log_info "You can view logs with: ./scripts/manage-cron.sh logs"
}

# Remove cron job
remove_cron() {
    log_info "Removing auto-sync cron job..."
    
    if ! cron_exists; then
        log_warning "Cron job not found. Nothing to remove."
        return 0
    fi
    
    # Remove the cron job and its comment
    crontab -l | grep -v -F "$CRON_SCRIPT" | grep -v -F "$CRON_COMMENT" | crontab -
    
    log_success "Cron job removed successfully!"
}

# Show cron job status
show_status() {
    log_info "Checking cron job status..."
    
    if cron_exists; then
        log_success "Auto-sync cron job is installed"
        echo
        echo "Current cron job:"
        crontab -l | grep -A1 -B1 "$CRON_SCRIPT" || true
        
        echo
        echo "Next scheduled runs:"
        # Show next few scheduled times (requires 'at' or we can calculate manually)
        echo "Every 4 hours: 00:00, 04:00, 08:00, 12:00, 16:00, 20:00"
        
        # Check if log file exists and show last activity
        if [[ -f "$LOG_FILE" ]]; then
            echo
            echo "Last log activity:"
            tail -n 3 "$LOG_FILE" 2>/dev/null || echo "No recent log entries"
        fi
    else
        log_warning "Auto-sync cron job is not installed"
        echo
        log_info "To install it, run: ./scripts/manage-cron.sh install"
    fi
}

# Show recent logs
show_logs() {
    log_info "Showing recent sync logs..."
    
    if [[ ! -f "$LOG_FILE" ]]; then
        log_warning "Log file not found: $LOG_FILE"
        log_info "The cron job may not have run yet, or logging is not working."
        return 0
    fi
    
    echo
    echo "=== Recent Sync Log Entries ==="
    tail -n 20 "$LOG_FILE"
    
    echo
    echo "=== Log File Info ==="
    echo "File: $LOG_FILE"
    echo "Size: $(du -h "$LOG_FILE" 2>/dev/null | cut -f1 || echo "unknown")"
    echo "Last modified: $(ls -l "$LOG_FILE" | awk '{print $6, $7, $8}')"
}

# Main function
main() {
    local command="${1:-help}"
    
    case "$command" in
        "install")
            install_cron
            ;;
        "remove")
            remove_cron
            ;;
        "status")
            show_status
            ;;
        "logs")
            show_logs
            ;;
        "help"|"--help"|"-h")
            show_help
            ;;
        *)
            log_error "Unknown command: $command"
            echo
            show_help
            exit 1
            ;;
    esac
}

# Execute main function
main "$@"
