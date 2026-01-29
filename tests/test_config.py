"""
Test Suite for SlideSense Configuration Management
"""

import unittest
import tempfile
import json
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.infrastructure.config import Config, get_config, reset_config


class TestConfigBasic(unittest.TestCase):
    """Test basic configuration functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        reset_config()
        self.config = Config()
    
    def test_default_config_loaded(self):
        """Test that default configuration is loaded"""
        self.assertIsNotNone(self.config)
        self.assertEqual(self.config.get("application.name"), "SlideSense")
    
    def test_get_config_value(self):
        """Test getting configuration values"""
        language = self.config.get("voice.language")
        self.assertEqual(language, "en-US")
    
    def test_get_with_default(self):
        """Test getting non-existent config with default"""
        value = self.config.get("non.existent.key", "default_value")
        self.assertEqual(value, "default_value")
    
    def test_set_config_value(self):
        """Test setting configuration values"""
        self.config.set("voice.language", "id-ID")
        self.assertEqual(self.config.get("voice.language"), "id-ID")
    
    def test_get_section(self):
        """Test getting entire configuration section"""
        voice_config = self.config.get_section("voice")
        self.assertIn("language", voice_config)
        self.assertIn("listen_timeout", voice_config)
    
    def test_to_dict(self):
        """Test converting config to dictionary"""
        config_dict = self.config.to_dict()
        self.assertIsInstance(config_dict, dict)
        self.assertIn("application", config_dict)
        self.assertIn("voice", config_dict)
    
    def test_validation_passes(self):
        """Test configuration validation"""
        is_valid = self.config.validate()
        self.assertTrue(is_valid)
    
    def test_validation_fails_missing_section(self):
        """Test validation fails when section missing"""
        self.config._config = {}  # Remove all config
        is_valid = self.config.validate()
        self.assertFalse(is_valid)


class TestConfigModification(unittest.TestCase):
    """Test configuration modifications"""
    
    def setUp(self):
        """Set up test fixtures"""
        reset_config()
        self.config = Config()
    
    def test_modify_nested_value(self):
        """Test modifying nested configuration values"""
        original = self.config.get("voice.listen_timeout")
        self.config.set("voice.listen_timeout", 10)
        self.assertEqual(self.config.get("voice.listen_timeout"), 10)
    
    def test_create_new_section(self):
        """Test creating new configuration section"""
        self.config.set("new_section.new_key", "new_value")
        self.assertEqual(self.config.get("new_section.new_key"), "new_value")
    
    def test_save_configuration(self):
        """Test saving configuration to file"""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_file = Path(tmpdir) / "config.json"
            self.config.save(config_file)
            self.assertTrue(config_file.exists())
            
            # Verify content
            with open(config_file) as f:
                saved_config = json.load(f)
            self.assertIn("application", saved_config)


class TestConfigDefaults(unittest.TestCase):
    """Test configuration defaults"""
    
    def setUp(self):
        """Set up test fixtures"""
        reset_config()
        self.config = Config()
    
    def test_debug_default_false(self):
        """Test debug mode defaults to false"""
        self.assertFalse(self.config.get("application.debug"))
    
    def test_microphone_auto_select_true(self):
        """Test microphone auto-select defaults to true"""
        self.assertTrue(self.config.get("microphone.auto_select"))
    
    def test_listening_timeout_positive(self):
        """Test listening timeout is positive"""
        timeout = self.config.get("voice.listen_timeout")
        self.assertGreater(timeout, 0)
    
    def test_language_english(self):
        """Test default language is English or Indonesian"""
        language = self.config.get("voice.language")
        self.assertIn(language, ["en-US", "id-ID"])  # Accept both defaults


class TestSingleton(unittest.TestCase):
    """Test singleton pattern for config"""
    
    def test_get_config_returns_same_instance(self):
        """Test that get_config returns same instance"""
        reset_config()
        config1 = get_config()
        config2 = get_config()
        self.assertIs(config1, config2)
    
    def test_modification_persists(self):
        """Test that modifications persist across get_config calls"""
        reset_config()
        config1 = get_config()
        config1.set("test.value", "test")
        
        config2 = get_config()
        self.assertEqual(config2.get("test.value"), "test")


class TestConfigIntegration(unittest.TestCase):
    """Integration tests for configuration"""
    
    def setUp(self):
        """Set up test fixtures"""
        reset_config()
    
    def test_load_modify_save(self):
        """Test load, modify, save workflow"""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_file = Path(tmpdir) / "config.json"
            
            # Create and save initial config
            config = Config()
            config.set("voice.language", "id-ID")
            config.save(config_file)
            
            # Verify saved
            with open(config_file) as f:
                data = json.load(f)
            self.assertEqual(data["voice"]["language"], "id-ID")


if __name__ == "__main__":
    unittest.main()
