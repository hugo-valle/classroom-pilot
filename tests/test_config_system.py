"""
Test suite for the configuration management system.

Tests configuration loading, validation, and generation.
"""

import pytest
from pathlib import Path
import tempfile
import os

from classroom_pilot.config.loader import ConfigLoader
from classroom_pilot.config.validator import ConfigValidator
from classroom_pilot.config.generator import ConfigGenerator


class TestConfigLoader:
    """Test configuration loading functionality."""

    def test_load_valid_config(self, test_config_data, temp_config_file):
        """Test loading a valid configuration file."""
        loader = ConfigLoader(temp_config_file)
        config = loader.load()

        assert config is not None
        assert config['CLASSROOM_URL'] == test_config_data['CLASSROOM_URL']
        assert config['TEMPLATE_REPO_URL'] == test_config_data['TEMPLATE_REPO_URL']
        assert config['GITHUB_ORGANIZATION'] == test_config_data['GITHUB_ORGANIZATION']

    def test_load_nonexistent_config(self):
        """Test loading a non-existent configuration file."""
        loader = ConfigLoader(Path("/nonexistent/config.conf"))
        config = loader.load()

        assert config == {}

    def test_get_value_with_default(self, temp_config_file):
        """Test getting configuration values with defaults."""
        loader = ConfigLoader(temp_config_file)

        # Test existing value
        value = loader.get_value('CLASSROOM_URL')
        assert value is not None

        # Test non-existing value with default
        value = loader.get_value('NONEXISTENT_KEY', 'default_value')
        assert value == 'default_value'

    def test_update_config(self, temp_config_file):
        """Test updating configuration values."""
        loader = ConfigLoader(temp_config_file)

        updates = {
            'NEW_KEY': 'new_value',
            'CLASSROOM_URL': 'updated_url'
        }

        success = loader.update_config(updates)
        assert success is True

        # Verify updates
        updated_config = loader.load()
        assert updated_config['NEW_KEY'] == 'new_value'
        assert updated_config['CLASSROOM_URL'] == 'updated_url'

    def test_load_malformed_config(self, temp_directory):
        """Test loading a malformed configuration file."""
        malformed_file = temp_directory / "malformed.conf"
        with open(malformed_file, 'w') as f:
            f.write("INVALID LINE WITHOUT EQUALS\n")
            f.write("VALID_KEY=valid_value\n")
            f.write("=INVALID_EQUALS_FORMAT\n")

        loader = ConfigLoader(malformed_file)
        config = loader.load()

        # Should load valid lines and skip invalid ones
        assert 'VALID_KEY' in config
        assert config['VALID_KEY'] == 'valid_value'


class TestConfigValidator:
    """Test configuration validation functionality."""

    def test_validate_github_url(self):
        """Test GitHub URL validation."""
        # Valid URLs
        assert ConfigValidator.validate_github_url(
            "https://github.com/user/repo")[0] is True
        assert ConfigValidator.validate_github_url(
            "https://classroom.github.com/classrooms/123/assignments/test")[0] is True

        # Invalid URLs
        assert ConfigValidator.validate_github_url("")[0] is False
        assert ConfigValidator.validate_github_url("invalid-url")[0] is False
        assert ConfigValidator.validate_github_url(
            "http://github.com/user/repo")[0] is False  # http not https

    def test_validate_organization(self):
        """Test GitHub organization validation."""
        # Valid organizations
        assert ConfigValidator.validate_organization("valid-org")[0] is True
        assert ConfigValidator.validate_organization("ValidOrg123")[0] is True
        assert ConfigValidator.validate_organization("a")[0] is True

        # Invalid organizations
        assert ConfigValidator.validate_organization("")[0] is False
        assert ConfigValidator.validate_organization("invalid_org!")[
            0] is False
        assert ConfigValidator.validate_organization("-invalid")[0] is False
        assert ConfigValidator.validate_organization("invalid-")[0] is False

    def test_validate_assignment_name(self):
        """Test assignment name validation."""
        # Valid names (including empty)
        assert ConfigValidator.validate_assignment_name("")[0] is True
        assert ConfigValidator.validate_assignment_name(
            "valid-assignment")[0] is True
        assert ConfigValidator.validate_assignment_name("assignment_123")[
            0] is True

        # Invalid names
        assert ConfigValidator.validate_assignment_name("invalid!name")[
            0] is False
        assert ConfigValidator.validate_assignment_name("-invalid")[0] is False

    def test_validate_file_path(self):
        """Test file path validation."""
        # Valid file paths
        assert ConfigValidator.validate_file_path(
            "assignment.ipynb")[0] is True
        assert ConfigValidator.validate_file_path("main.py")[0] is True
        assert ConfigValidator.validate_file_path("homework.cpp")[0] is True
        assert ConfigValidator.validate_file_path("script.sql")[0] is True

        # Invalid file paths
        assert ConfigValidator.validate_file_path("")[0] is False
        assert ConfigValidator.validate_file_path("file.invalid")[0] is False
        assert ConfigValidator.validate_file_path("no_extension")[0] is False

    def test_validate_required_fields(self):
        """Test required fields validation."""
        # Complete config
        complete_config = {
            'CLASSROOM_URL': 'https://classroom.github.com/test',
            'TEMPLATE_REPO_URL': 'https://github.com/test/template',
            'GITHUB_ORGANIZATION': 'test-org',
            'ASSIGNMENT_FILE': 'assignment.ipynb'
        }
        missing = ConfigValidator.validate_required_fields(complete_config)
        assert len(missing) == 0

        # Missing fields
        incomplete_config = {
            'CLASSROOM_URL': 'https://classroom.github.com/test'
        }
        missing = ConfigValidator.validate_required_fields(incomplete_config)
        assert len(missing) == 3
        assert 'TEMPLATE_REPO_URL' in missing
        assert 'GITHUB_ORGANIZATION' in missing
        assert 'ASSIGNMENT_FILE' in missing

    def test_validate_full_config(self, test_config_data):
        """Test full configuration validation."""
        # Valid config
        valid_config = {
            'CLASSROOM_URL': 'https://classroom.github.com/classrooms/123/assignments/test',
            'TEMPLATE_REPO_URL': 'https://github.com/test/template',
            'GITHUB_ORGANIZATION': 'test-org',
            'ASSIGNMENT_FILE': 'assignment.ipynb'
        }
        is_valid, errors = ConfigValidator.validate_full_config(valid_config)
        assert is_valid is True
        assert len(errors) == 0

        # Invalid config
        invalid_config = {
            'CLASSROOM_URL': 'invalid-url',
            'TEMPLATE_REPO_URL': 'also-invalid',
            'GITHUB_ORGANIZATION': 'invalid!org',
            'ASSIGNMENT_FILE': 'invalid.xyz'
        }
        is_valid, errors = ConfigValidator.validate_full_config(invalid_config)
        assert is_valid is False
        assert len(errors) > 0


class TestConfigGenerator:
    """Test configuration file generation."""

    def test_create_config_file(self, temp_directory):
        """Test configuration file creation."""
        config_file = temp_directory / "test_assignment.conf"
        generator = ConfigGenerator(config_file)

        config_values = {
            'CLASSROOM_URL': 'https://classroom.github.com/test',
            'TEMPLATE_REPO_URL': 'https://github.com/test/template',
            'GITHUB_ORGANIZATION': 'test-org',
            'MAIN_ASSIGNMENT_FILE': 'assignment.ipynb',
            'USE_SECRETS': 'true'
        }

        token_files = {
            'INSTRUCTOR_TESTS_TOKEN': 'instructor_token.txt'
        }

        token_validation = {
            'INSTRUCTOR_TESTS_TOKEN': True
        }

        generator.create_config_file(
            config_values, token_files, token_validation)

        # Verify file was created
        assert config_file.exists()

        # Verify content
        content = config_file.read_text()
        assert 'CLASSROOM_URL="https://classroom.github.com/test"' in content
        assert 'TEMPLATE_REPO_URL="https://github.com/test/template"' in content
        assert 'GITHUB_ORGANIZATION="test-org"' in content
        assert 'ASSIGNMENT_FILE="assignment.ipynb"' in content

    def test_config_file_sections(self, temp_directory):
        """Test that all configuration sections are generated."""
        config_file = temp_directory / "test_sections.conf"
        generator = ConfigGenerator(config_file)

        config_values = {
            'CLASSROOM_URL': 'https://classroom.github.com/test',
            'TEMPLATE_REPO_URL': 'https://github.com/test/template',
            'GITHUB_ORGANIZATION': 'test-org',
            'MAIN_ASSIGNMENT_FILE': 'assignment.ipynb',
            'USE_SECRETS': 'false'
        }

        generator.create_config_file(config_values, {}, {})

        content = config_file.read_text()

        # Check for required sections
        assert 'ASSIGNMENT INFORMATION' in content
        assert 'SECRET MANAGEMENT' in content
        assert 'WORKFLOW CONFIGURATION' in content
        assert 'ADVANCED CONFIGURATION' in content

        # Check for specific settings
        assert 'STEP_MANAGE_SECRETS=false' in content
        assert 'LOG_LEVEL=INFO' in content
        assert 'DEFAULT_DRY_RUN=false' in content


class TestConfigIntegration:
    """Test integration between configuration components."""

    def test_loader_validator_integration(self, temp_config_file):
        """Test that loader and validator work together."""
        loader = ConfigLoader(temp_config_file)
        config = loader.load()

        is_valid, errors = ConfigValidator.validate_full_config(config)
        assert is_valid is True
        assert len(errors) == 0

    def test_generator_loader_roundtrip(self, temp_directory):
        """Test generating and then loading a config file."""
        config_file = temp_directory / "roundtrip.conf"
        generator = ConfigGenerator(config_file)

        original_values = {
            'CLASSROOM_URL': 'https://classroom.github.com/test',
            'TEMPLATE_REPO_URL': 'https://github.com/test/template',
            'GITHUB_ORGANIZATION': 'test-org',
            'MAIN_ASSIGNMENT_FILE': 'assignment.ipynb',
            'USE_SECRETS': 'true'
        }

        # Generate config
        generator.create_config_file(original_values, {}, {})

        # Load config
        loader = ConfigLoader(config_file)
        loaded_config = loader.load()

        # Verify roundtrip
        assert loaded_config['CLASSROOM_URL'] == original_values['CLASSROOM_URL']
        assert loaded_config['TEMPLATE_REPO_URL'] == original_values['TEMPLATE_REPO_URL']
        assert loaded_config['GITHUB_ORGANIZATION'] == original_values['GITHUB_ORGANIZATION']
        # Note: key changes - generator uses STUDENT_FILES instead of ASSIGNMENT_FILE
        assert loaded_config['STUDENT_FILES'] == original_values['MAIN_ASSIGNMENT_FILE']
