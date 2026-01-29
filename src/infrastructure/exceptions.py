"""
Custom Exception Classes for SlideSense
Provides specific exceptions for different error types
"""


class SlideSenseException(Exception):
    """Base exception for SlideSense"""
    
    def __init__(self, message: str, error_code: str = "UNKNOWN_ERROR"):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


class MicrophoneError(SlideSenseException):
    """Raised when microphone related errors occur"""
    
    def __init__(self, message: str):
        super().__init__(message, "MICROPHONE_ERROR")


class MicrophoneNotFoundError(MicrophoneError):
    """Raised when no microphone is detected"""
    
    def __init__(self, message: str = "No microphone detected"):
        super().__init__(message)


class MicrophoneInitializationError(MicrophoneError):
    """Raised when microphone initialization fails"""
    
    def __init__(self, message: str = "Failed to initialize microphone"):
        super().__init__(message)


class VoiceRecognitionError(SlideSenseException):
    """Raised when voice recognition fails"""
    
    def __init__(self, message: str):
        super().__init__(message, "VOICE_RECOGNITION_ERROR")


class VoiceNotRecognizedError(VoiceRecognitionError):
    """Raised when speech cannot be recognized"""
    
    def __init__(self, message: str = "Could not understand speech"):
        super().__init__(message)


class AudioProcessingError(SlideSenseException):
    """Raised when audio processing fails"""
    
    def __init__(self, message: str):
        super().__init__(message, "AUDIO_PROCESSING_ERROR")


class CommandDetectionError(SlideSenseException):
    """Raised when command detection fails"""
    
    def __init__(self, message: str):
        super().__init__(message, "COMMAND_DETECTION_ERROR")


class CommandExecutionError(SlideSenseException):
    """Raised when command execution fails"""
    
    def __init__(self, message: str):
        super().__init__(message, "COMMAND_EXECUTION_ERROR")


class ConfigurationError(SlideSenseException):
    """Raised when configuration is invalid"""
    
    def __init__(self, message: str):
        super().__init__(message, "CONFIGURATION_ERROR")


class UIError(SlideSenseException):
    """Raised when UI related errors occur"""
    
    def __init__(self, message: str):
        super().__init__(message, "UI_ERROR")


class PowerPointError(SlideSenseException):
    """Raised when PowerPoint control fails"""
    
    def __init__(self, message: str):
        super().__init__(message, "POWERPOINT_ERROR")


class AccessibilityError(SlideSenseException):
    """Raised when accessibility features fail"""
    
    def __init__(self, message: str):
        super().__init__(message, "ACCESSIBILITY_ERROR")


# Error codes mapping
ERROR_MESSAGES = {
    "MICROPHONE_ERROR": "Microphone error occurred",
    "MICROPHONE_NOT_FOUND": "No microphone detected on your system",
    "MICROPHONE_INIT_FAILED": "Failed to initialize microphone",
    "VOICE_RECOGNITION_ERROR": "Voice recognition error occurred",
    "VOICE_NOT_RECOGNIZED": "Could not understand what you said",
    "AUDIO_PROCESSING_ERROR": "Audio processing error occurred",
    "COMMAND_DETECTION_ERROR": "Failed to detect command",
    "COMMAND_EXECUTION_ERROR": "Failed to execute command",
    "CONFIGURATION_ERROR": "Configuration error occurred",
    "UI_ERROR": "User interface error occurred",
    "POWERPOINT_ERROR": "PowerPoint control error occurred",
    "ACCESSIBILITY_ERROR": "Accessibility feature error occurred",
}


def get_error_message(error_code: str) -> str:
    """Get user-friendly error message from error code"""
    return ERROR_MESSAGES.get(error_code, "An unknown error occurred")
