"""
Unit Tests for Custom Exceptions
Tests all custom exception types and exception handling
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.infrastructure.exceptions import (
    SlideSenseException,
    ConfigurationError,
    VoiceRecognitionError,
    MicrophoneError,
    PowerPointError,
    UIError,
    AudioProcessingError,
    CommandDetectionError,
    CommandExecutionError,
    AccessibilityError,
    MicrophoneNotFoundError,
    MicrophoneInitializationError,
    VoiceNotRecognizedError
)


class TestSlideSenseException:
    """Test base SlideSenseException"""
    
    def test_base_exception_creation(self) -> None:
        """Test creating base exception"""
        exc = SlideSenseException("Test error")
        assert str(exc) == "Test error"
        assert isinstance(exc, Exception)
    
    def test_base_exception_with_code(self) -> None:
        """Test base exception with error code"""
        exc = SlideSenseException("Test error", error_code="TEST001")
        assert exc.error_code == "TEST001"
        assert str(exc) == "Test error"
    
    def test_base_exception_inheritance(self) -> None:
        """Test base exception can be caught as Exception"""
        exc = SlideSenseException("Test")
        try:
            raise exc
        except Exception as e:
            assert isinstance(e, SlideSenseException)


class TestConfigurationError:
    """Test ConfigurationError exception"""
    
    def test_config_error_creation(self) -> None:
        """Test creating configuration error"""
        exc = ConfigurationError("Missing config file")
        assert str(exc) == "Missing config file"
        assert isinstance(exc, SlideSenseException)
    
    def test_config_error_is_raisable(self) -> None:
        """Test configuration error can be raised and caught"""
        with pytest.raises(ConfigurationError):
            raise ConfigurationError("Test config error")
    
    def test_config_error_parent_catchable(self) -> None:
        """Test configuration error caught as parent"""
        with pytest.raises(SlideSenseException):
            raise ConfigurationError("Config issue")


class TestVoiceRecognitionError:
    """Test VoiceRecognitionError exception"""
    
    def test_voice_recognition_error_creation(self) -> None:
        """Test creating voice recognition error"""
        exc = VoiceRecognitionError("No speech detected")
        assert str(exc) == "No speech detected"
        assert isinstance(exc, SlideSenseException)
    
    def test_voice_recognition_error_is_raisable(self) -> None:
        """Test voice recognition error can be raised"""
        with pytest.raises(VoiceRecognitionError):
            raise VoiceRecognitionError("Speech not found")
    
    def test_voice_recognition_error_hierarchy(self) -> None:
        """Test voice recognition error inheritance chain"""
        exc = VoiceRecognitionError("Test")
        assert isinstance(exc, SlideSenseException)
        assert isinstance(exc, Exception)


class TestAudioDeviceError:
    """Test MicrophoneError exception"""
    
    def test_audio_device_error_creation(self) -> None:
        """Test creating microphone error"""
        exc = MicrophoneError("Microphone not found")
        assert str(exc) == "Microphone not found"
        assert isinstance(exc, SlideSenseException)
    
    def test_audio_device_error_is_raisable(self) -> None:
        """Test microphone error can be raised"""
        with pytest.raises(MicrophoneError):
            raise MicrophoneError("No audio devices available")


class TestPowerPointError:
    """Test PowerPointError exception"""
    
    def test_powerpoint_error_creation(self) -> None:
        """Test creating PowerPoint error"""
        exc = PowerPointError("Cannot open presentation")
        assert str(exc) == "Cannot open presentation"
        assert isinstance(exc, SlideSenseException)
    
    def test_powerpoint_error_is_raisable(self) -> None:
        """Test PowerPoint error can be raised"""
        with pytest.raises(PowerPointError):
            raise PowerPointError("Slide navigation failed")


class TestUIError:
    """Test UIError exception"""
    
    def test_ui_error_creation(self) -> None:
        """Test creating UI error"""
        exc = UIError("Window not found")
        assert str(exc) == "Window not found"
        assert isinstance(exc, SlideSenseException)
    
    def test_ui_error_is_raisable(self) -> None:
        """Test UI error can be raised"""
        with pytest.raises(UIError):
            raise UIError("Display error")


class TestValidationError:
    """Test AudioProcessingError exception"""
    
    def test_validation_error_creation(self) -> None:
        """Test creating audio processing error"""
        exc = AudioProcessingError("Invalid input")
        assert str(exc) == "Invalid input"
        assert isinstance(exc, SlideSenseException)
    
    def test_validation_error_is_raisable(self) -> None:
        """Test audio processing error can be raised"""
        with pytest.raises(AudioProcessingError):
            raise AudioProcessingError("Processing failed")


class TestCommunicationError:
    """Test CommandDetectionError exception"""
    
    def test_communication_error_creation(self) -> None:
        """Test creating command detection error"""
        exc = CommandDetectionError("Connection lost")
        assert str(exc) == "Connection lost"
        assert isinstance(exc, SlideSenseException)
    
    def test_communication_error_is_raisable(self) -> None:
        """Test command detection error can be raised"""
        with pytest.raises(CommandDetectionError):
            raise CommandDetectionError("Detection error")


class TestPluginError:
    """Test CommandExecutionError exception"""
    
    def test_plugin_error_creation(self) -> None:
        """Test creating command execution error"""
        exc = CommandExecutionError("Command load failed")
        assert str(exc) == "Command load failed"
        assert isinstance(exc, SlideSenseException)
    
    def test_plugin_error_is_raisable(self) -> None:
        """Test command execution error can be raised"""
        with pytest.raises(CommandExecutionError):
            raise CommandExecutionError("Execution failed")


class TestRecognizerError:
    """Test AccessibilityError exception"""
    
    def test_recognizer_error_creation(self) -> None:
        """Test creating accessibility error"""
        exc = AccessibilityError("Recognition failed")
        assert str(exc) == "Recognition failed"
        assert isinstance(exc, SlideSenseException)
    
    def test_recognizer_error_is_raisable(self) -> None:
        """Test accessibility error can be raised"""
        with pytest.raises(AccessibilityError):
            raise AccessibilityError("Accessibility error")


class TestStateError:
    """Test MicrophoneNotFoundError exception"""
    
    def test_state_error_creation(self) -> None:
        """Test creating microphone not found error"""
        exc = MicrophoneNotFoundError("Invalid state transition")
        assert str(exc) == "Invalid state transition"
        assert isinstance(exc, SlideSenseException)
    
    def test_state_error_is_raisable(self) -> None:
        """Test microphone not found error can be raised"""
        with pytest.raises(MicrophoneNotFoundError):
            raise MicrophoneNotFoundError("State machine error")


class TestTimeoutError:
    """Test MicrophoneInitializationError exception"""
    
    def test_timeout_error_creation(self) -> None:
        """Test creating microphone initialization error"""
        exc = MicrophoneInitializationError("Operation timeout")
        assert str(exc) == "Operation timeout"
        assert isinstance(exc, SlideSenseException)
    
    def test_timeout_error_is_raisable(self) -> None:
        """Test microphone initialization error can be raised"""
        with pytest.raises(MicrophoneInitializationError):
            raise MicrophoneInitializationError("Timeout occurred")


class TestExceptionHierarchy:
    """Test exception hierarchy and catching"""
    
    def test_all_errors_inherit_from_slidesense(self) -> None:
        """Test all custom errors inherit from SlideSenseException"""
        exceptions = [
            ConfigurationError("test"),
            VoiceRecognitionError("test"),
            MicrophoneError("test"),
            PowerPointError("test"),
            UIError("test"),
            AudioProcessingError("test"),
            CommandDetectionError("test"),
            CommandExecutionError("test"),
            AccessibilityError("test"),
            MicrophoneNotFoundError("test"),
            MicrophoneInitializationError("test"),
            VoiceNotRecognizedError("test")
        ]
        
        for exc in exceptions:
            assert isinstance(exc, SlideSenseException)
    
    def test_catch_base_catches_all(self) -> None:
        """Test catching base exception catches all custom exceptions"""
        test_exceptions = [
            ConfigurationError("config"),
            VoiceRecognitionError("voice"),
            MicrophoneError("audio"),
        ]
        
        for exc in test_exceptions:
            with pytest.raises(SlideSenseException):
                raise exc
    
    def test_catch_specific_exception(self) -> None:
        """Test catching specific exception type"""
        with pytest.raises(ConfigurationError):
            raise ConfigurationError("Config error")
    
    def test_cannot_catch_wrong_type(self) -> None:
        """Test cannot catch wrong exception type"""
        with pytest.raises(ConfigurationError):
            try:
                raise ConfigurationError("Config error")
            except MicrophoneError:
                pass


class TestExceptionErrorCodes:
    """Test exception handling"""
    
    def test_base_exception_has_message(self) -> None:
        """Test base exception has message"""
        exc = SlideSenseException("test message")
        assert str(exc) == "test message"
    
    def test_error_message_preserved(self) -> None:
        """Test error message is preserved"""
        exc = ConfigurationError("Config missing")
        assert str(exc) == "Config missing"
    
    def test_exception_with_long_message(self) -> None:
        """Test exception with long message"""
        long_msg = "x" * 1000
        exc = SlideSenseException(long_msg)
        assert str(exc) == long_msg


class TestExceptionMessages:
    """Test exception message handling"""
    
    def test_empty_message(self) -> None:
        """Test exception with empty message"""
        exc = SlideSenseException("")
        assert str(exc) == ""
    
    def test_long_message(self) -> None:
        """Test exception with long message"""
        long_msg = "x" * 1000
        exc = SlideSenseException(long_msg)
        assert str(exc) == long_msg
    
    def test_message_with_special_chars(self) -> None:
        """Test exception with special characters"""
        msg = "Error: \n\t 'quoted' and \"double quotes\" & symbols!"
        exc = SlideSenseException(msg)
        assert str(exc) == msg
    
    def test_unicode_message(self) -> None:
        """Test exception with unicode characters"""
        msg = "Error: 🎤 microphone issue"
        exc = SlideSenseException(msg)
        assert str(exc) == msg


class TestExceptionChaining:
    """Test exception chaining capabilities"""
    
    def test_exception_from_exception(self) -> None:
        """Test raising exception from another exception"""
        try:
            raise ValueError("Original error")
        except ValueError as e:
            with pytest.raises(SlideSenseException):
                raise SlideSenseException(f"Wrapped: {str(e)}") from e
    
    def test_exception_with_cause(self) -> None:
        """Test exception maintains cause context"""
        original = ValueError("Original")
        try:
            raise original
        except ValueError:
            exc = SlideSenseException("New error")
            assert exc is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
