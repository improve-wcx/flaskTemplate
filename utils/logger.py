"""
Logger module - supports dynamic configuration via JSON config.
"""
import logging
from logging.handlers import RotatingFileHandler
import os
import json
import time
import threading
import traceback
import uuid
from contextvars import ContextVar

# Context variable for request_id (thread-safe, async-safe)
_request_id_ctx = ContextVar('request_id', default=None)

# Get the project root directory (parent of utils directory)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Default paths (can be overridden by config)
LOG_DIR = os.path.join(PROJECT_ROOT, "logs")
LOG_FILE = os.path.join(LOG_DIR, "app.log")
LOG_TRACE_FILE = os.path.join(LOG_DIR, "trace.log")


def configure_logger_paths(
    log_dir: str,
    app_log_file: str = "app.log",
    trace_log_file: str = "trace.log"
):
    """
    Configure logger file paths.

    Args:
        log_dir: Directory for log files
        app_log_file: Name of the main log file
        trace_log_file: Name of the trace log file
    """
    global LOG_DIR, LOG_FILE, LOG_TRACE_FILE

    # Make log_dir absolute if relative
    if not os.path.isabs(log_dir):
        log_dir = os.path.join(PROJECT_ROOT, log_dir)

    LOG_DIR = log_dir
    os.makedirs(LOG_DIR, exist_ok=True)
    LOG_FILE = os.path.join(LOG_DIR, app_log_file)
    LOG_TRACE_FILE = os.path.join(LOG_DIR, trace_log_file)

    print(f"[INFO] Logger paths configured: LOG_DIR={LOG_DIR}")


class JSONListFormatter(logging.Formatter):
    """Format log records as a JSON array (list).

    Output format (list):
    [timestamp, level, pid, tid, logger_name, message, extra]

    `extra` is a dict that may include `pathname`, `lineno`, `traceback`,
    and `request_id` (when present).
    """

    def formatTime(self, record, datefmt=None):
        t = time.localtime(record.created)
        ms = int(record.msecs)
        return time.strftime("%Y-%m-%dT%H:%M:%S", t) + f".{ms:03d}"

    def format(self, record):
        timestamp = self.formatTime(record)
        level = record.levelname
        pid = getattr(record, "process", None) or os.getpid()
        tid = getattr(record, "thread", None) or threading.get_ident()
        name = record.name
        message = record.getMessage()

        # Get request_id from extra or context variable
        request_id = getattr(record, 'request_id', None) or _request_id_ctx.get()

        extra = {
            "pathname": getattr(record, "pathname", None),
            "lineno": getattr(record, "lineno", None),
        }

        # Add request_id to extra if present
        if request_id:
            extra["request_id"] = request_id

        # If there is exception info, include formatted traceback
        if record.exc_info:
            tb = ''.join(traceback.format_exception(*record.exc_info))
            extra["traceback"] = tb

        # Build JSON list payload
        payload = [timestamp, level, pid, tid, name, message, extra]
        try:
            return json.dumps(payload, ensure_ascii=False)
        except Exception:
            # Fallback to a simple text representation if JSON serialization fails
            return str(payload)


class ExceptionOnlyFilter(logging.Filter):
    """Allow only records that contain exception info."""

    def filter(self, record):
        return bool(record.exc_info)


def setup_logger(name: str = None, level: int = logging.DEBUG) -> logging.Logger:
    """
    Create and return a logger configured with JSON-list format and a trace handler.

    - Main handlers (file + console) write structured JSON-list log entries to `app.log`.
    - A separate rotating `trace.log` receives records that contain exception info
      and includes the traceback.
    """
    logger_name = name if name else __name__
    logger = logging.getLogger(logger_name)

    # Reset handlers to ensure new configuration applies if reloaded
    if logger.handlers:
        logger.handlers.clear()

    logger.setLevel(level)

    # Ensure files exist so tests or other code can open them immediately.
    open(LOG_FILE, "a", encoding="utf-8").close()
    open(LOG_TRACE_FILE, "a", encoding="utf-8").close()

    formatter = JSONListFormatter()

    # File handler
    file_handler = RotatingFileHandler(
        LOG_FILE, maxBytes=1024 * 1024, backupCount=5, encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Trace handler: only records with exception info are written here,
    # includes full traceback
    trace_handler = RotatingFileHandler(
        LOG_TRACE_FILE, maxBytes=1024 * 1024, backupCount=3, encoding="utf-8"
    )
    trace_handler.setFormatter(formatter)
    trace_handler.addFilter(ExceptionOnlyFilter())
    logger.addHandler(trace_handler)

    print(f"[INFO] Logger setup complete: name={logger_name}, "
          f"level={logging.getLevelName(level)}")

    return logger


def get_request_id():
    """Get the current request_id from context.

    Returns:
        str: The current request_id or None if not set
    """
    return _request_id_ctx.get()


def set_request_id(request_id: str = None):
    """Set the request_id in the current context.

    Args:
        request_id: The request_id to set. If None, generates a new UUID.

    Returns:
        str: The request_id that was set
    """
    if request_id is None:
        request_id = str(uuid.uuid4())
    token = _request_id_ctx.set(request_id)
    return request_id


def reset_request_id(token=None):
    """Reset the request_id to its previous value.

    Args:
        token: The token returned by set_request_id
    """
    if token is not None:
        _request_id_ctx.reset(token)
    else:
        _request_id_ctx.set(None)


class RequestIdFilter(logging.Filter):
    """Filter that adds request_id to log records if not already present."""

    def filter(self, record):
        # Get request_id from record or context
        request_id = getattr(record, 'request_id', None) or _request_id_ctx.get()
        if request_id:
            record.request_id = request_id
        return True
