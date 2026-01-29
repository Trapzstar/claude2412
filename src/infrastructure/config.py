"""
Centralized Configuration Management for SlideSense
Load configuration from file, environment variables, or defaults
"""

import os
import json
from pathlib import Path
from typing import Any, Dict, Optional
from src.infrastructure.logger import get_logger

logger = get_logger(__name__)

# Config file paths
CONFIG_DIR = Path("config")
CONFIG_FILE = CONFIG_DIR / "config.json"
ENV_FILE = Path(".env")

# Default configuration
DEFAULT_CONFIG = {
    "application": {
        "name": "SlideSense",
        "version": "2.0.0",
        "debug": False,
    },
    "voice": {
        "language": "en-US",
        "listen_timeout": 5,
        "phrase_limit": 4,
        "energy_threshold": 300,
        "max_retries": 3,
        "retry_delay": 0.5,
    },
    "microphone": {
        "device_index": None,  # Auto-detect
        "auto_select": True,
        "channels": 2,
    },
    "accessibility": {
        "caption_enabled": False,
        "real_time_caption": True,
        "caption_position": "top",
    },
    "logging": {
        "level": "INFO",
        "file_logging": True,
        "console_logging": True,
        "max_file_size": 10485760,  # 10MB
        "backup_count": 5,
    },
    "powerpoint": {
        "auto_start_slideshow": False,
        "listen_only_in_slideshow": True,
    },
}


class Config:
    """Configuration manager for SlideSense"""
    
    def __init__(self):
        """Initialize configuration"""
        self._config = DEFAULT_CONFIG.copy()
        self._load_config()
        logger.info("Configuration loaded successfully")
    
    def _load_config(self):
        """Load configuration from file and environment"""
        # Load from config file if exists
        if CONFIG_FILE.exists():
            try:
                with open(CONFIG_FILE, 'r') as f:
                    file_config = json.load(f)
                    self._merge_config(file_config)
                    logger.info(f"Loaded config from {CONFIG_FILE}")
            except Exception as e:
                logger.error(f"Error loading config file: {e}")
        
        # Load from environment variables
        self._load_from_env()
    
    def _merge_config(self, new_config: Dict[str, Any]):
        """Merge new configuration with defaults"""
        for key, value in new_config.items():
            if isinstance(value, dict) and key in self._config:
                self._config[key].update(value)
            else:
                self._config[key] = value
    
    def _load_from_env(self):
        """Load configuration from environment variables"""
        # Voice settings
        if "VOICE_LANGUAGE" in os.environ:
            self._config["voice"]["language"] = os.getenv("VOICE_LANGUAGE")
        
        if "LISTEN_TIMEOUT" in os.environ:
            self._config["voice"]["listen_timeout"] = int(os.getenv("LISTEN_TIMEOUT"))
        
        # Microphone settings
        if "MICROPHONE_DEVICE" in os.environ:
            self._config["microphone"]["device_index"] = int(os.getenv("MICROPHONE_DEVICE"))
        
        # Logging level
        if "LOG_LEVEL" in os.environ:
            self._config["logging"]["level"] = os.getenv("LOG_LEVEL")
        
        # Debug mode
        if "DEBUG" in os.environ:
            self._config["application"]["debug"] = os.getenv("DEBUG").lower() == "true"
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation
        
        Args:
            key: Configuration key (e.g., "voice.language")
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        keys = key.split(".")
        value = self._config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            logger.warning(f"Configuration key not found: {key}")
            return default
    
    def set(self, key: str, value: Any):
        """
        Set configuration value using dot notation
        
        Args:
            key: Configuration key (e.g., "voice.language")
            value: Value to set
        """
        keys = key.split(".")
        config = self._config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
        logger.debug(f"Configuration updated: {key} = {value}")
    
    def get_section(self, section: str) -> Dict[str, Any]:
        """
        Get entire configuration section
        
        Args:
            section: Section name (e.g., "voice")
            
        Returns:
            Configuration section as dictionary
        """
        return self._config.get(section, {})
    
    def to_dict(self) -> Dict[str, Any]:
        """Get entire configuration as dictionary"""
        return self._config.copy()
    
    def save(self, filepath: Optional[Path] = None):
        """
        Save configuration to file
        
        Args:
            filepath: Path to save (default: config/config.json)
        """
        filepath = filepath or CONFIG_FILE
        filepath.parent.mkdir(exist_ok=True)
        
        try:
            with open(filepath, 'w') as f:
                json.dump(self._config, f, indent=2)
            logger.info(f"Configuration saved to {filepath}")
        except Exception as e:
            logger.error(f"Error saving configuration: {e}")
    
    def validate(self) -> bool:
        """Validate configuration"""
        try:
            # Check required sections
            required_sections = ["application", "voice", "microphone"]
            for section in required_sections:
                if section not in self._config:
                    logger.error(f"Missing required section: {section}")
                    return False
            
            # Check voice timeout is positive
            if self._config["voice"]["listen_timeout"] <= 0:
                logger.error("voice.listen_timeout must be positive")
                return False
            
            logger.info("Configuration validation passed")
            return True
        except Exception as e:
            logger.error(f"Configuration validation error: {e}")
            return False


# Global config instance
_config_instance: Optional[Config] = None


def get_config() -> Config:
    """Get global configuration instance (singleton)"""
    global _config_instance
    
    if _config_instance is None:
        _config_instance = Config()
        if not _config_instance.validate():
            logger.warning("Configuration validation failed, using defaults")
    
    return _config_instance


def reset_config():
    """Reset configuration (mainly for testing)"""
    global _config_instance
    _config_instance = None


if __name__ == "__main__":
    # Test configuration
    config = get_config()
    
    print("Configuration:")
    print(f"  Language: {config.get('voice.language')}")
    print(f"  Timeout: {config.get('voice.listen_timeout')}")
    print(f"  Debug: {config.get('application.debug')}")
    
    # Test setting values
    config.set("voice.language", "id-ID")
    print(f"  Language (after set): {config.get('voice.language')}")
