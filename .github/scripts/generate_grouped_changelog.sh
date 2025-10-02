#!/usr/bin/env bash
# Generates a grouped `CHANGELOG.md` for the auto-release workflow.
#
# The `.github/workflows/auto-release.yml` workflow runs this script with the
# previous tag, new tag, and release type. It optionally passes a JSON payload
# of pull requests so that PR metadata can be merged with Git history. The
# script writes grouped sections (features, fixes, docs, other) to
# `CHANGELOG.md` and echoes the result for subsequent workflow steps.
set -euo pipefail

if [[ $# -lt 3 || $# -gt 4 ]]; then
  echo "Usage: $0 <previous-tag> <new-tag> <release-type> [prs-json-path]" >&2
  exit 1
fi

PREV_TAG="$1"
NEW_TAG="$2"
TYPE="$3"
PRS_JSON="${4:-prs.json}"
OUTPUT_FILE="CHANGELOG.md"

: > "$OUTPUT_FILE"

printf '## %s v%s\n\n' "${TYPE^}" "$NEW_TAG" >> "$OUTPUT_FILE"

echo "### 🚀 Features" >> "$OUTPUT_FILE"
if [[ -f "$PRS_JSON" ]]; then
  jq -r '.[] | select(.labels[]? == "feature") | "- \(.title) (#\(.number))"' "$PRS_JSON" >> "$OUTPUT_FILE" || true
fi
(
  git log "$PREV_TAG"..HEAD --pretty=format:"- %s" 2>/dev/null || true
) | grep -iE '^feat' | sed 's/^feat:? *//' >> "$OUTPUT_FILE" || true
if ! grep -q "-" "$OUTPUT_FILE"; then echo "_No new features_" >> "$OUTPUT_FILE"; fi

echo "" >> "$OUTPUT_FILE"
echo "### 🐛 Fixes" >> "$OUTPUT_FILE"
if [[ -f "$PRS_JSON" ]]; then
  jq -r '.[] | select(.labels[]? == "bug") | "- \(.title) (#\(.number))"' "$PRS_JSON" >> "$OUTPUT_FILE" || true
fi
(
  git log "$PREV_TAG"..HEAD --pretty=format:"- %s" 2>/dev/null || true
) | grep -iE '^fix' | sed 's/^fix:? *//' >> "$OUTPUT_FILE" || true
if ! grep -q "-" "$OUTPUT_FILE"; then echo "_No bug fixes_" >> "$OUTPUT_FILE"; fi

echo "" >> "$OUTPUT_FILE"
echo "### 📝 Docs" >> "$OUTPUT_FILE"
if [[ -f "$PRS_JSON" ]]; then
  jq -r '.[] | select(.labels[]? == "docs") | "- \(.title) (#\(.number))"' "$PRS_JSON" >> "$OUTPUT_FILE" || true
fi
(
  git log "$PREV_TAG"..HEAD --pretty=format:"- %s" 2>/dev/null || true
) | grep -iE '^docs' | sed 's/^docs:? *//' >> "$OUTPUT_FILE" || true
if ! grep -q "-" "$OUTPUT_FILE"; then echo "_No docs changes_" >> "$OUTPUT_FILE"; fi

echo "" >> "$OUTPUT_FILE"
echo "### 🔧 Other Changes" >> "$OUTPUT_FILE"
if [[ -f "$PRS_JSON" ]]; then
  jq -r '.[] | select(.labels[]? | in({"feature":1,"bug":1,"docs":1}) | not) | "- \(.title) (#\(.number))"' "$PRS_JSON" >> "$OUTPUT_FILE" || true
fi
(
  git log "$PREV_TAG"..HEAD --pretty=format:"- %s" 2>/dev/null || true
) | grep -vE '^(feat|fix|docs)' >> "$OUTPUT_FILE" || true
if ! grep -q "-" "$OUTPUT_FILE"; then echo "_None_" >> "$OUTPUT_FILE"; fi

echo "" >> "$OUTPUT_FILE"

cat "$OUTPUT_FILE"
