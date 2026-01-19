"""
Error handling utilities for AI service operations.
"""
import logging
from typing import Callable, Any, Optional
from functools import wraps
from ..config import settings

logger = logging.getLogger(__name__)


class AIServiceError(Exception):
    """Base exception for AI service operations."""
    pass


class AIServiceTimeoutError(AIServiceError):
    """Raised when AI service request times out."""
    pass


class AIServiceAuthenticationError(AIServiceError):
    """Raised when AI service authentication fails."""
    pass


class AIServiceRateLimitError(AIServiceError):
    """Raised when AI service rate limit is exceeded."""
    pass


class AIServiceUnavailableError(AIServiceError):
    """Raised when AI service is unavailable."""
    pass


def ai_fallback_handler(fallback_response: Optional[str] = None):
    """
    Decorator to handle AI service failures with fallback responses.

    Args:
        fallback_response: Optional fallback response to return on failure
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            try:
                return func(*args, **kwargs)
            except AIServiceAuthenticationError as e:
                logger.error(f"AI service authentication error: {str(e)}")
                return fallback_response or getattr(settings, 'fallback_response',
                                                   "I'm having trouble responding right now. Could you try rephrasing?")
            except AIServiceRateLimitError as e:
                logger.error(f"AI service rate limit error: {str(e)}")
                return fallback_response or getattr(settings, 'fallback_response',
                                                   "I'm experiencing high demand. Could you try again in a moment?")
            except AIServiceTimeoutError as e:
                logger.error(f"AI service timeout error: {str(e)}")
                return fallback_response or getattr(settings, 'fallback_response',
                                                   "I'm taking longer than usual to respond. Could you try again?")
            except AIServiceUnavailableError as e:
                logger.error(f"AI service unavailable error: {str(e)}")
                return fallback_response or getattr(settings, 'fallback_response',
                                                   "I'm temporarily unavailable. Could you try again later?")
            except AIServiceError as e:
                logger.error(f"AI service error: {str(e)}")
                return fallback_response or getattr(settings, 'fallback_response',
                                                   "I'm having trouble responding right now. Could you try rephrasing?")
            except Exception as e:
                logger.error(f"Unexpected error in AI service: {str(e)}")
                return fallback_response or getattr(settings, 'fallback_response',
                                                   "I encountered an unexpected issue. Could you try rephrasing?")
        return wrapper
    return decorator


def estimate_token_count(text: str) -> int:
    """
    Estimate the number of tokens in a text string.
    This is a rough approximation - 1 token is roughly 4 characters.

    Args:
        text: Input text to estimate tokens for

    Returns:
        Estimated number of tokens
    """
    if not text:
        return 0
    # Rough estimation: ~4 characters per token
    return len(text) // 4


def validate_token_limit(text: str, max_tokens: int) -> bool:
    """
    Validate that text does not exceed token limit.

    Args:
        text: Text to validate
        max_tokens: Maximum allowed tokens

    Returns:
        True if within limit, False otherwise
    """
    token_count = estimate_token_count(text)
    return token_count <= max_tokens