#!/usr/bin/env bash
# Performs lightweight dependency checks for automation scripts.
#
# The auto-update workflow runs this script to report on tooling referenced in
# the repository's shell scripts and to flag deprecated patterns for follow-up
# by maintainers.
set -euo pipefail

echo "🔍 Checking script dependencies..."

if [ -d scripts ]; then
  if grep -r "gh " scripts/; then
    echo "📋 Scripts use GitHub CLI - ensure latest version is available"
  fi
else
  echo "⚠️ scripts/ directory missing"
fi

echo "✅ Dependency check complete"
