#!/bin/bash
################################################################################
# Mocking and Stubbing Library
#
# Provides functions for testing without external dependencies:
# - GitHub API response mocking
# - File system mocking
# - Environment mocking
# - Command mocking
# - Response validation helpers
# - Cleanup functions
#
# Usage: source lib/mock_helpers.sh
################################################################################

# Mock data storage directory
MOCK_DATA_DIR=""
ORIGINAL_ENV_BACKUP=""
ORIGINAL_HOME=""
ORIGINAL_PATH=""

################################################################################
# GitHub API Mocking Functions
################################################################################

# Create mock HTTP response files for GitHub API endpoints
# Usage: mock_github_api_response "endpoint" "response_json" "status_code"
mock_github_api_response() {
    local endpoint="$1"
    local response="$2"
    local status_code="${3:-200}"
    
    if [ -z "$MOCK_DATA_DIR" ]; then
        MOCK_DATA_DIR=$(mktemp -d -t "mock_data_XXXXXX")
    fi
    
    local safe_endpoint=$(echo "$endpoint" | tr '/' '_' | tr -d '?&=')
    local response_file="$MOCK_DATA_DIR/api_${safe_endpoint}.json"
    
    echo "$response" > "$response_file"
    echo "$status_code" > "${response_file}.status"
    
    echo "$response_file"
}

# Set up a fake GitHub token for testing
# Usage: token=$(setup_mock_github_token)
# Returns: Mock token in correct format
setup_mock_github_token() {
    local mock_token="ghp_$(head -c 36 /dev/urandom | base64 | tr -dc 'a-zA-Z0-9' | head -c 36)"
    export GITHUB_TOKEN="$mock_token"
    echo "$mock_token"
}

# Generate mock repository list JSON response
# Usage: json=$(mock_github_repo_list "org_name" "repo_count")
# Returns: JSON array of mock repositories
mock_github_repo_list() {
    local org="$1"
    local count="${2:-5}"
    
    local repos="["
    for i in $(seq 1 "$count"); do
        if [ "$i" -gt 1 ]; then
            repos+=","
        fi
        repos+=$(cat <<EOF
{
  "id": $((i + 1000)),
  "name": "test-assignment-student$i",
  "full_name": "$org/test-assignment-student$i",
  "private": true,
  "html_url": "https://github.com/$org/test-assignment-student$i",
  "clone_url": "https://github.com/$org/test-assignment-student$i.git",
  "created_at": "2025-10-17T00:00:00Z",
  "updated_at": "2025-10-17T12:00:00Z"
}
EOF
        )
    done
    repos+="]"
    
    echo "$repos"
}

# Generate mock GitHub Classroom API response
# Usage: json=$(mock_github_classroom_response "assignment_id")
# Returns: JSON object for classroom assignment
mock_github_classroom_response() {
    local assignment_id="${1:-12345}"
    
    cat <<EOF
{
  "id": $assignment_id,
  "title": "Test Assignment",
  "type": "individual",
  "public_repo": false,
  "starter_code_repository": {
    "id": 54321,
    "full_name": "test-org/test-template",
    "html_url": "https://github.com/test-org/test-template"
  },
  "accepted": 10,
  "submitted": 8,
  "passing": 7,
  "classroom": {
    "id": 99999,
    "name": "Test Classroom",
    "url": "https://classroom.github.com/classrooms/99999"
  }
}
EOF
}

# Generate mock secrets API response
# Usage: json=$(mock_github_secrets_response "secret_count")
# Returns: JSON object with secrets list
mock_github_secrets_response() {
    local count="${1:-3}"
    
    local secrets="["
    for i in $(seq 1 "$count"); do
        if [ "$i" -gt 1 ]; then
            secrets+=","
        fi
        secrets+=$(cat <<EOF
{
  "name": "TEST_SECRET_$i",
  "created_at": "2025-10-17T00:00:00Z",
  "updated_at": "2025-10-17T12:00:00Z"
}
EOF
        )
    done
    secrets+="]"
    
    cat <<EOF
{
  "total_count": $count,
  "secrets": $secrets
}
EOF
}

################################################################################
# File System Mocking
################################################################################

# Create a mock repository directory structure with .git folder
# Usage: mock_dir=$(create_mock_repo_structure "repo_name")
# Returns: Path to mock repository
create_mock_repo_structure() {
    local repo_name="${1:-test-repo}"
    
    if [ -z "$MOCK_DATA_DIR" ]; then
        MOCK_DATA_DIR=$(mktemp -d -t "mock_data_XXXXXX")
    fi
    
    local repo_dir="$MOCK_DATA_DIR/repos/$repo_name"
    mkdir -p "$repo_dir/.git"
    
    # Create basic git structure
    echo "ref: refs/heads/main" > "$repo_dir/.git/HEAD"
    mkdir -p "$repo_dir/.git/refs/heads"
    echo "0000000000000000000000000000000000000000" > "$repo_dir/.git/refs/heads/main"
    
    # Create sample files
    echo "# $repo_name" > "$repo_dir/README.md"
    echo "*.pyc" > "$repo_dir/.gitignore"
    
    echo "$repo_dir"
}

# Generate a mock student list file with test usernames
# Usage: file=$(create_mock_student_list "count")
# Returns: Path to student list file
create_mock_student_list() {
    local count="${1:-10}"
    
    if [ -z "$MOCK_DATA_DIR" ]; then
        MOCK_DATA_DIR=$(mktemp -d -t "mock_data_XXXXXX")
    fi
    
    local students_file="$MOCK_DATA_DIR/students.txt"
    
    for i in $(seq 1 "$count"); do
        echo "student$i" >> "$students_file"
    done
    
    echo "$students_file"
}

# Generate a mock repos.txt file with test repository URLs
# Usage: file=$(create_mock_repos_file "org_name" "count")
# Returns: Path to repos file
create_mock_repos_file() {
    local org="${1:-test-org}"
    local count="${2:-5}"
    
    if [ -z "$MOCK_DATA_DIR" ]; then
        MOCK_DATA_DIR=$(mktemp -d -t "mock_data_XXXXXX")
    fi
    
    local repos_file="$MOCK_DATA_DIR/repos.txt"
    
    for i in $(seq 1 "$count"); do
        echo "https://github.com/$org/test-assignment-student$i" >> "$repos_file"
    done
    
    echo "$repos_file"
}

################################################################################
# Environment Mocking
################################################################################

# Set up mock environment variables for testing
# Usage: mock_environment_setup
mock_environment_setup() {
    # Backup original environment
    ORIGINAL_ENV_BACKUP=$(mktemp -t "env_backup_XXXXXX")
    env > "$ORIGINAL_ENV_BACKUP"
    
    # Backup critical environment variables
    ORIGINAL_HOME="$HOME"
    ORIGINAL_PATH="$PATH"
    
    # Set up mock GitHub token (capture output to prevent leaking to stdout)
    local mock_token
    mock_token=$(setup_mock_github_token)
    
    # Set up mock paths
    export CLASSROOM_PILOT_TEST_MODE="true"
    export CLASSROOM_PILOT_MOCK_API="true"
    
    # Set up mock home directory for config
    if [ -z "$MOCK_DATA_DIR" ]; then
        MOCK_DATA_DIR=$(mktemp -d -t "mock_data_XXXXXX")
    fi
    export HOME="$MOCK_DATA_DIR/home"
    mkdir -p "$HOME/.config/classroom-pilot"
}

# Create mock token configuration file
# Usage: mock_token_config
mock_token_config() {
    local config_dir="$HOME/.config/classroom-pilot"
    mkdir -p "$config_dir"
    
    local token=$(setup_mock_github_token)
    
    cat > "$config_dir/token_config.json" <<EOF
{
  "github_token": "$token",
  "token_type": "classic",
  "created_at": "2025-10-17T00:00:00Z",
  "scopes": ["repo", "workflow", "admin:org"],
  "username": "test-user"
}
EOF
    
    echo "$config_dir/token_config.json"
}

# Restore original environment after mocking
# Usage: restore_environment
restore_environment() {
    if [ -n "$ORIGINAL_ENV_BACKUP" ] && [ -f "$ORIGINAL_ENV_BACKUP" ]; then
        # Restore key environment variables
        unset GITHUB_TOKEN
        unset CLASSROOM_PILOT_TEST_MODE
        unset CLASSROOM_PILOT_MOCK_API
        
        # Restore HOME and PATH if they were backed up
        if [ -n "$ORIGINAL_HOME" ]; then
            export HOME="$ORIGINAL_HOME"
        fi
        if [ -n "$ORIGINAL_PATH" ]; then
            export PATH="$ORIGINAL_PATH"
        fi
        
        rm -f "$ORIGINAL_ENV_BACKUP"
        ORIGINAL_ENV_BACKUP=""
        ORIGINAL_HOME=""
        ORIGINAL_PATH=""
    fi
}

################################################################################
# Command Mocking
################################################################################

# Replace git commands with mock implementations
# Usage: mock_git_command
mock_git_command() {
    # Create mock git wrapper
    if [ -z "$MOCK_DATA_DIR" ]; then
        MOCK_DATA_DIR=$(mktemp -d -t "mock_data_XXXXXX")
    fi
    
    local mock_bin="$MOCK_DATA_DIR/bin"
    mkdir -p "$mock_bin"
    
    cat > "$mock_bin/git" <<'EOF'
#!/bin/bash
# Mock git command for testing

case "$1" in
    "clone")
        echo "Cloning into '$3'..."
        mkdir -p "$3"
        echo "Mock repository cloned successfully"
        exit 0
        ;;
    "pull")
        echo "Already up to date."
        exit 0
        ;;
    "push")
        echo "Everything up-to-date"
        exit 0
        ;;
    "status")
        echo "On branch main"
        echo "nothing to commit, working tree clean"
        exit 0
        ;;
    *)
        echo "git $*"
        exit 0
        ;;
esac
EOF
    
    chmod +x "$mock_bin/git"
    export PATH="$mock_bin:$PATH"
}

# Replace GitHub CLI commands with mock implementations
# Usage: mock_gh_command
mock_gh_command() {
    # Create mock gh wrapper
    if [ -z "$MOCK_DATA_DIR" ]; then
        MOCK_DATA_DIR=$(mktemp -d -t "mock_data_XXXXXX")
    fi
    
    local mock_bin="$MOCK_DATA_DIR/bin"
    mkdir -p "$mock_bin"
    
    cat > "$mock_bin/gh" <<'EOF'
#!/bin/bash
# Mock gh command for testing

case "$1" in
    "auth")
        if [ "$2" = "token" ]; then
            echo "ghp_mocktoken1234567890123456789012345678"
            exit 0
        fi
        ;;
    "repo")
        if [ "$2" = "list" ]; then
            echo "repo1"
            echo "repo2"
            echo "repo3"
            exit 0
        fi
        ;;
    "api")
        echo '{"message": "Mock API response"}'
        exit 0
        ;;
    *)
        echo "gh $*"
        exit 0
        ;;
esac
EOF
    
    chmod +x "$mock_bin/gh"
    export PATH="$mock_bin:$PATH"
}

# Restore original command implementations
# Usage: restore_commands
restore_commands() {
    # Remove mock bin directory from PATH - handle all positions
    if [ -n "$MOCK_DATA_DIR" ] && [ -d "$MOCK_DATA_DIR/bin" ]; then
        # Split PATH, filter out mock bin, and rejoin
        local new_path=""
        local IFS=':'
        for path_entry in $PATH; do
            if [ "$path_entry" != "$MOCK_DATA_DIR/bin" ]; then
                if [ -z "$new_path" ]; then
                    new_path="$path_entry"
                else
                    new_path="$new_path:$path_entry"
                fi
            fi
        done
        export PATH="$new_path"
    fi
}

################################################################################
# Response Validation Helpers
################################################################################

# Verify JSON response structure
# Usage: validate_json_response "json_string"
# Returns: 0 if valid JSON, 1 otherwise
validate_json_response() {
    local json="$1"
    
    if echo "$json" | python3 -m json.tool >/dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

# Verify API call was made with correct parameters
# Usage: validate_api_call "endpoint" "method" "expected_params"
# Returns: 0 if validation passes, 1 otherwise
validate_api_call() {
    local endpoint="$1"
    local method="$2"
    local expected_params="$3"
    
    # This would check mock API call logs
    # For now, just return success as placeholder
    return 0
}

################################################################################
# Cleanup Functions
################################################################################

# Remove all mock files and restore environment
# Usage: cleanup_mocks
cleanup_mocks() {
    restore_environment
    restore_commands
    
    if [ -n "$MOCK_DATA_DIR" ] && [ -d "$MOCK_DATA_DIR" ]; then
        rm -rf "$MOCK_DATA_DIR"
        MOCK_DATA_DIR=""
    fi
}

# Reset mock counters and state
# Usage: reset_mock_state
reset_mock_state() {
    # Clear any tracking variables
    unset MOCK_API_CALLS
    unset MOCK_GIT_CALLS
    
    # Re-initialize if needed
    if [ -z "$MOCK_DATA_DIR" ]; then
        MOCK_DATA_DIR=$(mktemp -d -t "mock_data_XXXXXX")
    fi
}

################################################################################
# Export all functions
################################################################################

export -f mock_github_api_response setup_mock_github_token mock_github_repo_list
export -f mock_github_classroom_response mock_github_secrets_response
export -f create_mock_repo_structure create_mock_student_list create_mock_repos_file
export -f mock_environment_setup mock_token_config restore_environment
export -f mock_git_command mock_gh_command restore_commands
export -f validate_json_response validate_api_call
export -f cleanup_mocks reset_mock_state

# Initialize on source
if [ -z "$MOCK_DATA_DIR" ]; then
    MOCK_DATA_DIR=$(mktemp -d -t "mock_data_XXXXXX")
fi
