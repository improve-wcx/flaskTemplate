import os
import json
import pytest
import logging

from app import app
import logger as project_logger


def _remove_if_exists(path):
    try:
        os.remove(path)
    except OSError:
        pass


def test_hello_logs(caplog, tmp_path):
    # Do not delete user logs. Use isolated temp log files and reconfigure the logger.
    log_path = tmp_path / "app.log"
    trace_path = tmp_path / "trace.log"

    # Point logger to temp files and reconfigure handlers
    project_logger.LOG_FILE = str(log_path)
    project_logger.LOG_TRACE_FILE = str(trace_path)
    project_logger.setup_logger("projectTemplate")

    caplog.clear()
    client = app.test_client()
    with caplog.at_level("INFO"):
        resp = client.get("/")

    assert resp.status_code == 200
    assert b"Hello, World!" in resp.data

    # Ensure the request was logged to the logger (caplog records capture the message)
    assert any("GET /" in rec.getMessage() for rec in caplog.records)

    # Ensure an entry was written to app.log in JSON-list format
    # Flush handlers to force file writes
    logger = logging.getLogger("projectTemplate")
    handler_file = None
    for h in logger.handlers:
        try:
            if hasattr(h, "flush"):
                h.flush()
        except Exception:
            pass
        # RotatingFileHandler exposes baseFilename
        if getattr(h, "baseFilename", None) == str(log_path):
            handler_file = h

    assert handler_file is not None, f"no handler writing to {log_path} found"
    with open(handler_file.baseFilename, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f if l.strip()]

    assert lines, "app.log is empty"
    last = lines[-1]
    data = json.loads(last)
    # [timestamp, level, pid, tid, name, message, extra]
    assert isinstance(data, list)
    assert len(data) >= 7
    assert data[1] == "DEBUG"
    assert data[5] == "handling hello route"
    extra = data[6]
    assert isinstance(extra, dict)
    assert "pathname" in extra and "lineno" in extra


def test_error_writes_trace_log(tmp_path):
    # Use isolated temp trace file and reconfigure logger
    log_path = tmp_path / "app.log"
    trace_path = tmp_path / "trace.log"
    project_logger.LOG_FILE = str(log_path)
    project_logger.LOG_TRACE_FILE = str(trace_path)
    project_logger.setup_logger("projectTemplate")

    client = app.test_client()
    # Propagate exceptions so the test can catch them
    app.testing = True

    # with pytest.raises(RuntimeError):
    #     client.get("/error")

    client.get("/error")

    # After the request, trace.log should contain an entry with a traceback
    logger = logging.getLogger("projectTemplate")
    trace_handler = None
    for h in logger.handlers:
        try:
            if getattr(h, "baseFilename", None) == str(trace_path):
                trace_handler = h
                h.flush()
                break
        except Exception:
            continue

    assert trace_handler is not None, "no trace handler writing to trace.log found"
    with open(trace_handler.baseFilename, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f if l.strip()]

    assert lines, "trace.log is empty"
    last = lines[-1]
    data = json.loads(last)
    # extra should include a traceback string containing the error message
    extra = data[6]
    assert "traceback" in extra
    assert "demonstration error" in extra["traceback"]
