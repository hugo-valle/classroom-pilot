#!/usr/bin/env bash
# Reports current GitHub Actions usage for the auto-update workflow.
#
# The auto-update workflow uses this script to print the jobs' actions so that
# maintainers can spot which pinned versions may need manual upgrading.
set -euo pipefail

echo "🔄 Checking for GitHub Actions updates..."
echo "Current GitHub Actions versions:"
grep -r "uses:" .github/workflows/ || true
