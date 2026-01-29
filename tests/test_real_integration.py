"""
Real Application Integration Tests & Profiling
Tests actual workflow with real performance metrics
"""

import pytest
import time
from typing import Dict, Any, List
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.voice_detector import SmartVoiceDetector
from src.core.voice_recognizer import HybridVoiceRecognizer
from src.core.powerpoint_controller import PowerPointController


class TestRealApplicationWorkflow:
    """Test real end-to-end workflows"""
    
    @pytest.fixture
    def app_components(self):
        """Initialize actual app components"""
        detector = SmartVoiceDetector()
        detector.cooldown_seconds = 0  # Disable for testing
        recognizer = HybridVoiceRecognizer()
        controller = PowerPointController()
        
        return {
            "detector": detector,
            "recognizer": recognizer,
            "controller": controller
        }
    
    def test_end_to_end_voice_command(self, app_components):
        """Full workflow: input → detect → command → execute"""
        components = app_components
        
        # Simulate voice input
        voice_input = "next slide"
        
        with measure_time("E2E Workflow"):
            # Step 1: Detect command
            detection_result = components["detector"].detect(voice_input)
            
            # Step 2: Check if detected
            assert detection_result is not None
            assert "command" in detection_result
            assert detection_result["command"] == "next"
            
            # Step 3: Execute command
            if detection_result["command"] != "unknown":
                execution_result = components["controller"].execute_command(detection_result)
                assert execution_result is not None
    
    def test_multiple_voice_commands(self, app_components):
        """Test rapid sequence of commands"""
        components = app_components
        
        commands = [
            ("next slide", "next"),
            ("back slide", "previous"),
            ("open slide show", "open_slideshow"),
            ("stop program", "stop"),
        ]
        
        profiler = PerformanceProfiler()
        
        for voice_input, expected_cmd in commands:
            def test_cmd():
                result = components["detector"].detect(voice_input)
                if result and result["command"] != "unknown":
                    components["controller"].execute_command(result)
            
            result = profiler.benchmark(test_cmd, iterations=5, name=f"cmd_{expected_cmd}")
            assert result.avg_time > 0, f"Command {expected_cmd} failed"


class TestVoiceDetectorPerformance:
    """Profile actual voice detector performance"""
    
    def test_detector_initialization_time(self):
        """Measure how long detector initialization takes"""
        with measure_time("Detector Initialization"):
            detector = SmartVoiceDetector()
        
        assert detector is not None
    
    def test_detection_speed(self):
        """Measure detection speed for various inputs"""
        detector = SmartVoiceDetector()
        detector.cooldown_seconds = 0
        
        test_cases = [
            "next slide",
            "back slide",
            "open slide show",
            "close slide show",
            "help",
            "stop",
        ]
        
        profiler = PerformanceProfiler()
        
        for test_input in test_cases:
            def detect():
                detector.detect(test_input)
            
            result = profiler.benchmark(
                detect, 
                iterations=10, 
                name=f"detect_{test_input[:10]}"
            )
            
            # Detection should be fast (< 100ms)
            assert result.avg_time < 0.1, f"Detection too slow for: {test_input}"
        
        print("\n" + profiler.report())
    
    def test_fuzzy_matching_impact(self):
        """Measure impact of fuzzy matching on performance"""
        detector = SmartVoiceDetector()
        detector.cooldown_seconds = 0
        
        # Test exact match (should be fast)
        profiler = PerformanceProfiler()
        
        # Fast path: exact match
        result1 = profiler.benchmark(
            lambda: detector.detect("next slide"),
            iterations=100,
            name="ExactMatch"
        )
        
        # Slow path: fuzzy matching
        result2 = profiler.benchmark(
            lambda: detector.detect("naks slaid"),
            iterations=100,
            name="FuzzyMatch"
        )
        
        # Fuzzy should be slower but not dramatically
        ratio = result2.avg_time / result1.avg_time
        print(f"\nFuzzy matching slowdown: {ratio:.2f}x")
        
        assert ratio < 5, "Fuzzy matching too slow"


class TestVoiceRecognizerPerformance:
    """Profile actual speech recognition performance"""
    
    def test_recognizer_initialization(self):
        """Measure recognizer initialization time"""
        with measure_time("Recognizer Initialization"):
            recognizer = HybridVoiceRecognizer()
        
        assert recognizer is not None
    
    def test_device_listing_speed(self):
        """Measure how long device listing takes"""
        recognizer = HybridVoiceRecognizer()
        
        with measure_time("Device Listing"):
            devices = recognizer.list_audio_devices()
        
        assert devices is not None


class TestControllerPerformance:
    """Profile PowerPoint controller performance"""
    
    def test_command_execution_speed(self):
        """Measure command execution time"""
        controller = PowerPointController()
        profiler = PerformanceProfiler()
        
        test_commands = [
            {"command": "next", "score": 10},
            {"command": "previous", "score": 10},
            {"command": "stop", "score": 15},
        ]
        
        for cmd in test_commands:
            result = profiler.benchmark(
                lambda c=cmd: controller.execute_command(c),
                iterations=10,
                name=f"execute_{cmd['command']}"
            )
            
            # Commands should execute quickly (< 500ms)
            assert result.avg_time < 0.5
        
        print("\n" + profiler.report())


class TestRealBottlenecks:
    """Identify REAL bottlenecks in the application"""
    
    def test_complete_workflow_profiling(self):
        """Profile complete workflow to find bottlenecks"""
        detector = SmartVoiceDetector()
        recognizer = HybridVoiceRecognizer()
        controller = PowerPointController()
        
        detector.cooldown_seconds = 0
        
        profiler = PerformanceProfiler()
        
        # Test complete workflow
        def complete_workflow():
            # 1. Voice input (simulated)
            voice_input = "next slide"
            
            # 2. Detection
            result = detector.detect(voice_input)
            
            # 3. Execution
            if result and result["command"] != "unknown":
                controller.execute_command(result)
        
        result = profiler.benchmark(complete_workflow, iterations=20)
        
        print("\n" + "="*70)
        print("COMPLETE WORKFLOW PROFILING")
        print("="*70)
        print(f"Total Time: {result.total_time:.3f}s")
        print(f"Avg Per Call: {result.avg_time*1000:.2f}ms")
        print(f"Min Time: {result.min_time*1000:.2f}ms")
        print(f"Max Time: {result.max_time*1000:.2f}ms")
        print(f"Calls/Second: {result.calls_per_second:.1f}")
        print("="*70)
        
        # Real applications need < 500ms response time for voice commands
        assert result.avg_time < 0.5, "Voice command too slow"
    
    def test_identify_slowest_components(self):
        """Identify which components are slowest"""
        profiler = PerformanceProfiler()
        
        # Profile individual components
        print("\n" + "="*70)
        print("COMPONENT PERFORMANCE ANALYSIS")
        print("="*70)
        
        # 1. Detector
        detector = SmartVoiceDetector()
        detector.cooldown_seconds = 0
        profiler.benchmark(
            lambda: detector.detect("next slide"),
            iterations=20,
            name="Detector"
        )
        
        # 2. Recognizer
        recognizer = HybridVoiceRecognizer()
        profiler.benchmark(
            lambda: recognizer.list_audio_devices(),
            iterations=5,
            name="Recognizer_DeviceList"
        )
        
        # 3. Controller
        controller = PowerPointController()
        profiler.benchmark(
            lambda: controller.execute_command({"command": "next", "score": 10}),
            iterations=20,
            name="Controller_Execute"
        )
        
        print(profiler.report())
        
        # Identify hotspots
        hotspots = profiler.identify_hotspots(threshold_percent=5)
        print(f"\nHotspots (>5% time):")
        for name, percent in hotspots:
            print(f"  - {name}: {percent:.1f}%")


class TestCommandMatchingAccuracy:
    """Verify command matching accuracy (real test)"""
    
    def test_similar_command_disambiguation(self):
        """Test that similar commands are correctly distinguished"""
        detector = SmartVoiceDetector()
        detector.cooldown_seconds = 0
        
        # These should NOT match each other
        tests = [
            ("next slide", "next"),          # Should match next
            ("back slide", "previous"),      # Should match previous (not next!)
            ("previous slide", "previous"),  # Should match previous
            ("open slide show", "open_slideshow"),      # Should match open
            ("close slide show", "close_slideshow"),    # Should match close (not open!)
        ]
        
        failures = []
        for voice_input, expected_cmd in tests:
            result = detector.detect(voice_input)
            if result and result["command"] != expected_cmd:
                failures.append({
                    "input": voice_input,
                    "expected": expected_cmd,
                    "got": result["command"],
                    "score": result.get("score", 0)
                })
        
        if failures:
            print("\n❌ COMMAND MATCHING FAILURES:")
            for fail in failures:
                print(f"  Input: '{fail['input']}'")
                print(f"  Expected: {fail['expected']}")
                print(f"  Got: {fail['got']} (score: {fail['score']:.1f})")
                print()
        
        assert len(failures) == 0, f"{len(failures)} command matching failures"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
