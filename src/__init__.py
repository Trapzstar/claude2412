"""
SlideSense - Voice-Controlled Presentation System
Main application package
"""

__version__ = "2.0.0"
__author__ = "SlideSense Team"
__description__ = "Voice-controlled PowerPoint presentation with accessibility features"

# Import main components for easy access
try:
    from src.core.voice_detector import SmartVoiceDetector
    from src.core.voice_recognizer import HybridVoiceRecognizer
    from src.core.powerpoint_controller import PowerPointController
    from src.core.accessibility_popup import AccessibilityPopup
    from src.infrastructure.logger import get_logger
    from src.infrastructure.config import get_config
except ImportError:
    pass
