"""
API routes - for future REST API endpoints
"""
from flask import Blueprint, jsonify

api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/health')
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'healthy'})


@api_bp.route('/version')
def version():
    """API version endpoint."""
    return jsonify({'version': '1.0.0'})
