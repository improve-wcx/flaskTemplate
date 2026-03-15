"""
API routes - for future REST API endpoints
"""
from flask import Blueprint, jsonify, current_app
from utils.logger import get_request_id

api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/health')
def health_check():
    """Health check endpoint."""
    request_id = get_request_id()
    current_app.logger.info("Health check", extra={'request_id': request_id})
    return jsonify({'status': 'healthy', 'request_id': request_id})


@api_bp.route('/version')
def version():
    """API version endpoint."""
    request_id = get_request_id()
    return jsonify({'version': '1.0.0', 'request_id': request_id})
