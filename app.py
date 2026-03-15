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


if __name__ == "__main__":
    # Development server
    app.run(host="127.0.0.1", port=5000, debug=True)
