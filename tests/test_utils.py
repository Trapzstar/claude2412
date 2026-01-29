"""
Unit Tests for Utility Modules
Test all refactored utility functions and classes
"""

import pytest
import sys
import os
import tempfile
from typing import List, Dict, Any
from dataclasses import dataclass
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.helpers import (
    retry_operation, safe_call, get_audio_devices, find_best_device,
    validate_confidence, format_confidence, sanitize_text,
    group_by_key, flatten_dict, ensure_directory,
    safe_read_file, safe_write_file, Timer
)
from test_infrastructure import TestResult, TestRunner, ImportTestRunner


class TestRetryOperations:
    """Test retry and error handling utilities"""
    
    def test_retry_operation_success(self) -> None:
        """Test retry_operation succeeds on first try"""
        def successful_func() -> str:
            return "success"
        
        result = retry_operation(successful_func, max_attempts=3, verbose=False)
        assert result == "success"
    
    def test_retry_operation_eventual_success(self) -> None:
        """Test retry_operation succeeds after retries"""
        call_count = 0
        
        def eventually_successful() -> str:
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ValueError("Not yet")
            return "success"
        
        result = retry_operation(eventually_successful, max_attempts=5, delay=0.01, verbose=False)
        assert result == "success"
        assert call_count == 3
    
    def test_retry_operation_all_fail(self) -> None:
        """Test retry_operation returns None when all attempts fail"""
        def always_fails() -> str:
            raise ValueError("Always fails")
        
        result = retry_operation(always_fails, max_attempts=2, delay=0.01, verbose=False)
        assert result is None
    
    def test_safe_call_success(self) -> None:
        """Test safe_call succeeds"""
        def func() -> str:
            return "result"
        
        result = safe_call(func, default="default", verbose=False)
        assert result == "result"
    
    def test_safe_call_with_exception(self) -> None:
        """Test safe_call returns default on exception"""
        def func() -> str:
            raise ValueError("error")
        
        result = safe_call(func, default="default", verbose=False)
        assert result == "default"


class TestDeviceManagement:
    """Test device detection and selection utilities"""
    
    def test_find_best_device_empty_list(self) -> None:
        """Test find_best_device with empty device list"""
        result = find_best_device([])
        assert result == 0
    
    def test_find_best_device_single_device(self) -> None:
        """Test find_best_device with single device"""
        devices = [{"index": 0, "name": "Device 1", "channels": 2}]
        result = find_best_device(devices)
        assert result == 0
    
    def test_find_best_device_scores_array(self) -> None:
        """Test find_best_device prioritizes array microphone"""
        devices = [
            {"index": 0, "name": "Microphone", "channels": 1},
            {"index": 1, "name": "Array Microphone", "channels": 2},
            {"index": 2, "name": "USB Mic", "channels": 1}
        ]
        result = find_best_device(devices)
        assert result == 1  # Array microphone should win
    
    def test_find_best_device_scores_realtek(self) -> None:
        """Test find_best_device prioritizes Realtek"""
        devices = [
            {"index": 0, "name": "Microphone", "channels": 1},
            {"index": 1, "name": "Realtek Audio", "channels": 2},
            {"index": 2, "name": "USB Mic", "channels": 1}
        ]
        result = find_best_device(devices)
        assert result == 1  # Realtek should win
    
    def test_find_best_device_scores_multi_channel(self) -> None:
        """Test find_best_device prioritizes multi-channel"""
        devices = [
            {"index": 0, "name": "Microphone", "channels": 1},
            {"index": 1, "name": "Stereo Mic", "channels": 2},
            {"index": 2, "name": "Mono Mic", "channels": 1}
        ]
        result = find_best_device(devices)
        assert result == 1  # Stereo should win


class TestValidationFormatting:
    """Test validation and formatting utilities"""
    
    def test_validate_confidence_below_zero(self) -> None:
        """Test confidence below 0 is clamped"""
        result = validate_confidence(-10)
        assert result == 0.0
    
    def test_validate_confidence_above_100(self) -> None:
        """Test confidence above 100 is clamped"""
        result = validate_confidence(150)
        assert result == 100.0
    
    def test_validate_confidence_valid(self) -> None:
        """Test valid confidence is unchanged"""
        result = validate_confidence(75.5)
        assert result == 75.5
    
    def test_format_confidence_high(self) -> None:
        """Test format_confidence for high confidence"""
        result = format_confidence(85)
        assert "[OK]" in result
        assert "green" in result
    
    def test_format_confidence_medium(self) -> None:
        """Test format_confidence for medium confidence"""
        result = format_confidence(70)
        assert "[WARN]" in result
        assert "yellow" in result
    
    def test_format_confidence_low(self) -> None:
        """Test format_confidence for low confidence"""
        result = format_confidence(30)
        assert "[FAIL]" in result
        assert "red" in result
    
    def test_sanitize_text_normal(self) -> None:
        """Test sanitize_text with normal input"""
        result = sanitize_text("hello world")
        assert result == "hello world"
    
    def test_sanitize_text_extra_spaces(self) -> None:
        """Test sanitize_text removes extra spaces"""
        result = sanitize_text("hello   world")
        assert result == "hello world"
    
    def test_sanitize_text_truncate(self) -> None:
        """Test sanitize_text truncates long text"""
        long_text = "a" * 150
        result = sanitize_text(long_text, max_length=100)
        assert len(result) == 100
        assert result.endswith("...")
    
    def test_sanitize_text_empty(self) -> None:
        """Test sanitize_text handles empty string"""
        result = sanitize_text("")
        assert result == ""


class TestDataProcessing:
    """Test data processing utilities"""
    
    def test_group_by_key_single_key(self) -> None:
        """Test group_by_key with single key value"""
        items = [
            {"type": "A", "value": 1},
            {"type": "A", "value": 2}
        ]
        result = group_by_key(items, "type")
        assert "A" in result
        assert len(result["A"]) == 2
    
    def test_group_by_key_multiple_keys(self) -> None:
        """Test group_by_key with multiple key values"""
        items = [
            {"type": "A", "value": 1},
            {"type": "B", "value": 2},
            {"type": "A", "value": 3}
        ]
        result = group_by_key(items, "type")
        assert len(result["A"]) == 2
        assert len(result["B"]) == 1
    
    def test_group_by_key_missing_key(self) -> None:
        """Test group_by_key skips items without key"""
        items = [
            {"type": "A", "value": 1},
            {"value": 2},  # Missing 'type'
            {"type": "A", "value": 3}
        ]
        result = group_by_key(items, "type")
        assert len(result["A"]) == 2
        assert len(result) == 1
    
    def test_flatten_dict_simple(self) -> None:
        """Test flatten_dict with simple nested dict"""
        d = {"a": {"b": 1, "c": 2}, "d": 3}
        result = flatten_dict(d)
        assert result["a.b"] == 1
        assert result["a.c"] == 2
        assert result["d"] == 3
    
    def test_flatten_dict_deep_nesting(self) -> None:
        """Test flatten_dict with deep nesting"""
        d = {"a": {"b": {"c": 1}}}
        result = flatten_dict(d)
        assert result["a.b.c"] == 1
    
    def test_flatten_dict_custom_separator(self) -> None:
        """Test flatten_dict with custom separator"""
        d = {"a": {"b": 1}}
        result = flatten_dict(d, sep="-")
        assert "a-b" in result


class TestFileOperations:
    """Test file operation utilities"""
    
    def test_ensure_directory_creates(self) -> None:
        """Test ensure_directory creates directory"""
        with tempfile.TemporaryDirectory() as tmpdir:
            new_dir = os.path.join(tmpdir, "test_dir")
            result = ensure_directory(new_dir)
            assert result is True
            assert os.path.isdir(new_dir)
    
    def test_ensure_directory_existing(self) -> None:
        """Test ensure_directory with existing directory"""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = ensure_directory(tmpdir)
            assert result is True
    
    def test_safe_read_file_success(self) -> None:
        """Test safe_read_file reads file content"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("test content")
            f.flush()
            temp_path = f.name
        
        try:
            result = safe_read_file(temp_path)
            assert result == "test content"
        finally:
            os.unlink(temp_path)
    
    def test_safe_read_file_nonexistent(self) -> None:
        """Test safe_read_file returns default for nonexistent file"""
        result = safe_read_file("/nonexistent/path/file.txt", default="default")
        assert result == "default"
    
    def test_safe_write_file_success(self) -> None:
        """Test safe_write_file writes content"""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "test.txt")
            result = safe_write_file(path, "test content")
            assert result is True
            with open(path, 'r') as f:
                assert f.read() == "test content"
    
    def test_safe_write_file_invalid_path(self) -> None:
        """Test safe_write_file handles invalid path"""
        result = safe_write_file("/nonexistent/path/file.txt", "content")
        assert result is False


class TestTimer:
    """Test Timer context manager"""
    
    def test_timer_measures_time(self) -> None:
        """Test Timer measures execution time"""
        import time
        with Timer("test", verbose=False) as timer:
            time.sleep(0.1)
        
        assert timer.elapsed >= 0.09  # Allow small variation
    
    def test_timer_context_manager(self) -> None:
        """Test Timer works as context manager"""
        with Timer("test", verbose=False) as timer:
            assert timer.start_time is not None
        
        assert timer.elapsed > 0


class TestTestRunner:
    """Test test infrastructure utilities"""
    
    def test_test_runner_pass(self) -> None:
        """Test TestRunner tracks passed tests"""
        runner = TestRunner(verbose=False)
        runner.run_test("test1", lambda: True)
        
        assert runner.passed_count == 1
        assert runner.failed_count == 0
    
    def test_test_runner_fail(self) -> None:
        """Test TestRunner tracks failed tests"""
        runner = TestRunner(verbose=False)
        runner.run_test("test1", lambda: False)
        
        assert runner.passed_count == 0
        assert runner.warning_count == 1
    
    def test_test_runner_exception(self) -> None:
        """Test TestRunner tracks exceptions"""
        runner = TestRunner(verbose=False)
        runner.run_test("test1", lambda: 1/0)
        
        assert runner.failed_count == 1
        assert len(runner.results) == 1
        assert runner.results[0].error is not None
    
    def test_test_result_dataclass(self) -> None:
        """Test TestResult dataclass"""
        result = TestResult("test", True, "passed")
        assert result.name == "test"
        assert result.passed is True


class TestImportTestRunner:
    """Test import test infrastructure"""
    
    def test_import_test_runner_valid_import(self) -> None:
        """Test ImportTestRunner validates valid imports"""
        runner = ImportTestRunner(verbose=False)
        result = runner.run_import_test("config", "config.get_config")
        
        assert result.passed is True
    
    def test_import_test_runner_invalid_import(self) -> None:
        """Test ImportTestRunner handles invalid imports"""
        runner = ImportTestRunner(verbose=False)
        result = runner.run_import_test("invalid", "nonexistent_module.func")
        
        assert result.passed is False
        assert result.error is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
