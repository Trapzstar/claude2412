"""
Utility Functions - Common patterns extracted for DRY (Don't Repeat Yourself) principle
Reduces code duplication across the application
"""

from typing import Optional, List, Dict, Any, Callable, TypeVar
from rich.console import Console
import sys
import time

console = Console()

T = TypeVar('T')


# ============================================
# RETRY & ERROR HANDLING UTILITIES
# ============================================

def retry_operation(
    func: Callable[..., T],
    max_attempts: int = 3,
    delay: float = 0.5,
    backoff: float = 1.0,
    verbose: bool = True
) -> Optional[T]:
    """
    Retry an operation multiple times with exponential backoff.
    
    Args:
        func: Function to retry
        max_attempts: Maximum number of attempts
        delay: Initial delay between retries in seconds
        backoff: Multiplier for delay each retry
        verbose: Print retry messages
        
    Returns:
        Result of function or None if all attempts fail
    """
    current_delay = delay
    
    for attempt in range(1, max_attempts + 1):
        try:
            return func()
        except Exception as e:
            if attempt == max_attempts:
                if verbose:
                    console.print(f"[red][FAIL] Failed after {max_attempts} attempts[/red]")
                return None
            
            if verbose:
                console.print(f"[yellow][RETRY] Attempt {attempt}/{max_attempts} failed: {str(e)[:50]}...[/yellow]")
            
            time.sleep(current_delay)
            current_delay *= backoff
    
    return None


def safe_call(
    func: Callable[..., T],
    default: T = None,
    error_message: str = "",
    verbose: bool = True
) -> T:
    """
    Call a function safely with exception handling.
    
    Args:
        func: Function to call
        default: Default value if exception occurs
        error_message: Message to display on error
        verbose: Print error messages
        
    Returns:
        Function result or default value
    """
    try:
        return func()
    except Exception as e:
        if verbose:
            msg = error_message or f"Error: {str(e)[:50]}..."
            console.print(f"[yellow][WARN] {msg}[/yellow]")
        return default


# ============================================
# DEVICE MANAGEMENT UTILITIES
# ============================================

def get_audio_devices() -> List[Dict[str, Any]]:
    """
    Get list of available audio input devices.
    
    Returns:
        List of device dictionaries with 'index', 'name', 'channels' keys
    """
    try:
        import pyaudio
        audio = pyaudio.PyAudio()
        devices = []
        
        for i in range(audio.get_device_count()):
            device_info = audio.get_device_info_by_index(i)
            if device_info.get('maxInputChannels') > 0:
                devices.append({
                    'index': i,
                    'name': device_info.get('name', 'Unknown'),
                    'channels': device_info.get('maxInputChannels', 0)
                })
        
        audio.terminate()
        return devices
        
    except Exception as e:
        console.print(f"[red]Error getting devices: {e}[/red]")
        return []


def find_best_device(devices: List[Dict[str, Any]]) -> int:
    """
    Find best audio device using heuristic scoring.
    
    Scoring: array (100) > realtek (50) > microphone (30) > multi-channel (20) > usb (15)
    
    Args:
        devices: List of device dictionaries
        
    Returns:
        Device index of best device, or 0 (first device) if list is empty
    """
    if not devices:
        return 0
    
    best_device = 0
    best_score = 0
    
    for device in devices:
        score = 0
        name_lower = device['name'].lower()
        channels = device.get('channels', 0)
        
        # Scoring system
        if 'array' in name_lower:
            score += 100
        if 'realtek' in name_lower:
            score += 50
        if 'microphone' in name_lower:
            score += 30
        if channels >= 2:
            score += 20
        if 'usb' in name_lower:
            score += 15
        
        # Update best if this is better
        if score > best_score:
            best_score = score
            best_device = device['index']
    
    return best_device


# ============================================
# VALIDATION & FORMATTING UTILITIES
# ============================================

def validate_confidence(confidence: float) -> float:
    """
    Validate and normalize confidence value to 0-100 range.
    
    Args:
        confidence: Confidence value (may be any range)
        
    Returns:
        Normalized confidence between 0-100
    """
    if confidence < 0:
        return 0.0
    if confidence > 100:
        return 100.0
    return float(confidence)


def format_confidence(confidence: float) -> str:
    """
    Format confidence value as colored string.
    
    Args:
        confidence: Confidence value (0-100)
        
    Returns:
        Formatted string with color code
    """
    confidence = validate_confidence(confidence)
    
    if confidence >= 80:
        color = "green"
        icon = "[OK]"
    elif confidence >= 60:
        color = "yellow"
        icon = "[WARN]"
    else:
        color = "red"
        icon = "[FAIL]"
    
    return f"{icon} [{color}]{confidence:.0f}%[/{color}]"


def sanitize_text(text: str, max_length: int = 100) -> str:
    """
    Sanitize and truncate text for display.
    
    Args:
        text: Text to sanitize
        max_length: Maximum length
        
    Returns:
        Sanitized text
    """
    if not text:
        return ""
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    # Truncate if needed
    if len(text) > max_length:
        text = text[:max_length-3] + "..."
    
    return text


# ============================================
# UI/CONSOLE UTILITIES
# ============================================

def print_separator(title: str = "", char: str = "=", width: int = 60) -> None:
    """
    Print a separator line with optional title.
    
    Args:
        title: Optional title to center
        char: Character to use for line
        width: Total width of separator
    """
    if title:
        padding = (width - len(title) - 2) // 2
        line = char * padding + " " + title + " " + char * (width - padding - len(title) - 2)
        console.print(line)
    else:
        console.print(char * width)


def print_status(status: str, message: str = "", color: str = "cyan") -> None:
    """
    Print a status message with consistent formatting.
    
    Args:
        status: Status label (e.g., "OK", "WARN", "FAIL")
        message: Optional message
        color: Color for status label
    """
    if message:
        console.print(f"[{color}][{status}][/{color}] {message}")
    else:
        console.print(f"[{color}][{status}][/{color}]")


def pause_and_continue(message: str = "Press Enter to continue...") -> None:
    """
    Pause execution and wait for user input.
    
    Args:
        message: Message to display
    """
    try:
        input(f"\n[dim]{message}[/dim]\n")
    except (KeyboardInterrupt, EOFError):
        raise KeyboardInterrupt("User interrupted")


# ============================================
# TIMING & PERFORMANCE UTILITIES
# ============================================

class Timer:
    """Context manager for measuring execution time"""
    
    def __init__(self, name: str = "Operation", verbose: bool = True):
        self.name = name
        self.verbose = verbose
        self.start_time: Optional[float] = None
        self.elapsed: float = 0.0
    
    def __enter__(self):
        self.start_time = time.time()
        if self.verbose:
            console.print(f"[dim]⏱️ {self.name}...[/dim]", end=" ")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.elapsed = time.time() - self.start_time
        if self.verbose:
            console.print(f"[dim](took {self.elapsed:.2f}s)[/dim]")
        return False


# ============================================
# DATA PROCESSING UTILITIES
# ============================================

def group_by_key(items: List[Dict[str, Any]], key: str) -> Dict[str, List[Dict[str, Any]]]:
    """
    Group list of dictionaries by a specific key.
    
    Args:
        items: List of dictionaries
        key: Key to group by
        
    Returns:
        Dictionary with key values as keys, items as values
    """
    grouped: Dict[str, List[Dict[str, Any]]] = {}
    for item in items:
        if key in item:
            k = item[key]
            if k not in grouped:
                grouped[k] = []
            grouped[k].append(item)
    return grouped


def flatten_dict(d: Dict[str, Any], parent_key: str = '', sep: str = '.') -> Dict[str, Any]:
    """
    Flatten nested dictionary.
    
    Args:
        d: Dictionary to flatten
        parent_key: Parent key for recursion
        sep: Separator for nested keys
        
    Returns:
        Flattened dictionary
    """
    items: List[tuple] = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


# ============================================
# FILE & PATH UTILITIES
# ============================================

def ensure_directory(path: str) -> bool:
    """
    Ensure a directory exists, create if needed.
    
    Args:
        path: Path to directory
        
    Returns:
        True if successful, False otherwise
    """
    try:
        import os
        os.makedirs(path, exist_ok=True)
        return True
    except Exception as e:
        console.print(f"[red]Error creating directory: {e}[/red]")
        return False


def safe_read_file(path: str, default: str = "") -> str:
    """
    Safely read file content.
    
    Args:
        path: File path
        default: Default content if read fails
        
    Returns:
        File content or default
    """
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        console.print(f"[yellow][WARN] Error reading {path}: {e}[/yellow]")
        return default


def safe_write_file(path: str, content: str) -> bool:
    """
    Safely write content to file.
    
    Args:
        path: File path
        content: Content to write
        
    Returns:
        True if successful, False otherwise
    """
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        console.print(f"[red]Error writing {path}: {e}[/red]")
        return False
