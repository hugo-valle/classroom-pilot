# Installation

Get Classroom Pilot up and running in minutes.

## 📦 Install from PyPI (Recommended)

```bash
# Install the latest version
pip install classroom-pilot

# Verify installation
classroom-pilot --help
```

## 🔧 Development Installation

### Using Poetry

```bash
# Clone repository
git clone https://github.com/hugo-valle/classroom-pilot.git
cd classroom-pilot

# Install with Poetry
poetry install
poetry shell

# Verify installation
classroom-pilot --help
```

### Using pip (Development Mode)

```bash
# Clone repository
git clone https://github.com/hugo-valle/classroom-pilot.git
cd classroom-pilot

# Install in editable mode
pip install -e .

# Verify installation
classroom-pilot --help
```

## ⚙️ Requirements

- **Python 3.10+** (3.11+ recommended)
- **Git** for repository operations
- **GitHub CLI** (optional, for enhanced authentication)

## 🔐 Authentication Setup

### GitHub Token

Create a GitHub personal access token for classroom-pilot:

1. Go to [GitHub Settings → Personal Access Tokens](https://github.com/settings/tokens)
2. Generate a new token with these scopes:
   - `repo` (for repository access)
   - `admin:org` (for organization management)
   - `write:org` (for secret management)
3. Save the token securely using the centralized token manager:

```bash
# Create centralized token config
mkdir -p ~/.config/classroom-pilot
cat > ~/.config/classroom-pilot/token_config.json << 'EOF'
{
    "github_token": "ghp_your_token_here",
    "username": "your_username",
    "scopes": ["repo", "admin:org", "write:org"],
    "expires_at": null
}
EOF
chmod 600 ~/.config/classroom-pilot/token_config.json

# Or set as environment variable for CI/automation
export GITHUB_TOKEN="ghp_your_token_here"
```

### GitHub CLI (Optional)

For enhanced authentication, install GitHub CLI:

```bash
# Install GitHub CLI
# macOS
brew install gh

# Ubuntu/Debian
sudo apt install gh

# Windows
winget install GitHub.cli

# Authenticate
gh auth login
```

## ✅ Verify Installation

```bash
# Check version
classroom-pilot version

# Test basic functionality
classroom-pilot --help

# Test command groups
classroom-pilot assignments --help
classroom-pilot repos --help
classroom-pilot secrets --help
classroom-pilot automation --help
```

## 🚀 Next Steps

- [Quick Start Guide](quick-start.md) - Get up and running
- [Configuration](configuration.md) - Set up your first assignment
- [CLI Reference](../cli/overview.md) - Complete command documentation
