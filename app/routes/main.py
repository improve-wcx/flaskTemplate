"""
Main routes - homepage, favicon, etc.
"""
from flask import Blueprint, current_app, g
from utils.logger import get_request_id

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def hello():
    """Home route."""
    request_id = get_request_id()
    current_app.logger.info("Handling hello route", extra={'request_id': request_id})
    return "Hello, World!"


@main_bp.route('/favicon.ico')
def favicon():
    """Favicon route - returns 204 No Content."""
    request_id = get_request_id()
    current_app.logger.info("Handling favicon route", extra={'request_id': request_id})
    return "", 204
