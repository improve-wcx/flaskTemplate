"""API routes - for future REST API endpoints"""

from flask import Blueprint, current_app, jsonify

from app.api_registry import get_apis_by_category
from utils.logger import get_request_id

api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.route("/health")
def health_check():
    """Health check endpoint."""
    request_id = get_request_id()
    current_app.logger.info("Health check", extra={"request_id": request_id})
    return jsonify({"status": "healthy", "request_id": request_id})


@api_bp.route("/version")
def version():
    """API version endpoint."""
    request_id = get_request_id()
    return jsonify({"version": "1.0.0", "request_id": request_id})


@api_bp.route("/apis")
def list_apis():
    """
    查询当前服务支持的所有 Web 接口
    返回：JSON 格式，包含所有可用接口的详细信息
    """
    request_id = get_request_id()

    # Log API list request
    current_app.logger.info("Listing all APIs", extra={"request_id": request_id})

    # 动态获取所有注册的接口
    categorized_apis = get_apis_by_category()

    # 计算总数
    total = sum(len(apis) for apis in categorized_apis.values())

    current_app.logger.info(
        f"Returning {total} APIs across {len(categorized_apis)} categories",
        extra={"request_id": request_id},
    )

    return (
        jsonify({"total": total, "apis": categorized_apis, "request_id": request_id}),
        200,
    )
