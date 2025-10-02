#!/bin/bash
set -euo pipefail

# Comprehensive health summary generator
# Creates detailed repository health report

source "$(dirname "$0")/workflow_utils.sh"

HEALTH_CHECK_START="${1:-$(date +%s)}"
ADVISORIES="${2:-0}"
VULNERABLE_DEPS="${3:-0}"
UPDATES_NEEDED="${4:-false}"

step_duration=$(report_step_timing "Enhanced Health Check" "$HEALTH_CHECK_START")

# Load workflow status aggregation utilities
if [[ -f ".github/scripts/workflow_status_aggregator.sh" ]]; then
    chmod +x .github/scripts/workflow_status_aggregator.sh
    source .github/scripts/workflow_status_aggregator.sh
    
    # Collect workflow status for auto-update
    collect_workflow_status "auto-update" "enhanced-health-check" || true
    
    # Generate workflow status dashboard
    generate_workflow_dashboard "auto_update_health_dashboard.md" || true
    
    # Track workflow trends
    track_workflow_trends "auto-update" || true
fi

# Overall health assessment
overall_health="🟢 Healthy"
if [[ $VULNERABLE_DEPS -gt 0 ]] || [[ "$UPDATES_NEEDED" = "true" ]]; then
    overall_health="🟡 Minor Issues"
fi

# Security checks from environment
security_checks=${SECURITY_CHECKS_PASSED:-2}

health_summary="# 🏥 Repository Health Report\n\n"
health_summary+="## 📊 Overall Assessment: $overall_health\n\n"
health_summary+="| Health Category | Status | Details |\n"
health_summary+="| --- | --- | --- |\n"
health_summary+="| **Security** | $([ $VULNERABLE_DEPS -eq 0 ] && echo "🟢 Secure" || echo "🟡 Needs Attention") | $VULNERABLE_DEPS vulnerable dependencies |\n"
health_summary+="| **Dependencies** | $([ "$UPDATES_NEEDED" = "true" ] && echo "🟡 Updates Available" || echo "🟢 Up to Date") | Security updates $([ "$UPDATES_NEEDED" = "true" ] && echo "needed" || echo "not needed") |\n"
health_summary+="| **Configuration** | $([ $security_checks -ge 3 ] && echo "🟢 Good" || echo "🟡 Fair") | $security_checks/4 security checks passed |\n"
health_summary+="| **Performance** | 📈 Monitored | Workflow trends tracked |\n"
health_summary+="| **Duration** | ⏱️ ${step_duration}s | Health check completed |\n\n"

# Include workflow performance metrics if available
if [[ -f "auto_update_health_dashboard.md" ]]; then
    health_summary+="\n## Workflow Performance Metrics\n\n"
    health_summary+="$(cat auto_update_health_dashboard.md | grep -A 10 '### Workflow Metrics' || echo 'No detailed metrics available')\n\n"
fi

health_summary+="---\n_Health check completed on $(date -u)_"

create_step_summary "Enhanced Repository Health Check" "$([ "$overall_health" = "🟢 Healthy" ] && echo "success" || echo "warning")" "$health_summary"

# Export final health check metrics
export_performance_metrics "enhanced_health_check" "/tmp/workflow_metrics.json"

print_message "$([ "$overall_health" = "🟢 Healthy" ] && echo "success" || echo "warning")" "Repository health check completed - Status: $overall_health"