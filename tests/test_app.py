import os
import json
import pytest
import logging
from pathlib import Path

from app import app
import logger as project_logger


def _remove_if_exists(path):
    """Helper to remove a file if it exists."""
    try:
        os.remove(path)
    except OSError:
        pass


def _setup_isolated_logger(tmp_path, logger_name="projectTemplate"):
    """Set up logger with isolated temp files and return paths."""
    log_path = tmp_path / "app.log"
    trace_path = tmp_path / "trace.log"
    
    # Reset the global paths
    project_logger.LOG_FILE = str(log_path)
    project_logger.LOG_TRACE_FILE = str(trace_path)
    
    # Reconfigure the logger
    project_logger.setup_logger(logger_name)
    
    return log_path, trace_path


def _get_handler_by_filename(logger, target_filename):
    """Find a handler writing to the specified filename."""
    for h in logger.handlers:
        try:
            if getattr(h, "baseFilename", None) == target_filename:
                return h
        except Exception:
            continue
    return None


def _flush_all_handlers(logger):
    """Flush all handlers of a logger."""
    for h in logger.handlers:
        try:
            if hasattr(h, "flush"):
                h.flush()
        except Exception:
            pass


@pytest.fixture(autouse=True)
def reset_logger_state():
    """Reset logger state before and after each test to ensure isolation."""
    # Before test
    original_log_file = project_logger.LOG_FILE
    original_trace_file = project_logger.LOG_TRACE_FILE
    
    yield
    
    # After test: restore original paths (if needed)
    project_logger.LOG_FILE = original_log_file
    project_logger.LOG_TRACE_FILE = original_trace_file


def test_hello_route_returns_hello_world():
    """Test that the hello route returns the expected response."""
    client = app.test_client()
    resp = client.get("/")
    
    assert resp.status_code == 200
    assert b"Hello, World!" in resp.data


def test_hello_route_logs_request(caplog, tmp_path):
    """Test that the hello route logs the request properly."""
    log_path, _ = _setup_isolated_logger(tmp_path)
    logger = logging.getLogger("projectTemplate")
    
    client = app.test_client()
    resp = client.get("/")
    
    assert resp.status_code == 200
    
    # Flush handlers to ensure logs are written
    _flush_all_handlers(logger)
    
    # Verify log file contains the request log
    assert log_path.exists(), "Log file was not created"
    
    with open(log_path, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f if l.strip()]
    
    assert len(lines) >= 1, "Log file is empty"
    
    # Find the INFO entry for "GET /"
    info_entries = [
        json.loads(line) for line in lines
        if json.loads(line)[1] == "INFO" and "GET /" in json.loads(line)[5]
    ]
    
    assert len(info_entries) >= 1, "INFO log for 'GET /' not found"
    
    entry = info_entries[-1]
    assert isinstance(entry, list)
    assert len(entry) >= 7
    extra = entry[6]
    assert isinstance(extra, dict)
    assert "pathname" in extra and "lineno" in extra


def test_hello_route_logs_handling_debug(tmp_path):
    """Test that the hello route logs the debug message for handling."""
    log_path, _ = _setup_isolated_logger(tmp_path)
    logger = logging.getLogger("projectTemplate")
    
    client = app.test_client()
    resp = client.get("/")
    
    assert resp.status_code == 200
    
    # Flush handlers
    _flush_all_handlers(logger)
    
    # Read and verify the debug log entry
    with open(log_path, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f if l.strip()]
    
    # Find the DEBUG entry for "handling hello route"
    debug_entries = [
        json.loads(line) for line in lines
        if json.loads(line)[1] == "DEBUG" and "handling hello route" in json.loads(line)[5]
    ]
    
    assert len(debug_entries) >= 1, "Debug log for 'handling hello route' not found"
    
    entry = debug_entries[-1]
    assert len(entry) >= 7
    extra = entry[6]
    assert isinstance(extra, dict)
    assert "pathname" in extra and "lineno" in extra


def test_favicon_route_returns_204():
    """Test that the favicon route returns 204 No Content."""
    client = app.test_client()
    resp = client.get("/favicon.ico")
    
    assert resp.status_code == 204
    assert len(resp.data) == 0


def test_favicon_route_logs_debug(tmp_path):
    """Test that the favicon route logs a debug message."""
    log_path, _ = _setup_isolated_logger(tmp_path)
    logger = logging.getLogger("projectTemplate")
    
    client = app.test_client()
    resp = client.get("/favicon.ico")
    
    assert resp.status_code == 204
    
    # Flush handlers
    _flush_all_handlers(logger)
    
    # Verify debug log entry
    with open(log_path, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f if l.strip()]
    
    debug_entries = [
        json.loads(line) for line in lines
        if json.loads(line)[1] == "DEBUG" and "handling favicon route" in json.loads(line)[5]
    ]
    
    assert len(debug_entries) >= 1, "Debug log for 'handling favicon route' not found"


def test_error_route_returns_error_message(tmp_path):
    """Test that the error route returns the expected error message."""
    log_path, trace_path = _setup_isolated_logger(tmp_path)
    logger = logging.getLogger("projectTemplate")
    
    client = app.test_client()
    app.testing = True  # Propagate exceptions
    
    resp = client.get("/error")
    
    # The route catches the exception and returns "error"
    assert resp.status_code == 200
    assert b"error" in resp.data
    
    # Flush handlers
    _flush_all_handlers(logger)
    
    # Verify trace.log contains the traceback
    assert trace_path.exists(), "Trace log file was not created"
    
    with open(trace_path, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f if l.strip()]
    
    assert len(lines) >= 1, "Trace log is empty"
    
    # Find the entry with traceback
    trace_entries = [
        json.loads(line) for line in lines
        if json.loads(line)[6].get("traceback")
    ]
    
    assert len(trace_entries) >= 1, "No trace entry with traceback found"
    
    entry = trace_entries[-1]
    extra = entry[6]
    assert "traceback" in extra
    assert "demonstration error" in extra["traceback"]
    assert "RuntimeError" in extra["traceback"]


def test_error_route_logs_error_info(tmp_path):
    """Test that the error route logs error information."""
    log_path, _ = _setup_isolated_logger(tmp_path)
    logger = logging.getLogger("projectTemplate")
    
    client = app.test_client()
    app.testing = True
    
    resp = client.get("/error")
    assert resp.status_code == 200
    
    # Flush handlers
    _flush_all_handlers(logger)
    
    # Verify error log entry in app.log
    with open(log_path, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f if l.strip()]
    
    error_entries = [
        json.loads(line) for line in lines
        if json.loads(line)[1] == "ERROR" and "An error occurred" in json.loads(line)[5]
    ]
    
    assert len(error_entries) >= 1, "Error log entry not found"
