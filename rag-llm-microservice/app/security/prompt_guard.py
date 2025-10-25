import re
from typing import Tuple, Optional
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class PromptGuard:
    def __init__(self):
        self.blocked_patterns = settings.blocked_patterns
        self.max_length = settings.max_prompt_length
    
    def check_prompt(self, prompt: str) -> Tuple[bool, Optional[str]]:
        """
        Check if prompt is safe
        Returns: (is_safe, reason_if_unsafe)
        """
        # Check length
        if len(prompt) > self.max_length:
            return False, f"Prompt exceeds maximum length of {self.max_length}"
        
        # Check for blocked patterns
        prompt_lower = prompt.lower()
        for pattern in self.blocked_patterns:
            if pattern.lower() in prompt_lower:
                return False, f"Blocked pattern detected: {pattern}"
        
        # Check for potential code injection
        code_patterns = [
            r'<script[^>]*>.*?</script>',
            r'javascript:',
            r'on\w+\s*=',
            r'\$\{.*?\}',
        ]
        
        for pattern in code_patterns:
            if re.search(pattern, prompt, re.IGNORECASE):
                return False, f"Potential code injection detected"
        
        return True, None
    
    def sanitize_response(self, response: str) -> str:
        """Sanitize LLM response"""
        # Remove any potential HTML/script tags
        response = re.sub(r'<[^>]+>', '', response)
        return response.strip()