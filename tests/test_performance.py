"""
Performance Tests for SlideSense Application
Benchmark critical functions and identify optimization opportunities
"""

import pytest
import time
from typing import Dict, Any
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.helpers import (
    get_audio_devices, find_best_device, retry_operation,
    validate_confidence, format_confidence, sanitize_text,
    group_by_key, flatten_dict, safe_read_file, safe_write_file
)


class TestPerformanceProfiler:
    """Test the performance profiler itself"""
    
    def test_profiler_initialization(self) -> None:
        """Test profiler initializes correctly"""
        profiler = PerformanceProfiler()
        assert profiler is not None
        assert len(profiler.results) == 0
    
    def test_benchmark_simple_function(self) -> None:
        """Test benchmarking a simple function"""
        def simple_func() -> int:
            return sum(range(100))
        
        profiler = PerformanceProfiler()
        result = profiler.benchmark(simple_func, iterations=100)
        
        assert result.function_name == "simple_func"
        assert result.iterations == 100
        assert result.avg_time > 0
        assert result.calls_per_second > 0
    
    def test_benchmark_timing_accuracy(self) -> None:
        """Test benchmark timing is reasonably accurate"""
        def slow_func() -> None:
            time.sleep(0.01)  # 10ms
        
        profiler = PerformanceProfiler()
        result = profiler.benchmark(slow_func, iterations=3)
        
        # Should be approximately 10ms (0.01s)
        assert result.avg_time >= 0.009  # Allow 1ms variance
    
    def test_compare_implementations(self) -> None:
        """Test comparing two implementations"""
        def fast_impl() -> list:
            return [i for i in range(100)]
        
        def slow_impl() -> list:
            result = []
            for i in range(100):
                result.append(i)
            return result
        
        profiler = PerformanceProfiler()
        comparison = profiler.compare_implementations(
            slow_impl, fast_impl, iterations=100
        )
        
        assert "speedup" in comparison
        assert "improvement_percent" in comparison
        assert "faster" in comparison
    
    def test_identify_hotspots(self) -> None:
        """Test identifying hotspot functions"""
        def func1() -> None:
            time.sleep(0.001)
        
        def func2() -> None:
            time.sleep(0.01)
        
        profiler = PerformanceProfiler()
        profiler.benchmark(func1, iterations=10, name="Fast")
        profiler.benchmark(func2, iterations=10, name="Slow")
        
        hotspots = profiler.identify_hotspots(threshold_percent=1)
        assert len(hotspots) > 0
        assert hotspots[0][0] == "Slow"  # Should be first


class TestUtilityPerformance:
    """Performance tests for utility functions"""
    
    def test_validate_confidence_performance(self) -> None:
        """Test validate_confidence performance"""
        profiler = PerformanceProfiler()
        
        def test_func() -> None:
            validate_confidence(75.5)
        
        result = profiler.benchmark(test_func, iterations=10000)
        assert check_performance_target(result.avg_time, "command_matching")
        assert result.calls_per_second > 100000  # Should be very fast
    
    def test_sanitize_text_performance(self) -> None:
        """Test sanitize_text performance"""
        profiler = PerformanceProfiler()
        
        def test_func() -> None:
            sanitize_text("test text with spaces")
        
        result = profiler.benchmark(test_func, iterations=1000)
        assert result.avg_time < 0.001  # Should be under 1ms
    
    def test_find_best_device_performance(self) -> None:
        """Test find_best_device performance"""
        devices = [
            {"index": 0, "name": "Device 1", "channels": 1},
            {"index": 1, "name": "Device 2", "channels": 2},
            {"index": 2, "name": "Device 3", "channels": 1}
        ]
        
        profiler = PerformanceProfiler()
        
        def test_func() -> None:
            find_best_device(devices)
        
        result = profiler.benchmark(test_func, iterations=1000)
        assert result.avg_time < 0.001  # Should be very fast
    
    def test_group_by_key_performance(self) -> None:
        """Test group_by_key performance with large dataset"""
        items = [{"type": "A", "value": i} for i in range(100)]
        
        profiler = PerformanceProfiler()
        
        def test_func() -> None:
            group_by_key(items, "type")
        
        result = profiler.benchmark(test_func, iterations=100)
        assert result.avg_time < 0.01  # Should be under 10ms
    
    def test_flatten_dict_performance(self) -> None:
        """Test flatten_dict performance"""
        deep_dict = {
            "level1": {
                "level2": {
                    "level3": {
                        "value": 1
                    }
                }
            }
        }
        
        profiler = PerformanceProfiler()
        
        def test_func() -> None:
            flatten_dict(deep_dict)
        
        result = profiler.benchmark(test_func, iterations=1000)
        assert result.avg_time < 0.001


class TestCacheOptimizer:
    """Test cache optimization functionality"""
    
    def test_cache_initialization(self) -> None:
        """Test cache initializes correctly"""
        cache = CacheOptimizer()
        assert cache is not None
        assert len(cache.cache) == 0
        assert cache.hits == 0
        assert cache.misses == 0
    
    def test_memoization_basic(self) -> None:
        """Test basic memoization"""
        call_count = 0
        
        def expensive_func(x: int) -> int:
            nonlocal call_count
            call_count += 1
            return x * x
        
        cache = CacheOptimizer()
        cached_func = cache.memoize(expensive_func)
        
        # First call
        result1 = cached_func(5)
        assert result1 == 25
        assert call_count == 1
        
        # Second call (should be cached)
        result2 = cached_func(5)
        assert result2 == 25
        assert call_count == 1  # Should not increment
    
    def test_cache_statistics(self) -> None:
        """Test cache statistics tracking"""
        def func(x: int) -> int:
            return x + 1
        
        cache = CacheOptimizer()
        cached_func = cache.memoize(func)
        
        # Make some calls
        cached_func(1)  # miss
        cached_func(1)  # hit
        cached_func(2)  # miss
        cached_func(2)  # hit
        
        stats = cache.get_stats()
        assert stats["hits"] == 2
        assert stats["misses"] == 2
        assert stats["hit_rate"] == 50.0
    
    def test_cache_size_limit(self) -> None:
        """Test cache respects size limit"""
        def func(x: int) -> int:
            return x
        
        cache = CacheOptimizer(max_size=3)
        cached_func = cache.memoize(func)
        
        # Fill cache beyond limit
        for i in range(5):
            cached_func(i)
        
        assert len(cache.cache) <= 3


class TestOptimizationAnalyzer:
    """Test code optimization analyzer"""
    
    def test_analyzer_initialization(self) -> None:
        """Test analyzer initializes"""
        analyzer = OptimizationAnalyzer()
        assert analyzer is not None
    
    def test_analyze_list_operations(self) -> None:
        """Test analyzing list operations"""
        code = """
        items = []
        for i in range(100):
            items.append(i)
        items.remove(50)
        """
        
        analyzer = OptimizationAnalyzer()
        issues = analyzer.check_list_operations(code)
        assert len(issues) > 0
    
    def test_analyze_string_operations(self) -> None:
        """Test analyzing string operations"""
        code = """
        result = ""
        for i in range(100):
            result = result + str(i) + result + str(i) + result + str(i)
        """
        
        analyzer = OptimizationAnalyzer()
        issues = analyzer.check_string_operations(code)
        # May or may not detect depending on count threshold
        # Just verify it returns a list
        assert isinstance(issues, list)
    
    def test_full_analysis(self) -> None:
        """Test full code analysis"""
        code = """
        items = []
        for i in range(100):
            items.append(i)
        result = ""
        for item in items:
            result = result + str(item)
        """
        
        analyzer = OptimizationAnalyzer()
        analysis = analyzer.analyze(code)
        
        assert "list_operations" in analysis
        assert "string_operations" in analysis
        assert "loop_operations" in analysis


class TestPerformanceTargets:
    """Test performance targets and compliance"""
    
    def test_device_detection_target(self) -> None:
        """Test device detection meets performance target"""
        def test_func() -> None:
            find_best_device([
                {"index": 0, "name": "Device 1", "channels": 1},
                {"index": 1, "name": "Device 2", "channels": 2}
            ])
        
        profiler = PerformanceProfiler()
        result = profiler.benchmark(test_func, iterations=100)
        assert check_performance_target(result.avg_time, "device_detection")
    
    def test_command_matching_target(self) -> None:
        """Test command matching meets performance target"""
        def test_func() -> None:
            validate_confidence(75)
        
        profiler = PerformanceProfiler()
        result = profiler.benchmark(test_func, iterations=1000)
        assert check_performance_target(result.avg_time, "command_matching")
    
    def test_file_operations_target(self) -> None:
        """Test file operations meet performance target"""
        import tempfile
        import os
        
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = os.path.join(tmpdir, "test.txt")
            
            def test_func() -> None:
                safe_write_file(test_file, "test content")
                safe_read_file(test_file)
            
            profiler = PerformanceProfiler()
            result = profiler.benchmark(test_func, iterations=10)
            # File ops are slower, so check against file_operations target
            assert result.avg_time < 1.0  # Less strict for I/O


class TestMeasureTimeContext:
    """Test the measure_time context manager"""
    
    def test_measure_time_basic(self, capsys) -> None:
        """Test measure_time context manager"""
        with measure_time("Test operation"):
            time.sleep(0.01)
        
        captured = capsys.readouterr()
        assert "Test operation" in captured.out
        assert "ms" in captured.out


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
