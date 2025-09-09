"""
Test module for Configuration functionality (Legacy).

Tests the Configuration class and configuration loading.
Note: This is a legacy test file. New tests are in test_config_system.py
"""

import tempfile
from pathlib import Path

import pytest

from classroom_pilot.config import ConfigLoader


class TestConfigurationInitialization:
    """Test Configuration initialization."""

    def test_init_with_data(self, test_config_data):
        """Test Configuration initialization with data."""
        # ConfigLoader requires a file path, not data dict
        # Skip this test for now as it tests old API
        pytest.skip("Legacy API test - ConfigLoader uses different interface")

    def test_init_empty(self):
        """Test Configuration initialization without data raises validation error."""
        # ConfigLoader requires a file path
        pytest.skip("Legacy API test - ConfigLoader uses different interface")


class TestConfigurationValidation:
    """Test Configuration validation."""

    def test_valid_config(self, test_config_data):
        """Test validation with valid configuration."""
        pytest.skip(
            "Legacy API test - validation now handled by ConfigValidator")

    def test_missing_required_fields(self):
        """Test validation with missing required fields."""
        pytest.skip(
            "Legacy API test - validation now handled by ConfigValidator")


class TestConfigurationLoading:
    """Test Configuration loading from files."""

    def test_load_from_file(self, temp_config_file):
        """Test loading configuration from file."""
        config_loader = ConfigLoader(temp_config_file)
        config_data = config_loader.load()
        assert isinstance(config_data, dict)
        assert 'CLASSROOM_URL' in config_data

    def test_load_nonexistent_file(self):
        """Test loading from non-existent file."""
        # ConfigLoader behavior is different - it logs a warning instead of raising
        pytest.skip(
            "Legacy API test - ConfigLoader behavior differs for missing files")


class TestConfigurationEnvironment:
    """Test Configuration environment variable conversion."""

    def test_to_env_dict(self):
        """Test conversion to environment dictionary."""
        pytest.skip(
            "Legacy API test - environment conversion now handled separately")

    def test_env_dict_values(self):
        """Test environment dictionary values."""
        pytest.skip(
            "Legacy API test - environment conversion now handled separately")


class TestConfigurationEnvironment:
    """Test Configuration environment variable conversion."""

    def test_to_env_dict(self):
        """Test conversion to environment dictionary."""
        pytest.skip(
            "Legacy API test - environment conversion now handled separately")

    def test_env_dict_values(self):
        """Test environment dictionary values."""
        pytest.skip(
            "Legacy API test - environment conversion now handled separately")
