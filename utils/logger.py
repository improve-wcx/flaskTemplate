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

# Get the project root directory (parent of utils directory)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Default paths (can be overridden by config)
LOG_DIR = os.path.join(PROJECT_ROOT, "logs")
LOG_FILE = os.path.join(LOG_DIR, "app.log")
LOG_TRACE_FILE = os.path.join(LOG_DIR, "trace.log")


def configure_logger_paths(log_dir: str, app_log_file: str = "app.log", trace_log_file: str = "trace.log"):
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


class JSONListFormatter(logging.Formatter):
    """Format log records as a JSON array (list).

    Output format (list):
    [timestamp, level, pid, tid, logger_name, message, extra]

    `extra` is a dict that may include `pathname`, `lineno`, and `traceback` (when present).
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

        extra = {
            "pathname": getattr(record, "pathname", None),
            "lineno": getattr(record, "lineno", None),
        }

        # If there is exception info, include formatted traceback
        if record.exc_info:
            tb = ''.join(traceback.format_exception(*record.exc_info))
            extra["traceback"] = tb

        # Build JSON list
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
    """Create and return a logger configured with JSON-list format and a trace handler.

    - Main handlers (file + console) write structured JSON-list log entries to `app.log`.
    - A separate rotating `trace.log` receives records that contain exception info and includes the traceback.
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

    file_handler = RotatingFileHandler(LOG_FILE, maxBytes=1024 * 1024, backupCount=5, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Trace handler: only records with exception info are written here, includes full traceback
    trace_handler = RotatingFileHandler(LOG_TRACE_FILE, maxBytes=1024 * 1024, backupCount=3, encoding="utf-8")
    trace_handler.setFormatter(formatter)
    trace_handler.addFilter(ExceptionOnlyFilter())
    logger.addHandler(trace_handler)

    return logger
