# ============================================
# INPUT VALIDATOR - Security & Input Validation
# ============================================
import re
import string

class InputValidator:
    """Validate and sanitize voice input for security"""
    
    # Allowed characters in commands
    ALLOWED_COMMAND_CHARS = set(string.ascii_lowercase + string.digits + " ")
    
    # Dangerous patterns to block
    DANGEROUS_PATTERNS = [
        r"[;&|`$(){}]",  # Shell injection attempts
        r"\.\.[\\/]",     # Path traversal
        r"<|>",            # Redirection
        r"--",             # Double dash (flags)
    ]
    
    # Commands that are safe to execute
    SAFE_COMMANDS = {
        "next", "previous", "stop", "help", "test",
        "open_slideshow", "close_slideshow", "noise",
        "popup_on", "popup_off", "caption_on", "caption_off",
        "change_language", "show_analytics", "unknown"
    }
    
    @staticmethod
    def sanitize_voice_input(text):
        """Remove potentially dangerous characters from voice input"""
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower().strip()
        
        # Remove extra whitespace
        text = " ".join(text.split())
        
        # Remove special characters that shouldn't be in voice input
        # Keep only letters, numbers, and basic punctuation
        text = re.sub(r"[^\w\s\-\.\,\!\?]", "", text)
        
        return text
    
    @staticmethod
    def validate_command(command):
        """Validate that command is in safe list"""
        return command in InputValidator.SAFE_COMMANDS
    
    @staticmethod
    def is_dangerous(text):
        """Check if text contains dangerous patterns"""
        if not text:
            return False
        
        for pattern in InputValidator.DANGEROUS_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        
        return False
    
    @staticmethod
    def check_injection_attempt(text):
        """Check for command injection attempts"""
        dangerous_keywords = [
            "exec", "eval", "system", "import",
            "subprocess", "os.system", "shell",
            "cmd", "powershell", "bash"
        ]
        
        text_lower = text.lower() if text else ""
        for keyword in dangerous_keywords:
            if keyword in text_lower:
                return True
        
        return False
    
    @staticmethod
    def validate_file_path(filepath):
        """Validate file path for safety"""
        # Prevent path traversal
        if ".." in filepath or filepath.startswith("/"):
            return False
        
        # Only allow specific directories
        safe_dirs = ["logs", "data", "cache", "."]
        if not any(filepath.startswith(d) for d in safe_dirs):
            return False
        
        return True
    
    @staticmethod
    def validate_and_sanitize(text):
        """Complete validation and sanitization"""
        if not text or not isinstance(text, str):
            return None, "Invalid input"
        
        # Check for injection attempts
        if InputValidator.check_injection_attempt(text):
            return None, "Potential injection attempt detected"
        
        # Check for dangerous patterns
        if InputValidator.is_dangerous(text):
            return None, "Dangerous characters detected"
        
        # Sanitize
        sanitized = InputValidator.sanitize_voice_input(text)
        
        if not sanitized or len(sanitized) < 2:
            return None, "Input too short or invalid"
        
        if len(sanitized) > 200:
            return None, "Input too long"
        
        return sanitized, None

# Singleton instance
_validator = None

def get_validator():
    """Get or create singleton validator"""
    global _validator
    if _validator is None:
        _validator = InputValidator()
    return _validator
