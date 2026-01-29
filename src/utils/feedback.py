# ============================================
# FEEDBACK UI - Real-time User Feedback
# ============================================
import sys

class FeedbackUI:
    """Display real-time feedback to user"""
    
    STATES = {
        "listening": ("🎤 RECORDING", "Listening for voice input..."),
        "processing": ("🔄 PROCESSING", "Processing audio..."),
        "matching": ("🔍 MATCHING", "Matching command..."),
        "confirming": ("❓ CONFIRM", "Say 'yes' to confirm or 'no' to cancel"),
        "executing": ("⚡ EXECUTING", "Executing command..."),
        "success": ("✅ SUCCESS", "Command executed successfully"),
        "retry": ("🔄 RETRY", "Retrying..."),
        "error": ("❌ ERROR", "An error occurred"),
    }
    
    def __init__(self, verbose=True):
        self.verbose = verbose
        self.current_state = None
    
    def show_state(self, state, duration=None):
        """Display current state"""
        if state not in self.STATES:
            return
        
        emoji, message = self.STATES[state]
        self.current_state = state
        
        if self.verbose:
            print(f"\n    {emoji} {message}")
            if duration:
                print(f"       ({duration})")
    
    def show_confidence(self, command, score, max_score=10, threshold=6):
        """Display confidence score with visual indicator"""
        percentage = (score / max_score) * 100
        bar_length = 20
        filled = int((score / max_score) * bar_length)
        bar = "█" * filled + "░" * (bar_length - filled)
        
        # Color based on confidence
        if score >= threshold * 1.5:
            confidence_level = "🟢 HIGH"
        elif score >= threshold:
            confidence_level = "🟡 MEDIUM"
        else:
            confidence_level = "🔴 LOW"
        
        if self.verbose:
            print(f"\n    📊 Confidence: {confidence_level}")
            print(f"       [{bar}] {percentage:.0f}%")
            print(f"       Command: {command}")
            print(f"       Score: {score}/{max_score}")
    
    def show_retry_info(self, attempt, max_attempts, delay=None):
        """Display retry information"""
        remaining = max_attempts - attempt
        
        if self.verbose:
            print(f"\n    🔄 RETRY ATTEMPT {attempt}/{max_attempts}")
            if delay:
                print(f"       Retrying in {delay} second(s)...")
            print(f"       {remaining} attempt(s) remaining")
    
    def show_progress(self, current, total, task=""):
        """Display progress indicator"""
        if total == 0:
            return
        
        percentage = (current / total) * 100
        bar_length = 20
        filled = int((current / total) * bar_length)
        bar = "█" * filled + "░" * (bar_length - filled)
        
        if self.verbose:
            task_str = f" - {task}" if task else ""
            print(f"\n    📈 Progress{task_str}")
            print(f"       [{bar}] {percentage:.0f}% ({current}/{total})")
    
    def show_error_brief(self, error_message):
        """Show brief error message (full details in error handler)"""
        if self.verbose:
            print(f"\n    ❌ {error_message}")
    
    def show_suggestion(self, suggestion):
        """Show helpful suggestion to user"""
        if self.verbose:
            print(f"\n    💡 Tip: {suggestion}")
    
    def clear_current_state(self):
        """Clear current state display"""
        self.current_state = None
    
    def show_waiting(self, dots=3):
        """Show waiting animation with dots"""
        if self.verbose:
            dots_str = "." * (dots % 4)
            print(f"    ⏳ Processing{dots_str}", end="\r", flush=True)
    
    def show_result(self, command, success=True):
        """Show command result"""
        if success:
            print(f"\n    ✅ Executed: {command}")
        else:
            print(f"\n    ❌ Failed: {command}")
    
    @staticmethod
    def format_duration(seconds):
        """Format duration in human readable format"""
        if seconds < 1:
            return f"{seconds*1000:.0f}ms"
        elif seconds < 60:
            return f"{seconds:.1f}s"
        else:
            minutes = seconds / 60
            return f"{minutes:.1f}m"

# Singleton instance
_feedback_ui = None

def get_feedback_ui(verbose=True):
    """Get or create singleton feedback UI"""
    global _feedback_ui
    if _feedback_ui is None:
        _feedback_ui = FeedbackUI(verbose)
    return _feedback_ui
