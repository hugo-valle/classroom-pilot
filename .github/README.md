# 🔄 GitHub Actions Workflows

This directory contains all GitHub Actions workflows for the `gh_classroom_tools` repository. Each workflow serves a specific purpose in our CI/CD pipeline and repository management.

## � Complete Workflow Suite

| Workflow | Trigger | Purpose | Status |
|----------|---------|---------|--------|
| [🤖 auto-release.yml](#-automated-release) | Push to `main` | Quick automated releases from feature branches | ✅ Active |
| [🚀 release.yml](#-official-release) | Git tags (`v*.*.*`) | Official production releases with full validation | ✅ Active |
| [🔍 branch-name-check.yml](#-branch-name-check) | PR creation/updates | Enforce branch naming conventions | ✅ Active |
| [🛡️ branch-protection.yml](#️-branch-protection) | Manual dispatch | Apply protection rules to main branch | ✅ Active |
| [🧪 ci.yml](#-continuous-integration) | PR/Push events | Continuous integration testing | ✅ Active |
| [🔄 auto-update.yml](#-automated-updates) | Weekly schedule | Automated dependency updates | ✅ Active |

---

## 🤖 Automated Release

**File**: [`workflows/auto-release.yml`](./workflows/auto-release.yml)

### Purpose
Automatically creates releases when feature branches are merged to the main branch. Designed for quick development iterations and continuous deployment.

### Triggers
- Push to `main` branch (only when merged from `release/*` or `hotfix/*` branches)

### Features
- ✅ Automatic version detection from branch names
- ✅ PR-based changelog generation
- ✅ GitHub release creation
- ✅ Fast deployment for development cycles

### Usage Example
```bash
# Create a release branch
git checkout -b release/1.2.3

# Make your changes and commit
git add .
git commit -m "feat: add new feature"

# Push and create PR
git push origin release/1.2.3
# Create PR to main branch

# Once merged → auto-release.yml triggers automatically
```

### Expected Branch Format
- `release/X.Y.Z` (e.g., `release/1.2.3`)
- `hotfix/X.Y.Z` (e.g., `hotfix/1.2.1`)

---

## 🚀 Official Release

**File**: [`workflows/release.yml`](./workflows/release.yml)

### Purpose
Creates comprehensive, production-ready releases with full validation, testing, and security scanning. Used for major releases and production deployments.

### Triggers
- Git tags matching pattern `v*.*.*` (e.g., `v1.2.3`, `v2.0.0-beta.1`)

### Features
- ✅ Comprehensive validation and testing
- ✅ Multi-shell compatibility testing (bash, zsh, dash)
- ✅ Security scanning with ShellCheck
- ✅ Secret scanning with TruffleHog
- ✅ Detailed changelog generation
- ✅ Pre-release support (alpha, beta, RC)
- ✅ Version validation and smart detection
- ✅ Error handling and timeouts

### Supported Version Formats
- **Stable**: `v1.2.3`
- **Alpha**: `v1.2.3-alpha.1`
- **Beta**: `v1.2.3-beta.1`
- **Release Candidate**: `v1.2.3-rc.1`

### Usage Example
```bash
# For stable releases
git tag v1.2.3
git push origin v1.2.3

# For pre-releases
git tag v1.3.0-beta.1
git push origin v1.3.0-beta.1

# For release candidates
git tag v2.0.0-rc.1
git push origin v2.0.0-rc.1
```

---

## 🔍 Branch Name Check

**File**: [`workflows/branch-name-check.yml`](./workflows/branch-name-check.yml)

### Purpose
Enforces branch naming conventions to maintain consistency and enable automation.

### Triggers
- Pull Request events (opened, edited, synchronize)

### Allowed Branch Patterns
- `feature/*` - New features
- `bugfix/*` - Bug fixes
- `hotfix/*` - Critical fixes
- `release/*` - Release preparation
- `docs/*` - Documentation updates
- `chore/*` - Maintenance tasks

### Examples
✅ **Valid branch names:**
- `feature/add-user-authentication`
- `bugfix/fix-login-issue`
- `hotfix/1.2.1`
- `release/2.0.0`
- `docs/update-readme`
- `chore/update-dependencies`

❌ **Invalid branch names:**
- `my-feature` (missing prefix)
- `FEATURE/add-login` (wrong case)
- `fix_bug` (wrong separator)

---

## �️ Branch Protection

**File**: [`workflows/branch-protection.yml`](./workflows/branch-protection.yml)

### Purpose
Automatically applies protection rules to the main branch to ensure code quality and security.

### Triggers
- Manual dispatch (`workflow_dispatch`)

### Protection Rules Applied
- ✅ Require pull request reviews
- ✅ Require status checks to pass
- ✅ Require branches to be up to date
- ✅ Require conversation resolution
- ✅ Restrict pushes to main branch

### Usage
1. Go to **Actions** tab in GitHub
2. Select **Branch Protection** workflow
3. Click **Run workflow**
4. Protection rules will be applied to `main` branch

---

## 🧪 Continuous Integration

**File**: [`workflows/ci.yml`](./workflows/ci.yml)

### Purpose
Runs comprehensive tests and quality checks on all code changes to ensure stability and quality.

### Triggers
- Pull Request events (opened, synchronize, reopened)
- Push to main branch

### Test Matrix
- **Operating Systems**: Ubuntu, macOS, Windows
- **Shells**: bash, zsh, dash (where applicable)

### Quality Checks
- ✅ Syntax validation
- ✅ ShellCheck static analysis
- ✅ Script execution tests
- ✅ Configuration validation
- ✅ Cross-platform compatibility

---

## 🔄 Automated Updates

**File**: [`workflows/auto-update.yml`](./workflows/auto-update.yml)

### Purpose
Automatically updates dependencies and creates pull requests for review.

### Triggers
- Weekly schedule (Sundays at 2 AM UTC)
- Manual dispatch (`workflow_dispatch`)

### Updates Managed
- ✅ GitHub Actions versions
- ✅ Shell dependencies
- ✅ Configuration updates
- ✅ Security patches
- ✅ Repository health checks

---

## 🚀 Comprehensive Usage Guide

### For Developers

#### 1. **Feature Development**
```bash
# Create feature branch (follows naming conventions)
git checkout -b feature/my-new-feature

# Develop and test locally
# Push and create PR → CI runs automatically
git push origin feature/my-new-feature
```

#### 2. **Quick Development Releases**
```bash
# Create release branch for automatic deployment
git checkout -b release/1.2.3

# Finalize release changes
git push origin release/1.2.3
# Create PR to main → Auto-release triggers after merge
```

#### 3. **Production Releases (Official)**
```bash
# Create and push semantic version tag
git tag v1.2.3
git push origin v1.2.3
# → Full validation and production release process
```

### For Repository Maintainers

#### **Setup Branch Protection**
1. Go to **Actions** tab in GitHub
2. Select **Branch Protection** workflow
3. Click **Run workflow**
4. Protection rules applied to `main` branch

#### **Monitor & Maintain**
- Check **Actions** tab for workflow status
- Review failed workflows and address issues
- Monitor automated updates and approve PRs
- Ensure all required secrets are configured

---

## 🔧 Configuration & Setup

### Required Secrets
| Secret | Purpose | Required For |
|--------|---------|--------------|
| `GITHUB_TOKEN` | GitHub API access (auto-provided) | All workflows |
| `GH_PAT` | Enhanced permissions for protection | Branch protection |

### Required Permissions
All workflows require appropriate permissions:
- `contents: write` - Create releases and update files
- `pull-requests: write` - Create and update PRs
- `issues: read` - Security scanning capabilities

### Optional Customization
Edit workflows to:
- Add more test environments
- Include additional security scanners
- Customize release note templates
- Add deployment steps for your infrastructure

---

## 🐛 Troubleshooting Guide

### Common Issues & Solutions

#### **Auto-release not triggering**
- ✅ Ensure branch name follows `release/*` or `hotfix/*` pattern
- ✅ Verify branch was actually merged to main (not just pushed)
- ✅ Check `GITHUB_TOKEN` has sufficient permissions
- ✅ Review workflow logs in Actions tab

#### **Branch name check failing**
- ✅ Use approved prefixes: `feature/`, `bugfix/`, `hotfix/`, `release/`, `docs/`, `chore/`
- ✅ Use lowercase with hyphens: `feature/my-feature`
- ✅ Avoid underscores or mixed case

#### **CI tests failing**
- ✅ Run ShellCheck locally: `shellcheck scripts/*.sh`
- ✅ Test scripts in different shells (bash, zsh)
- ✅ Check file permissions and executable bits
- ✅ Verify script paths are correct

#### **Official release workflow failing**
- ✅ Ensure tag follows semantic versioning: `v1.2.3`
- ✅ Check that all CI checks pass before tagging
- ✅ Verify repository permissions and secrets
- ✅ Review workflow logs for specific error details

#### **Branch protection setup issues**
- ✅ Ensure `GH_PAT` secret is configured with admin permissions
- ✅ Check that the token has repository administration rights
- ✅ Verify workflow dispatch permissions

---

## 📊 Workflow Dependencies & Flow

```mermaid
graph TD
    A[Developer Push] --> B{Branch Type?}
    B -->|feature/*| C[CI Workflow]
    B -->|release/*| D[CI + Auto-release]
    B -->|main| E[CI + Tag Check]
    
    F[Git Tag v*.*.*] --> G[Official Release]
    
    H[Weekly Schedule] --> I[Auto-update]
    
    J[Manual Trigger] --> K[Branch Protection]
    
    C --> L[PR Review Process]
    D --> M[Quick Development Release]
    G --> N[Production Release]
    
    L --> O[Merge Decision]
    O --> P[Update Main Branch]
```

---

## 📝 Best Practices

### When Contributing
1. **Follow branch naming conventions** (enforced by branch-name-check.yml)
2. **Ensure all CI checks pass** before requesting review
3. **Use appropriate release strategy**:
   - Feature branches → Auto-release for development iterations
   - Git tags → Official release for production deployments
4. **Review workflow changes carefully** as they affect the entire team

### Release Strategy
- **Alpha/Beta releases**: Use for testing and early feedback
- **Release candidates**: Use for final validation before stable
- **Stable releases**: Use for production deployments
- **Hotfix releases**: Use for critical bug fixes

---

## � Additional Resources

### Documentation Links
- [Repository Main README](../README.md)
- [Contributing Guidelines](../docs/CONTRIBUTING.md)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Semantic Versioning Specification](https://semver.org/)

### Workflow Management
- **GitHub Actions Tab**: Monitor all workflow runs
- **Repository Settings**: Configure branch protection manually if needed
- **Security Tab**: Review secret scanning results
- **Insights Tab**: View repository activity and workflow performance

---

## 🚀 Next Steps

After reviewing this documentation:

1. **Test the workflows**: Create a test PR to verify CI workflow
2. **Practice releases**: Try both auto-release and official release processes
3. **Monitor performance**: Check GitHub Actions tab for workflow runs
4. **Customize as needed**: Adapt workflows to your specific requirements
5. **Train your team**: Share this documentation with contributors

The complete workflow suite provides robust automation for development, testing, and release processes while maintaining high quality and security standards! 🎉

---

*Last updated: September 1, 2025*  
*Maintained by: Repository maintainers*
