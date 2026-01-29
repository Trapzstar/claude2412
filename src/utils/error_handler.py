# ============================================
# ERROR HANDLER - Centralized Error Management
# ============================================
import sys
import traceback

class ErrorHandler:
    """Centralized error handling with user-friendly messages"""
    
    ERROR_SOLUTIONS = {
        "microphone_not_found": {
            "title": "❌ Microphone Not Found",
            "solutions": [
                "1. Connect microphone USB cable",
                "2. Enable microphone in Settings → Privacy & Security → Microphone",
                "3. Restart this application",
                "4. Try a different microphone device (use --device flag)",
                "5. Update audio drivers from manufacturer"
            ]
        },
        "microphone_muted": {
            "title": "❌ Microphone Muted",
            "solutions": [
                "1. Check if microphone is physically muted",
                "2. Unmute in Windows Sound Settings",
                "3. Check application volume mixer (Settings → Volume mixer)",
                "4. Ensure microphone is not disabled in BIOS"
            ]
        },
        "no_speech_detected": {
            "title": "⏰ No Speech Detected",
            "solutions": [
                "1. Speak louder and clearer",
                "2. Move closer to microphone",
                "3. Ensure environment is quiet",
                "4. Check microphone is not covered",
                "5. Use --test-mic to verify microphone works"
            ]
        },
        "google_api_error": {
            "title": "❌ Google Speech API Error",
            "solutions": [
                "1. Check internet connection",
                "2. Verify Google Speech API is accessible",
                "3. Check firewall/proxy settings",
                "4. Try again in a few moments (rate limiting)",
                "5. Use offline mode if available (--offline)"
            ]
        },
        "audio_buffer_overflow": {
            "title": "❌ Audio Buffer Overflow",
            "solutions": [
                "1. Reduce ambient noise level",
                "2. Adjust microphone sensitivity in Settings",
                "3. Try different audio device",
                "4. Restart application"
            ]
        },
        "invalid_command": {
            "title": "⚠️ Invalid Command",
            "solutions": [
                "1. Say 'help' to see available commands",
                "2. Use exact phrases from help menu",
                "3. Speak clearly and pause between words",
                "4. Check if command confirmation is required"
            ]
        },
        "network_timeout": {
            "title": "❌ Network Timeout",
            "solutions": [
                "1. Check internet connection",
                "2. Verify you can access Google services",
                "3. Try again in a moment",
                "4. Check for network interruptions"
            ]
        }
    }
    
    def __init__(self, debug_mode=True):
        self.debug_mode = debug_mode
        self.retry_count = {}
    
    def handle_error(self, error_type, error_obj=None, context=""):
        """Handle error with user-friendly message and solutions"""
        print("\n" + "=" * 70)
        
        if error_type in self.ERROR_SOLUTIONS:
            solution = self.ERROR_SOLUTIONS[error_type]
            print(solution["title"])
            print("-" * 70)
            print("\n💡 SOLUTIONS:")
            for sol in solution["solutions"]:
                print(f"   {sol}")
        else:
            print(f"❌ Unknown Error: {error_type}")
            if error_obj:
                print(f"   Details: {str(error_obj)[:100]}")
        
        if context:
            print(f"\n📍 Context: {context}")
        
        if self.debug_mode and error_obj:
            print(f"\n🔧 Debug Info:")
            print(f"   {type(error_obj).__name__}: {str(error_obj)}")
            print(f"   Traceback: {traceback.format_exc()}")
        
        print("=" * 70 + "\n")
    
    def should_retry(self, error_type, max_retries=3):
        """Check if error should trigger retry logic"""
        if error_type not in self.retry_count:
            self.retry_count[error_type] = 0
        
        self.retry_count[error_type] += 1
        
        retryable_errors = [
            "network_timeout",
            "google_api_error",
            "audio_buffer_overflow",
            "no_speech_detected"
        ]
        
        return (
            error_type in retryable_errors and 
            self.retry_count[error_type] < max_retries
        )
    
    def reset_retry_count(self, error_type):
        """Reset retry counter for error type"""
        if error_type in self.retry_count:
            self.retry_count[error_type] = 0
    
    @staticmethod
    def format_error_message(error_obj, truncate=True):
        """Format error object as readable string"""
        msg = str(error_obj)
        if truncate and len(msg) > 100:
            return msg[:97] + "..."
        return msg

# Singleton instance
_error_handler = None

def get_error_handler(debug_mode=True):
    """Get or create singleton error handler"""
    global _error_handler
    if _error_handler is None:
        _error_handler = ErrorHandler(debug_mode)
    return _error_handler
