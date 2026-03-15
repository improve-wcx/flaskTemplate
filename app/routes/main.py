"""
Main routes - homepage, favicon, etc.
"""
from flask import Blueprint

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def hello():
    """Home route."""
    from app import app
    logger = app.logger
    logger.debug("handling hello route")
    return "Hello, World!"


@main_bp.route('/favicon.ico')
def favicon():
    """Favicon route - returns 204 No Content."""
    from app import app
    logger = app.logger
    logger.debug("handling favicon route")
    return "", 204
