"""
pytest configuration for classroom-pilot tests.

This file contains fixtures and configuration that are shared across all tests.
"""

import os
import tempfile
from pathlib import Path
from typing import Dict, Any

import pytest

from classroom_pilot.config import Configuration
from classroom_pilot.bash_wrapper import BashWrapper


@pytest.fixture
def test_config_data() -> Dict[str, Any]:
    """Provide test configuration data."""
    return {
        'CLASSROOM_URL': 'https://classroom.github.com/classrooms/test/assignments/test',
        'TEMPLATE_REPO_URL': 'https://github.com/test/template',
        'GITHUB_ORGANIZATION': 'test-org',
        'CLASSROOM_REPO_URL': 'https://github.com/test-org/test-assignment',
        'SECRETS_JSON': '{"TEST_SECRET": "test-value"}',
        'INSTRUCTOR_HANDLE': 'instructor',
        'ASSIGNMENT_NAME': 'test-assignment',
        'SEMESTER': 'fall2025'
    }


@pytest.fixture
def test_config(test_config_data) -> Configuration:
    """Provide a test Configuration instance."""
    return Configuration(test_config_data)


@pytest.fixture
def test_wrapper(test_config) -> BashWrapper:
    """Provide a test BashWrapper instance with dry-run enabled."""
    return BashWrapper(
        config=test_config,
        dry_run=True,
        verbose=True,
        auto_yes=True
    )


@pytest.fixture
def temp_config_file(test_config_data) -> Path:
    """Create a temporary configuration file for testing."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.conf', delete=False) as f:
        for key, value in test_config_data.items():
            f.write(f'{key}="{value}"\n')
        temp_path = Path(f.name)

    yield temp_path

    # Cleanup
    if temp_path.exists():
        temp_path.unlink()


@pytest.fixture
def temp_directory():
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


@pytest.fixture(autouse=True)
def preserve_cwd():
    """Preserve the current working directory across tests."""
    original_cwd = os.getcwd()
    yield
    os.chdir(original_cwd)
