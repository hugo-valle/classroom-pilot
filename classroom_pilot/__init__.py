"""
Classroom Pilot - Python CLI Package

A comprehensive automation suite for managing Classroom assignments
with advanced workflow orchestration, repository discovery, and secret management capabilities.
"""

__version__ = "3.0.0-alpha.1"
__author__ = "Hugo Valle"
__description__ = "Classroom Pilot - Comprehensive automation suite for managing assignments"

from .config import ConfigLoader, ConfigValidator
from .bash_wrapper import BashWrapper
from .utils import setup_logging, get_logger

__all__ = [
    "ConfigLoader",
    "ConfigValidator",
    "BashWrapper",
    "setup_logging",
    "get_logger",
    "__version__",
]
