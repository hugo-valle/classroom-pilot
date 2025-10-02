#!/usr/bin/env bash
# Runs a lightweight repository health audit for the auto-update workflow.
#
# The auto-update workflow surfaces the presence of required automation files
# and basic repository statistics with this script so maintainers can spot
# missing assets without performing manual checks.
set -euo pipefail

echo "🏥 Performing repository health check..."

echo "📂 Checking file structure..."
required_files=(
  "scripts/setup-assignment.sh"
  "scripts/assignment-orchestrator.sh"
  "scripts/fetch-student-repos.sh"
  "docs/CHANGELOG.md"
)

for file in "${required_files[@]}"; do
  if [ -f "$file" ]; then
    echo "✅ $file exists"
  else
    echo "❌ $file missing"
  fi
done

echo "📊 Repository statistics:"
if [ -d scripts ]; then
  script_total=$(find scripts/ -name "*.sh" | wc -l)
else
  script_total=0
fi

if [ -d docs ]; then
  docs_total=$(find docs/ -name "*.md" | wc -l)
else
  docs_total=0
fi

workflow_total=$(find .github/workflows/ -name "*.yml" | wc -l)

echo "- Scripts: ${script_total}"
echo "- Documentation files: ${docs_total}"
echo "- Workflow files: ${workflow_total}"

echo "✅ Health check complete"
