"""
Configuration loading for Classroom Pilot.

This module handles loading and parsing of assignment configuration files.
"""

from pathlib import Path
from typing import Dict, Any, Optional
import configparser
from ..utils import get_logger, PathManager

logger = get_logger("config.loader")


class ConfigLoader:
    """Load and parse configuration files."""

    def __init__(self, config_path: Optional[Path] = None):
        self.path_manager = PathManager()
        self.config_path = config_path or self.path_manager.find_config_file()

    def load(self) -> Dict[str, Any]:
        """
        Load configuration from file.

        Returns:
            Dictionary containing configuration values
        """
        if not self.config_path or not self.config_path.exists():
            logger.warning("No configuration file found")
            return {}

        try:
            # Read configuration file (shell format)
            config = {}
            with open(self.config_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    # Skip comments and empty lines
                    if not line or line.startswith('#'):
                        continue

                    # Parse variable assignments
                    if '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip().strip('"\'')  # Remove quotes
                        config[key] = value

            logger.info(f"Loaded configuration from {self.config_path}")
            return config

        except Exception as e:
            logger.error(f"Failed to load configuration: {e}")
            return {}

    def get_value(self, key: str, default: Any = None) -> Any:
        """Get a specific configuration value."""
        config = self.load()
        return config.get(key, default)

    def update_config(self, updates: Dict[str, Any]) -> bool:
        """
        Update configuration file with new values.

        Args:
            updates: Dictionary of key-value pairs to update

        Returns:
            True if successful, False otherwise
        """
        if not self.config_path:
            logger.error("No configuration file path available")
            return False

        try:
            # Load existing config
            existing_config = self.load()

            # Merge updates
            existing_config.update(updates)

            # Write back to file
            with open(self.config_path, 'w') as f:
                f.write("# GitHub Classroom Assignment Configuration\n")
                f.write(f"# Updated by ConfigLoader\n\n")

                for key, value in existing_config.items():
                    f.write(f'{key}="{value}"\n')

            logger.info(f"Updated configuration file: {self.config_path}")
            return True

        except Exception as e:
            logger.error(f"Failed to update configuration: {e}")
            return False
