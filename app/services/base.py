"""
Example service module demonstrating how to use request_id in service layer.
"""

import logging

from utils.logger import get_request_id


class BaseService:
    """Base service class that provides request_id logging support."""

    def __init__(self, logger_name: str = None):
        """Initialize the service with a logger.

        Args:
            logger_name: Name of the logger to use. If None, uses 'service'.
        """
        self.logger = logging.getLogger(logger_name or "service")

    def log_with_request_id(self, level: int, message: str, **kwargs):
        """Log a message with the current request_id.

        Args:
            level: Logging level (e.g., logging.INFO, logging.DEBUG)
            message: Log message
            **kwargs: Additional extra fields to include in the log
        """
        request_id = get_request_id()
        extra = {"request_id": request_id}
        extra.update(kwargs)
        self.logger.log(level, message, extra=extra)

    def info(self, message: str, **kwargs):
        """Log an info message with request_id."""
        self.log_with_request_id(logging.INFO, message, **kwargs)

    def debug(self, message: str, **kwargs):
        """Log a debug message with request_id."""
        self.log_with_request_id(logging.DEBUG, message, **kwargs)

    def warning(self, message: str, **kwargs):
        """Log a warning message with request_id."""
        self.log_with_request_id(logging.WARNING, message, **kwargs)

    def error(self, message: str, **kwargs):
        """Log an error message with request_id."""
        self.log_with_request_id(logging.ERROR, message, **kwargs)

    def exception(self, message: str, **kwargs):
        """Log an exception message with request_id."""
        self.log_with_request_id(logging.ERROR, message, **kwargs)


# Example usage:
# class UserService(BaseService):
#     def __init__(self):
#         super().__init__('user_service')
#
#     def get_user(self, user_id: int):
#         self.info(f"Fetching user {user_id}")
#         # ... user fetching logic ...
#         self.debug(f"User {user_id} fetched successfully")
