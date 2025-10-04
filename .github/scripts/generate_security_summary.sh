#!/bin/bash
set -euo pipefail

# Security monitoring summary generator
# Creates security metrics dashboard

source "$(dirname "$0")/workflow_utils.sh"

SECURITY_CHECK_START="${1:-$(date +%s)}"
ADVISORIES="${2:-0}"
VULNERABLE_DEPS="${3:-0}" 
UPDATES_NEEDED="${4:-false}"

step_duration=$(report_step_timing "Security Monitoring" "$SECURITY_CHECK_START")

security_summary="| Security Metric | Count | Status |\n"
security_summary+="| --- | --- | --- |\n"
security_summary+="| Security Advisories | ${ADVISORIES} | $([ "$ADVISORIES" -eq 0 ] && echo "✅" || echo "⚠️") |\n"
security_summary+="| Vulnerable Dependencies | ${VULNERABLE_DEPS} | $([ "$VULNERABLE_DEPS" -eq 0 ] && echo "✅" || echo "⚠️") |\n"
security_summary+="| Security Updates Needed | $([ "$UPDATES_NEEDED" = "true" ] && echo "Yes" || echo "No") | $([ "$UPDATES_NEEDED" = "true" ] && echo "⚠️" || echo "✅") |\n"
security_summary+="| **Monitoring Duration** | **${step_duration}s** | ✅ |"

create_step_summary "Security Monitoring" "$([ "$UPDATES_NEEDED" = "true" ] && echo "warning" || echo "success")" "$security_summary"

print_message "$([ "$UPDATES_NEEDED" = "true" ] && echo "warning" || echo "success")" "Security monitoring summary generated"