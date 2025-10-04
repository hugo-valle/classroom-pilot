"""
Classroom Pilot - Python CLI Package

A comprehensive automation suite for managing Classroom assignments
with advanced workflow orchestration, repository discovery, and secret management capabilities.
"""

from ._version import get_version

__version__ = get_version()
__author__ = "Hugo Valle"
__description__ = "Classroom Pilot - Comprehensive automation suite for managing assignments"

from .config import ConfigLoader, ConfigValidator
from .utils import setup_logging, get_logger

__all__ = [
    "ConfigLoader",
    "ConfigValidator",
    "setup_logging",
    "get_logger",
    "__version__",
]
