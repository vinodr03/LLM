import logging
from datetime import datetime
import json
from pathlib import Path

class SecurityLogger:
    def __init__(self, log_file: str = "logs/security.log"):
        Path("logs").mkdir(exist_ok=True)
        self.log_file = log_file
        
        # Configure logger
        self.logger = logging.getLogger("security")
        self.logger.setLevel(logging.INFO)
        
        # File handler
        fh = logging.FileHandler(log_file)
        fh.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)
    
    def log_query(self, query: str, flagged: bool, reason: str = None, 
                  response: str = None, ip: str = None):
        """Log security-relevant query information"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "query": query,
            "flagged": flagged,
            "reason": reason,
            "response": response,
            "ip_address": ip
        }
        
        if flagged:
            self.logger.warning(f"FLAGGED QUERY: {json.dumps(log_entry)}")
        else:
            self.logger.info(f"QUERY: {json.dumps(log_entry)}")