"""
Classroom Pilot - Python CLI Package

A comprehensive automation suite for managing Classroom assignments
with advanced workflow orchestration, repository discovery, and secret management capabilities.
"""

__version__ = "0.1.0"
__author__ = "Hugo Valle"
__description__ = "Classroom Pilot - Python CLI Package"

from .config import Configuration
from .bash_wrapper import BashWrapper
from .utils import setup_logging, validate_github_url

__all__ = [
    "Configuration",
    "BashWrapper",
    "setup_logging",
    "validate_github_url",
    "__version__",
]
