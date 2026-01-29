"""
Test Type Hints Implementation - Phase 2
Comprehensive test suite for type annotations
"""

import pytest
from typing import Dict, Any, Optional, List
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.voice_detector import SmartVoiceDetector
from src.core.voice_recognizer import HybridVoiceRecognizer
from src.core.powerpoint_controller import PowerPointController


class TestTypeHints:
    """Test that all type hints are properly defined"""
    
    def test_smart_voice_detector_initialization(self) -> None:
        """Test SmartVoiceDetector type hints"""
        detector = SmartVoiceDetector()
        assert detector is not None
        assert isinstance(detector.wake_words, dict)
        assert isinstance(detector.fuzzy_available, bool)
    
    def test_smart_voice_detector_detect_return_type(self) -> None:
        """Test detect method returns Optional[Dict]"""
        detector = SmartVoiceDetector()
        result = detector.detect("next slide")
        assert result is None or isinstance(result, dict)
    
    def test_hybrid_voice_recognizer_initialization(self) -> None:
        """Test HybridVoiceRecognizer type hints"""
        recognizer = HybridVoiceRecognizer(debug_mode=False)
        assert recognizer is not None
        assert isinstance(recognizer.debug_mode, bool)
        assert isinstance(recognizer.speech_history, list)
        assert isinstance(recognizer.listen_timeout, (int, float))
    
    def test_hybrid_recognizer_history_type(self) -> None:
        """Test get_history returns List[str]"""
        recognizer = HybridVoiceRecognizer(debug_mode=False)
        history = recognizer.get_history()
        assert isinstance(history, list)
        for item in history:
            assert isinstance(item, str) or item is None
    
    def test_powerpoint_controller_initialization(self) -> None:
        """Test PowerPointController type hints"""
        controller = PowerPointController()
        assert controller is not None
        assert isinstance(controller.stats, dict)
        assert isinstance(controller.current_slide, int)
        assert isinstance(controller.total_slides, int)
    
    def test_powerpoint_execute_command_return_type(self) -> None:
        """Test execute_command returns str"""
        controller = PowerPointController()
        result = controller.execute_command({"command": "next"})
        assert isinstance(result, str)
    
    def test_detector_expand_variants_return_type(self) -> None:
        """Test _expand_with_variants returns List[str]"""
        detector = SmartVoiceDetector()
        phrases = ["next", "next slide"]
        result = detector._expand_with_variants(phrases)
        assert isinstance(result, list)
    
    def test_settings_with_optional_params(self) -> None:
        """Test methods with Optional parameters"""
        detector = SmartVoiceDetector(config=None, feedback_ui=None)
        assert detector is not None
        
        recognizer = HybridVoiceRecognizer(debug_mode=True, config=None)
        assert recognizer is not None


class TestTypeConsistency:
    """Test that type hints are consistent across the codebase"""
    
    def test_detector_config_type(self) -> None:
        """Test SmartVoiceDetector config parameter type"""
        # Should accept None
        detector1 = SmartVoiceDetector(config=None)
        assert detector1 is not None
        
        # Should accept Dict
        config: Dict[str, Any] = {"test": True}
        detector2 = SmartVoiceDetector(config=config)
        assert detector2 is not None
    
    def test_recognizer_timeout_type(self) -> None:
        """Test HybridVoiceRecognizer timeout parameter type"""
        recognizer = HybridVoiceRecognizer(debug_mode=False)
        
        # Should accept None
        result1 = recognizer.listen(timeout=None)
        assert result1 is None or isinstance(result1, str)
        
        # Should accept int
        result2 = recognizer.listen(timeout=5)
        assert result2 is None or isinstance(result2, str)
    
    def test_powerpoint_stats_dict_type(self) -> None:
        """Test PowerPointController stats dictionary type"""
        controller = PowerPointController()
        
        # All values should be integers
        for key, value in controller.stats.items():
            assert isinstance(key, str)
            assert isinstance(value, int)


class TestReturnTypeValidation:
    """Test that return types match their annotations"""
    
    def test_detector_methods_return_correct_types(self) -> None:
        """Test all detector methods return correct types"""
        detector = SmartVoiceDetector()
        
        # Test _expand_with_variants returns List
        result = detector._expand_with_variants(["test"])
        assert isinstance(result, list)
        
        # Test detect returns Optional[Dict]
        result = detector.detect("test")
        assert result is None or isinstance(result, dict)
        
        # Test show_help returns None
        result = detector.show_help()
        assert result is None
    
    def test_recognizer_methods_return_correct_types(self) -> None:
        """Test all recognizer methods return correct types"""
        recognizer = HybridVoiceRecognizer(debug_mode=False)
        
        # Test get_history returns List[str]
        result = recognizer.get_history()
        assert isinstance(result, list)
        
        # Test clear_history returns None
        result = recognizer.clear_history()
        assert result is None
        
        # Test show_history returns None
        result = recognizer.show_history()
        assert result is None
    
    def test_controller_methods_return_correct_types(self) -> None:
        """Test all controller methods return correct types"""
        controller = PowerPointController()
        
        # Test execute_command returns str
        result = controller.execute_command({"command": "unknown"})
        assert isinstance(result, str)
        
        # Test set_popup_system returns None
        result = controller.set_popup_system(None)
        assert result is None
        
        # Test set_slide_count returns None
        result = controller.set_slide_count(10)
        assert result is None
        
        # Test show_statistics returns None
        result = controller.show_statistics()
        assert result is None


class TestTypeInferencing:
    """Test that type hints improve IDE inference"""
    
    def test_detector_attribute_types(self) -> None:
        """Test detector attributes have proper types"""
        detector = SmartVoiceDetector()
        
        # These should be properly typed for IDE
        wake_words: Dict[str, Any] = detector.wake_words
        history: List[str] = []  # Based on implementation
        
        assert isinstance(wake_words, dict)
    
    def test_recognizer_attribute_types(self) -> None:
        """Test recognizer attributes have proper types"""
        recognizer = HybridVoiceRecognizer(debug_mode=False)
        
        # These should be properly typed for IDE
        debug: bool = recognizer.debug_mode
        history: List[str] = recognizer.get_history()
        timeout: int = recognizer.listen_timeout
        
        assert isinstance(debug, bool)
        assert isinstance(history, list)
        assert isinstance(timeout, int)
    
    def test_controller_attribute_types(self) -> None:
        """Test controller attributes have proper types"""
        controller = PowerPointController()
        
        # These should be properly typed for IDE
        stats: Dict[str, int] = controller.stats
        slide: int = controller.current_slide
        total: int = controller.total_slides
        
        assert isinstance(stats, dict)
        assert isinstance(slide, int)
        assert isinstance(total, int)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
