"""
Test module for Configuration functionality.

Tests the Configuration class and configuration loading.
"""

import tempfile
from pathlib import Path

import pytest

from classroom_pilot.config import Configuration


class TestConfigurationInitialization:
    """Test Configuration initialization."""

    def test_init_with_data(self, test_config_data):
        """Test Configuration initialization with data."""
        config = Configuration(test_config_data)
        assert config.data == test_config_data

    def test_init_empty(self):
        """Test Configuration initialization without data."""
        config = Configuration()
        assert config.data == {}


class TestConfigurationValidation:
    """Test Configuration validation."""

    def test_valid_config(self, test_config_data):
        """Test validation with valid configuration."""
        # Should not raise an exception
        Configuration(test_config_data)

    def test_missing_required_fields(self):
        """Test validation with missing required fields."""
        incomplete_data = {
            'CLASSROOM_URL': 'https://classroom.github.com/test'
            # Missing other required fields
        }
        with pytest.raises(ValueError):
            Configuration(incomplete_data)


class TestConfigurationLoading:
    """Test Configuration loading from files."""

    def test_load_from_file(self, temp_config_file):
        """Test loading configuration from file."""
        config = Configuration.load(temp_config_file)
        assert isinstance(config, Configuration)
        assert config.data['CLASSROOM_URL'] is not None

    def test_load_nonexistent_file(self):
        """Test loading from non-existent file."""
        with pytest.raises(FileNotFoundError):
            Configuration.load(Path("/nonexistent/config.conf"))


class TestConfigurationEnvironment:
    """Test Configuration environment variable conversion."""

    def test_to_env_dict(self, test_config):
        """Test conversion to environment dictionary."""
        env_dict = test_config.to_env_dict()
        assert isinstance(env_dict, dict)
        assert 'CLASSROOM_URL' in env_dict
        assert 'GITHUB_ORGANIZATION' in env_dict

    def test_env_dict_values(self, test_config):
        """Test environment dictionary values."""
        env_dict = test_config.to_env_dict()
        # All values should be strings
        for key, value in env_dict.items():
            assert isinstance(
                value, str), f"Value for {key} is not a string: {value}"
