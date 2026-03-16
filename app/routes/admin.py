"""
Admin routes - for future admin panel
"""

from flask import Blueprint

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/")
def admin_index():
    """Admin dashboard."""
    return "Admin Dashboard"
