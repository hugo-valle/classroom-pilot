#!/bin/bash
set -euo pipefail

# GitHub API repository discovery test script
# Tests API functionality for repository operations

source "$(dirname "$0")/workflow_utils.sh"

start_step_timing "repo_discovery_api_test"

# Test GitHub API repository discovery functionality
print_message "step" "Testing repository discovery API integration..."

# Use actual GitHub API to test repository discovery (read-only operations)
poetry run python -c "
import requests
import os
token = os.environ.get('GITHUB_TOKEN')
headers = {'Authorization': f'token {token}', 'Accept': 'application/vnd.github.v3+json'}
response = requests.get('https://api.github.com/user/repos', headers=headers, params={'per_page': 5})
print(f'API Response Status: {response.status_code}')
print(f'Rate Limit Remaining: {response.headers.get(\"X-RateLimit-Remaining\", \"Unknown\")}')
assert response.status_code == 200, f'API request failed with status {response.status_code}'
repos = response.json()
print(f'Successfully discovered {len(repos)} repositories')
"

print_message "success" "Repository discovery API integration test passed"

end_step_timing "repo_discovery_api_test"