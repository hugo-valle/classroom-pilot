# GitHub Secrets Management

Comprehensive secret management for GitHub Classroom assignments through the modern Python CLI interface.

## 🎯 Overview

Classroom Pilot provides robust secret management capabilities for:

- **Automated Secret Distribution** - Add secrets across multiple student repositories
- **Secure Token Management** - Handle authentication tokens safely
- **Batch Operations** - Manage secrets for entire classrooms efficiently
- **Secret Rotation** - Update and rotate secrets across repositories
- **Access Control** - Manage secret visibility and permissions

## 📦 Installation

```bash
# Install from PyPI
pip install classroom-pilot

# Verify installation
classroom-pilot --help
```

## 🚀 Quick Setup

### 1. Configure Centralized Token

```bash
# Create centralized token config (recommended)
mkdir -p ~/.config/classroom-pilot
cat > ~/.config/classroom-pilot/token_config.json << 'EOF'
{
    "github_token": "ghp_your_github_token_here",
    "username": "instructor",
    "scopes": ["repo", "admin:org", "write:org"],
    "expires_at": null
}
EOF
chmod 600 ~/.config/classroom-pilot/token_config.json

# Or set environment variable for CI/automation
export GITHUB_TOKEN="ghp_your_github_token_here"
```

### 2. Configure Assignment

```bash
# Create assignment configuration
cat > assignment.conf << 'EOF'
CLASSROOM_URL="https://classroom.github.com/classrooms/123/assignments/homework1"
TEMPLATE_REPO_URL="https://github.com/instructor/homework1-template"
SECRETS_CONFIG="
API_KEY:API key for external service:true
GRADING_TOKEN:Token for automated grading:true
DATABASE_URL:Database connection string:false
"
EOF
```

### 3. Distribute Secrets

```bash
# Add secrets to all student repositories
classroom-pilot secrets add --config assignment.conf

# Preview what would be done first
classroom-pilot --dry-run secrets add --config assignment.conf
```

## 🔧 Secret Management Commands

### Adding Secrets

```bash
# Add all configured secrets
classroom-pilot secrets add --config assignment.conf

# Add specific secrets
classroom-pilot secrets add --config assignment.conf --secrets "API_KEY,GRADING_TOKEN"

# Add secrets with custom values
API_KEY="custom_value" classroom-pilot secrets add --config assignment.conf --secrets "API_KEY"
```

### Removing Secrets

```bash
# Remove specific secrets
classroom-pilot secrets remove --config assignment.conf --secrets "OLD_TOKEN"

# Remove all configured secrets
classroom-pilot secrets remove --config assignment.conf

# Preview removal (dry-run)
classroom-pilot --dry-run secrets remove --config assignment.conf --secrets "OLD_TOKEN"
```

### Listing Secrets

```bash
# List secrets in all repositories
classroom-pilot secrets list --config assignment.conf

# List secrets with details
classroom-pilot --verbose secrets list --config assignment.conf
```

## ⚙️ Configuration

### Secret Configuration Format

Define secrets in your `assignment.conf` file:

```bash
# Basic secret list
SECRETS_LIST="API_KEY,DATABASE_URL,GRADING_TOKEN"

# Secret files (for complex secrets)
SECRET_API_KEY_FILE="api_key.txt"
SECRET_DATABASE_URL_FILE="database_url.txt"

# Secret descriptions (for documentation)
SECRET_API_KEY_DESCRIPTION="API key for external service"
SECRET_DATABASE_URL_DESCRIPTION="Database connection string"
```

### Environment Variable Secrets

Use environment variables for sensitive values:

```bash
# Set secrets via environment variables
export API_KEY="your_api_key_here"
export DATABASE_URL="postgresql://user:pass@host:5432/db"
export GRADING_TOKEN="grading_token_value"

# Run secret management
classroom-pilot secrets add --config assignment.conf
```

### Secret File Management

Store secrets in separate files for security:

```bash
# Create secret files
echo "your_api_key" > api_key.txt
echo "postgresql://..." > database_url.txt
echo "grading_token" > grading_token.txt

# Set secure permissions
chmod 600 *.txt

# Configure in assignment.conf
SECRET_API_KEY_FILE="api_key.txt"
SECRET_DATABASE_URL_FILE="database_url.txt"
SECRET_GRADING_TOKEN_FILE="grading_token.txt"
```

## 🎯 Advanced Secret Management

### Secret Rotation

Automate secret rotation across all repositories:

```bash
# Step 1: Generate new secrets
new_api_key=$(generate_new_api_key)
new_token=$(generate_new_token)

# Step 2: Update environment
export API_KEY="$new_api_key"
export GRADING_TOKEN="$new_token"

# Step 3: Distribute new secrets
classroom-pilot secrets add --config assignment.conf --secrets "API_KEY,GRADING_TOKEN"

# Step 4: Verify distribution
classroom-pilot secrets list --config assignment.conf
```

### Conditional Secret Management

Apply secrets based on conditions:

```bash
# Add secrets only to specific repositories
EXCLUDE_REPOS="template,instructor-solution" classroom-pilot secrets add --config assignment.conf

# Add different secrets for different assignments
if [[ "$ASSIGNMENT_TYPE" == "final" ]]; then
    SECRETS_LIST="API_KEY,FINAL_EXAM_TOKEN" classroom-pilot secrets add --config assignment.conf
else
    SECRETS_LIST="API_KEY,HOMEWORK_TOKEN" classroom-pilot secrets add --config assignment.conf
fi
```

### Batch Secret Operations

Manage secrets across multiple assignments:

```bash
#!/bin/bash
# Batch secret management script

ASSIGNMENTS=("homework1" "homework2" "midterm" "final")
NEW_API_KEY="new_secure_api_key"

for assignment in "${ASSIGNMENTS[@]}"; do
    echo "Updating secrets for $assignment..."
    
    # Set assignment-specific configuration
    config_file="assignment-${assignment}.conf"
    
    # Update API key
    API_KEY="$NEW_API_KEY" classroom-pilot secrets add --config "$config_file" --secrets "API_KEY"
    
    echo "Completed $assignment"
done
```

## 🛡️ Security Best Practices

### Token Security

```bash
# Create dedicated tokens for secret management
# Required permissions:
# - repo (for repository access)
# - admin:org (for organization secrets)
# - secrets (for repository secrets)

# Store tokens securely
echo "ghp_token" > secure_token.txt
chmod 600 secure_token.txt

# Use token files instead of environment variables
GITHUB_TOKEN_FILE="secure_token.txt"
```

### Secret Validation

```bash
# Validate secrets before distribution
classroom-pilot --dry-run secrets add --config assignment.conf

# Check secret format and permissions
classroom-pilot --verbose secrets add --config assignment.conf

# Verify secret distribution
classroom-pilot secrets list --config assignment.conf
```

### Access Control

```bash
# Limit secret access to specific repositories
EXCLUDE_REPOS="public-template,instructor-repo" classroom-pilot secrets add --config assignment.conf

# Use different tokens for different secret types
GITHUB_TOKEN_FILE="grading_token.txt" classroom-pilot secrets add --config assignment.conf --secrets "GRADING_TOKEN"
GITHUB_TOKEN_FILE="api_token.txt" classroom-pilot secrets add --config assignment.conf --secrets "API_KEY"
```

## 📊 Monitoring & Auditing

### Secret Audit

```bash
# List all secrets across repositories
classroom-pilot secrets list --config assignment.conf > secret_audit.txt

# Check secret distribution status
classroom-pilot --verbose secrets list --config assignment.conf

# Verify specific secrets
classroom-pilot secrets list --config assignment.conf --secrets "API_KEY,GRADING_TOKEN"
```

### Distribution Monitoring

```bash
# Monitor secret distribution in real-time
classroom-pilot --verbose secrets add --config assignment.conf

# Check for distribution failures
classroom-pilot secrets add --config assignment.conf 2>&1 | grep -i error

# Validate distribution success
classroom-pilot secrets list --config assignment.conf | grep -c "API_KEY"
```

## 🔄 Integration with Automation

### Automated Secret Management

```bash
# Setup automated secret rotation
cat > secret-rotation.conf << 'EOF'
CLASSROOM_URL="https://classroom.github.com/classrooms/123/assignments/homework1"
GITHUB_TOKEN_FILE="automation_token.txt"
SECRETS_LIST="API_KEY,DATABASE_URL"

# Automation schedules
AUTOMATION_SCHEDULE_SECRETS="0 3 * * 1"  # Monday at 3 AM
AUTOMATION_SCHEDULE_ROTATION="0 2 1 * *" # First day of month at 2 AM
EOF

classroom-pilot automation scheduler setup --config secret-rotation.conf
```

### Workflow Integration

```bash
# Integrate secret management with complete workflow
classroom-pilot assignments orchestrate --config assignment.conf

# This automatically:
# 1. Discovers student repositories
# 2. Distributes configured secrets
# 3. Validates secret distribution
# 4. Reports success/failure status
```

## 🔍 Troubleshooting

### Common Issues

1. **Authentication Failures**:
   ```bash
   # Check token permissions
   classroom-pilot --verbose secrets add --config assignment.conf
   ```

2. **Secret Not Found**:
   ```bash
   # Verify secret configuration
   classroom-pilot --dry-run secrets add --config assignment.conf
   ```

3. **Distribution Failures**:
   ```bash
   # Check repository access
   classroom-pilot repos fetch --config assignment.conf
   ```

### Debug Mode

```bash
# Enable detailed logging
classroom-pilot --verbose secrets add --config assignment.conf

# Dry-run with maximum detail
classroom-pilot --dry-run --verbose secrets add --config assignment.conf
```

## 📚 Related Documentation

- **[Assignment Orchestrator](assignment-orchestrator.md)** - Complete workflow automation
- **[Automation Suite](automation-suite.md)** - Complete automation capabilities
- **[Cron Automation](cron-automation.md)** - Scheduled automation
- **[Main CLI Reference](../README.md)** - Complete command documentation

## 💡 Examples & Use Cases

### Exam Environment Setup

```bash
# Setup secure exam environment
cat > exam-secrets.conf << 'EOF'
CLASSROOM_URL="https://classroom.github.com/classrooms/123/assignments/midterm"
GITHUB_TOKEN_FILE="exam_token.txt"
SECRETS_LIST="EXAM_API_KEY,GRADING_DATABASE,SECURE_TOKEN"
EXCLUDE_REPOS="template,instructor-solution"
EOF

# Distribute exam secrets
classroom-pilot secrets add --config exam-secrets.conf

# Verify distribution
classroom-pilot secrets list --config exam-secrets.conf
```

### API Key Management

```bash
# Rotate API keys for new semester
OLD_KEY="old_api_key_value"
NEW_KEY="new_api_key_value"

# Remove old key
API_KEY="$OLD_KEY" classroom-pilot secrets remove --config assignment.conf --secrets "API_KEY"

# Add new key
API_KEY="$NEW_KEY" classroom-pilot secrets add --config assignment.conf --secrets "API_KEY"

# Verify update
classroom-pilot secrets list --config assignment.conf --secrets "API_KEY"
```

---

GitHub Secrets Management provides secure, efficient handling of sensitive information across GitHub Classroom assignments.
