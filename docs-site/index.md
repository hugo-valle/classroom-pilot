# Classroom Pilot 🚀

**Classroom Pilot** is a modern Python CLI tool for automating GitHub Classroom assignment management with comprehensive workflow orchestration, repository operations, and secret management.

[![PyPI version](https://badge.fury.io/py/classroom-pilot.svg)](https://badge.fury.io/py/classroom-pilot)
[![Python Support](https://img.shields.io/pypi/pyversions/classroom-pilot.svg)](https://pypi.org/project/classroom-pilot/)
[![Tests](https://github.com/hugo-valle/classroom-pilot/workflows/Tests/badge.svg)](https://github.com/hugo-valle/classroom-pilot/actions)

---

## ✨ Features

### 🐍 **Modern Python CLI**
- Type-safe, intuitive commands with rich help and output
- Simple installation: `pip install classroom-pilot`
- Cross-platform support (Windows, macOS, Linux)

### 🔧 **Modular Architecture**
- Organized command structure for different workflow areas
- `assignments` - Setup and orchestration
- `repos` - Repository operations and collaboration
- `secrets` - Secret and token management
- `automation` - Scheduling and batch processing

### 🎯 **Instructor-Focused**
- Smart repository discovery with automatic filtering
- Excludes instructor repos from batch operations
- Configuration-driven workflows
- Enterprise GitHub support

### 🔐 **Security & Automation**
- Secure distribution of tokens and credentials
- Automated workflows with cron scheduling
- Comprehensive logging and monitoring
- Token rotation and management

---

## 🚀 Quick Start

### Installation

```bash
# Install from PyPI
pip install classroom-pilot

# Verify installation
classroom-pilot --help
```

### Basic Usage

```bash
# Interactive setup
classroom-pilot assignments setup

# Run complete workflow
classroom-pilot assignments orchestrate --config assignment.conf

# Manage secrets
classroom-pilot secrets add --config assignment.conf
```

[Get Started →](getting-started/installation.md){ .md-button .md-button--primary }

---

## 📊 Project Status

- **Current Version**: 3.1.0a1
- **Python Support**: 3.10, 3.11, 3.12
- **Tests**: 153+ comprehensive tests with 100% pass rate
- **Package**: Available on [PyPI](https://pypi.org/project/classroom-pilot/)
- **CI/CD**: Automated testing and publishing

---

## 🎯 Use Cases

### **Assignment Management**
Automate the complete lifecycle of GitHub Classroom assignments from template synchronization to student support.

### **Repository Operations**
Efficiently discover, manage, and operate on student repositories with intelligent filtering and batch operations.

### **Secret Distribution**
Securely distribute API keys, tokens, and credentials across multiple student repositories with automated rotation.

### **Workflow Automation**
Set up scheduled automation for continuous assignment management with comprehensive monitoring.

---

## 🆘 Support

- **Documentation**: [Browse Documentation](getting-started/installation.md)
- **Issues**: [GitHub Issues](https://github.com/hugo-valle/classroom-pilot/issues)
- **Package**: [PyPI Package](https://pypi.org/project/classroom-pilot/)
- **Discussions**: [GitHub Discussions](https://github.com/hugo-valle/classroom-pilot/discussions)

---

## 📜 License

MIT License - see [License](about/license.md) for details.

**Classroom Pilot** - Modern Python automation for GitHub Classroom assignment management.
