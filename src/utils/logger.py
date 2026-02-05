"""
Logger module for intent mapping and behavior rules system.
"""
import logging
import sys
from datetime import datetime
from typing import Any, Dict


class Logger:
    """Custom logger for the intent mapping system."""

    def __init__(self, name: str, level: int = logging.INFO):
        self.logger = logging.getLogger(name)

        # Avoid adding handlers multiple times
        if not self.logger.handlers:
            self.logger.setLevel(level)

            # Create formatter
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )

            # Create handler for stdout
            handler = logging.StreamHandler(sys.stdout)
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def info(self, message: str) -> None:
        """Log an info message."""
        self.logger.info(message)

    def warning(self, message: str) -> None:
        """Log a warning message."""
        self.logger.warning(message)

    def error(self, message: str) -> None:
        """Log an error message."""
        self.logger.error(message)

    def debug(self, message: str) -> None:
        """Log a debug message."""
        self.logger.debug(message)

    def log_intent_detected(self, user_input: str, detected_intent: str, confidence: float) -> None:
        """Log when an intent is detected."""
        self.info(f"Intent detected: {detected_intent} (confidence: {confidence:.2f}) "
                  f"from input: '{user_input[:50]}{'...' if len(user_input) > 50 else ''}'")

    def log_mcp_tool_call(self, tool_name: str, parameters: Dict[str, Any]) -> None:
        """Log MCP tool calls."""
        self.info(f"MCP tool called: {tool_name} with params: {list(parameters.keys())}")

    def log_validation_result(self, intent_type: str, is_valid: bool, errors: list) -> None:
        """Log validation results."""
        status = "PASSED" if is_valid else "FAILED"
        self.info(f"Validation {status} for intent {intent_type}: {len(errors)} errors")
        for error in errors:
            self.warning(f"Validation error: {error}")

    def log_safe_fallback(self, reason: str, fallback_message: str) -> None:
        """Log when a safe fallback is triggered."""
        self.warning(f"Safe fallback triggered: {reason} -> Response: '{fallback_message}'")