"""
Circuit breaker pattern implementation for AI API resilience.
"""
import time
import threading
from typing import Callable, Type, Any
from functools import wraps

class CircuitBreakerState:
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Tripped, requests blocked
    HALF_OPEN = "half_open" # Testing if failure condition is resolved


class CircuitBreakerError(Exception):
    """Raised when the circuit breaker is open and a request is attempted."""
    pass


class CircuitBreaker:
    """
    Circuit breaker implementation to handle API resilience.
    """

    def __init__(self, failure_threshold: int = 5, recovery_timeout: int = 60, expected_exception: Type[Exception] = Exception):
        """
        Initialize the circuit breaker.

        Args:
            failure_threshold: Number of failures before opening the circuit
            recovery_timeout: Time in seconds to wait before allowing a test request
            expected_exception: Exception type(s) to watch for
        """
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.expected_exception = expected_exception

        self.state = CircuitBreakerState.CLOSED
        self.failure_count = 0
        self.last_failure_time = None

        self._lock = threading.Lock()

    def call(self, func: Callable, *args, **kwargs) -> Any:
        """
        Call the protected function with circuit breaker logic.

        Args:
            func: The function to call
            *args: Arguments to pass to the function
            **kwargs: Keyword arguments to pass to the function

        Returns:
            Result of the function call
        """
        with self._lock:
            if self.state == CircuitBreakerState.OPEN:
                # Check if recovery timeout has passed
                if self.last_failure_time and (time.time() - self.last_failure_time) >= self.recovery_timeout:
                    self.state = CircuitBreakerState.HALF_OPEN
                else:
                    raise CircuitBreakerError("Circuit breaker is OPEN. Requests are blocked.")

        try:
            result = func(*args, **kwargs)

            with self._lock:
                if self.state == CircuitBreakerState.HALF_OPEN or self.state == CircuitBreakerState.CLOSED:
                    # Success, reset the circuit
                    self._success()

            return result

        except self.expected_exception as e:
            with self._lock:
                self._failure()
            raise e

    def _failure(self):
        """Record a failure and update the circuit state."""
        self.failure_count += 1
        self.last_failure_time = time.time()

        if self.failure_count >= self.failure_threshold:
            self.state = CircuitBreakerState.OPEN

    def _success(self):
        """Record a success and update the circuit state."""
        self.failure_count = 0
        self.state = CircuitBreakerState.CLOSED
        self.last_failure_time = None

    def __call__(self, func: Callable) -> Callable:
        """
        Decorator implementation of the circuit breaker.

        Args:
            func: The function to wrap

        Returns:
            Wrapped function with circuit breaker logic
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            return self.call(func, *args, **kwargs)
        return wrapper


# Global circuit breaker for AI service calls
ai_circuit_breaker = CircuitBreaker(
    failure_threshold=3,
    recovery_timeout=30,
    expected_exception=Exception  # Catch all exceptions for AI service
)