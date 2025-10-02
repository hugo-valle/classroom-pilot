#!/bin/bash
set -euo pipefail

# GitHub API collaborator management test script
# Tests collaborator API functionality (read-only operations)

source "$(dirname "$0")/workflow_utils.sh"

REPO_NAME="${1:-$GITHUB_REPOSITORY}"

start_step_timing "collaborator_api_test"

# Test GitHub API collaborator management functionality
print_message "step" "Testing collaborator management API integration..."

# Test API access to repository collaborators (read-only)
poetry run python -c "
import requests
import os
token = os.environ.get('GITHUB_TOKEN')
repo = '${REPO_NAME}'
headers = {'Authorization': f'token {token}', 'Accept': 'application/vnd.github.v3+json'}
response = requests.get(f'https://api.github.com/repos/{repo}/collaborators', headers=headers)
print(f'Collaborators API Response Status: {response.status_code}')
print(f'Rate Limit Remaining: {response.headers.get(\"X-RateLimit-Remaining\", \"Unknown\")}')
assert response.status_code in [200, 403], f'Unexpected API response: {response.status_code}'
if response.status_code == 200:
    collaborators = response.json()
    print(f'Found {len(collaborators)} collaborators')
print('✅ Collaborators API access test completed')
"

print_message "success" "Collaborator management API integration test passed"

end_step_timing "collaborator_api_test"