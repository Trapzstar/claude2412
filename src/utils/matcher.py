# ============================================
# ADAPTIVE MATCHER - Smart threshold adjustment
# ============================================
import time
from collections import deque

class AdaptiveMatcher:
    """Adaptive command matching with learning from success/failure patterns"""
    
    def __init__(self, base_threshold=6.0):
        self.base_threshold = base_threshold
        self.current_threshold = base_threshold
        
        # Track recent failures for adaptive adjustment
        self.recent_failures = deque(maxlen=10)
        self.recent_successes = deque(maxlen=10)
        
        # Command frequency tracking
        self.command_frequency = {}
        
        # User pronunciation patterns
        self.user_pronunciations = {}
    
    def adjust_threshold(self):
        """
        Dynamically adjust threshold based on recent performance
        Returns: adjusted threshold value
        """
        base = self.base_threshold
        
        # Factor 1: Recent failure rate
        failure_rate = len(self.recent_failures) / 10.0 if self.recent_failures else 0
        if failure_rate > 0.5:  # More than 50% failures
            adjustment = -0.5  # Lower threshold (be more lenient)
            if self.base_threshold == 6:
                reason = "High failure rate detected (tolerance mode)"
        else:
            adjustment = 0  # Keep normal
            reason = "Normal operation"
        
        # Factor 2: Confidence trend
        recent_avg_score = sum(self.recent_successes) / len(self.recent_successes) if self.recent_successes else 10
        if recent_avg_score > 12:
            adjustment += 0.5  # Slightly stricter (prevent false positives)
        
        self.current_threshold = max(3.0, min(8.0, base + adjustment))  # Clamp between 3.0-8.0
        
        return self.current_threshold, reason
    
    def record_success(self, command, score):
        """Record successful command match"""
        self.recent_successes.append(score)
        
        # Track command frequency
        if command not in self.command_frequency:
            self.command_frequency[command] = 0
        self.command_frequency[command] += 1
    
    def record_failure(self, text, best_score):
        """Record failed match attempt"""
        self.recent_failures.append(best_score)
        
        # Store pronunciation attempt
        key = text.lower().strip()
        if key not in self.user_pronunciations:
            self.user_pronunciations[key] = {
                'attempts': 0,
                'best_score': best_score,
                'last_attempt': time.time()
            }
        self.user_pronunciations[key]['attempts'] += 1
        self.user_pronunciations[key]['best_score'] = max(
            self.user_pronunciations[key]['best_score'],
            best_score
        )
    
    def learn_common_pronunciation(self, text, command):
        """
        Learn user's pronunciation for future recognition
        If user says something often and it matches a command,
        add it as a permanent variant
        """
        key = text.lower().strip()
        
        if key in self.user_pronunciations:
            info = self.user_pronunciations[key]
            
            # If attempted 3+ times and scored >= 5, it's a valid variant
            if info['attempts'] >= 3 and info['best_score'] >= 5:
                return {
                    'text': text,
                    'command': command,
                    'should_add': True,
                    'reason': f"User's common pronunciation (attempted {info['attempts']}x)"
                }
        
        return None
    
    def get_adaptive_threshold(self, command=None, score=None):
        """
        Get current adaptive threshold with factors considered
        
        Args:
            command: command being evaluated (for frequency analysis)
            score: confidence score of current match (for comparison)
        
        Returns:
            threshold value to use for decision
        """
        threshold, reason = self.adjust_threshold()
        
        # Factor 3: Command frequency boost
        if command and command in self.command_frequency:
            freq = self.command_frequency[command]
            if freq > 10:
                threshold = max(3.0, threshold - 0.5)  # More lenient for frequent commands
        
        return threshold
    
    def should_ask_confirmation(self, score):
        """
        Determine if command score is in the "uncertain" range
        where user confirmation would be helpful
        
        Returns: True if confirmation should be requested
        """
        # Confirmation range: between 8 and 12
        return 8 <= score < 12
    
    def explain_decision(self, text, command, score, threshold, accepted):
        """Generate explanation for command decision"""
        if accepted:
            return f"✅ {command} (confidence: {score:.1f} > threshold: {threshold:.1f})"
        else:
            return f"⚠️ Low confidence (score: {score:.1f} < threshold: {threshold:.1f}) - Need to retry"
    
    def get_statistics(self):
        """Return learning statistics"""
        return {
            'current_threshold': round(self.current_threshold, 2),
            'base_threshold': self.base_threshold,
            'recent_failures': len(self.recent_failures),
            'recent_successes': len(self.recent_successes),
            'commands_learned': len(self.command_frequency),
            'pronunciations_learned': len(self.user_pronunciations),
            'average_success_score': round(
                sum(self.recent_successes) / len(self.recent_successes)
                if self.recent_successes else 0, 2
            )
        }
