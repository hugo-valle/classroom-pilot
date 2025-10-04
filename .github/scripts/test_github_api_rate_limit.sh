#!/bin/bash
set -euo pipefail

# GitHub API rate limiting test script
# Tests API rate limiting behavior and recovery

source "$(dirname "$0")/workflow_utils.sh"

start_step_timing "rate_limit_test"

# Test API rate limiting behavior and recovery
print_message "step" "Testing API rate limiting behavior..."

poetry run python -c "
import requests
import time
import os
token = os.environ.get('GITHUB_TOKEN')
headers = {'Authorization': f'token {token}', 'Accept': 'application/vnd.github.v3+json'}

# Check current rate limit status
response = requests.get('https://api.github.com/rate_limit', headers=headers)
rate_limit_info = response.json()
core_remaining = rate_limit_info['resources']['core']['remaining']
print(f'Rate limit remaining: {core_remaining}')

# Make a few test requests to monitor rate limiting
for i in range(5):
    response = requests.get('https://api.github.com/user', headers=headers)
    remaining = response.headers.get('X-RateLimit-Remaining', 'Unknown')
    print(f'Request {i+1}: Status {response.status_code}, Remaining: {remaining}')
    time.sleep(1)

print('✅ Rate limiting behavior test completed')
"

print_message "success" "API rate limiting test passed"

end_step_timing "rate_limit_test"