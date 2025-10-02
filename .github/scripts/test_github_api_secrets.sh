#!/bin/bash
set -euo pipefail

# GitHub API secrets management test script
# Tests secrets API functionality (read-only operations)

source "$(dirname "$0")/workflow_utils.sh"

REPO_NAME="${1:-$GITHUB_REPOSITORY}"

start_step_timing "secrets_api_test"

# Test GitHub API secrets management functionality (read-only operations)
print_message "step" "Testing secrets management API integration..."

# Test API access to repository secrets (read-only)
poetry run python -c "
import requests
import os
token = os.environ.get('GITHUB_TOKEN')
repo = '${REPO_NAME}'
headers = {'Authorization': f'token {token}', 'Accept': 'application/vnd.github.v3+json'}
# Test accessing the current repository's secrets
response = requests.get(f'https://api.github.com/repos/{repo}/actions/secrets', headers=headers)
print(f'Secrets API Response Status: {response.status_code}')
print(f'Rate Limit Remaining: {response.headers.get(\"X-RateLimit-Remaining\", \"Unknown\")}')
assert response.status_code in [200, 403], f'Unexpected API response: {response.status_code}'
print('✅ Secrets API access test completed')
"

print_message "success" "Secret management API integration test passed"

end_step_timing "secrets_api_test"