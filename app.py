from flask import Flask, request
from logger import setup_logger

app = Flask(__name__)
logger = setup_logger("projectTemplate")


@app.before_request
def log_request():
    logger.info("%s %s", request.method, request.path)


@app.route("/")
def hello():
    logger.debug("handling hello route")
    return "Hello, World!"


@app.route("/favicon.ico")
def favicon():
    logger.debug("handling favicon route")
    return "", 204

@app.route("/error")
def error():
    # Route to demonstrate exception logging; will raise and be captured by Flask
    try:
        logger.error("An error occurred")
        raise RuntimeError("demonstration error")
    except Exception:
        logger.exception("An error occurred in /error")
    return "error"


if __name__ == "__main__":
    # Development server
    app.run(host="127.0.0.1", port=5000, debug=True)
