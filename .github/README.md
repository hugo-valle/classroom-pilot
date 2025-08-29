# GitHub Actions Workflows

This directory contains automated workflows for the GitHub Classroom Tools project.

## 🚀 Release Workflow (`release.yml`)

**Triggered by**: Pushing a version tag (e.g., `v1.0.0-alpha.2`)

### What it does:
1. **🔍 Validates** the tag format and extracts version information
2. **🧪 Tests** all scripts across multiple shell environments (bash, zsh)
3. **🛡️ Security scans** using Shellcheck and secret detection
4. **📝 Generates** release notes from CHANGELOG.md or git history
5. **🎉 Creates** a GitHub Release with appropriate pre-release flags
6. **📝 Updates** CHANGELOG.md for beta/stable releases
7. **📢 Notifies** on success/failure

### Supported Version Formats:
- **Stable**: `v1.0.0`, `v1.2.3`
- **Alpha**: `v1.0.0-alpha.1`, `v1.0.0-alpha.2`
- **Beta**: `v1.0.0-beta.1`, `v1.0.0-beta.2`
- **Release Candidate**: `v1.0.0-rc.1`

### Usage:
```bash
# Create and push a tag
git tag v1.0.0-alpha.2
git push origin v1.0.0-alpha.2

# The workflow automatically:
# - Runs tests
# - Creates GitHub Release
# - Marks as pre-release for alpha/beta/rc
```

## 🔄 CI Workflow (`ci.yml`)

**Triggered by**: Push to `main`/`develop` branches, Pull Requests

### What it does:
1. **🧪 Tests** script syntax across bash and zsh
2. **🔍 Lints** scripts with Shellcheck
3. **🛡️ Security** scanning for secrets
4. **📚 Validates** documentation format

### Usage:
Runs automatically on every push and PR to ensure code quality.

## 🔄 Auto Update Workflow (`auto-update.yml`)

**Triggered by**: Weekly schedule (Sundays 2 AM UTC) or manual dispatch

### What it does:
1. **📦 Checks** for dependency updates
2. **🏥 Performs** repository health checks
3. **📊 Reports** repository statistics

### Usage:
```bash
# Trigger manually via GitHub Actions tab
# Or runs automatically weekly
```

## 🎯 Release Process

Follow this process for creating releases:

### Alpha Release:
```bash
# 1. Create feature branch and make changes
git checkout -b feature/new-feature
# ... make changes ...
git commit -m "feat: add new feature"

# 2. Merge to main via PR
# 3. Create alpha tag
git checkout main
git pull origin main
git tag v1.0.0-alpha.2
git push origin v1.0.0-alpha.2

# 4. Workflow automatically creates pre-release
```

### Beta Release:
```bash
# 1. When alpha is stable, create beta
git tag v1.0.0-beta.1
git push origin v1.0.0-beta.1

# 2. Workflow creates pre-release and updates CHANGELOG
```

### Stable Release:
```bash
# 1. When beta is stable, create stable release
git tag v1.0.0
git push origin v1.0.0

# 2. Workflow creates final release and updates CHANGELOG
```

## 📋 Workflow Features

### Automatic Release Notes
- Extracts from CHANGELOG.md if version section exists
- Falls back to git log between tags
- Customized templates for alpha/beta/stable releases

### Security & Quality
- Shellcheck linting with configurable severity
- Secret scanning with TruffleHog
- Multi-shell testing (bash, zsh)

### Smart Version Detection
- Automatically detects release type from tag format
- Sets appropriate pre-release flags
- Generates contextual release notes

### Documentation Maintenance
- Validates CHANGELOG.md format
- Updates changelog for non-alpha releases
- Maintains version history

## 🔧 Configuration

### Required Secrets
- `GITHUB_TOKEN` (automatically provided by GitHub)

### Optional Customization
Edit the workflows to:
- Add more test environments
- Include additional security scanners
- Customize release note templates
- Add deployment steps

## 🚀 Next Steps

After setting up these workflows:

1. **Test the CI**: Create a PR to verify CI workflow
2. **Create Alpha Release**: Tag `v1.0.0-alpha.2` to test release workflow
3. **Monitor**: Check GitHub Actions tab for workflow runs
4. **Iterate**: Refine workflows based on your needs

The workflows are designed to be robust and provide comprehensive automation for your release process! 🎉
