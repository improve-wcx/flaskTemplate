"""
Text submission routes.
Provides API endpoints for text submission and retrieval.
"""

import logging
from datetime import datetime

from flask import Blueprint, jsonify, render_template, request

from app.services.text_submission import add_submission, get_submissions
from app.api_registry import register_api

# Create blueprint
text_submission_bp = Blueprint("text_submission", __name__, url_prefix="/api/v1")

# Configure logger
logger = logging.getLogger(__name__)


@text_submission_bp.route("/submission", methods=["POST"])
@register_api(path="/api/v1/submission", method="POST", category="文本共享", description="提交文本内容")
def submit_text():
    """
    Submit new text content.

    Request body:
        content (str): The text content to submit (required, max 1MB)

    Response:
        success (bool): Whether submission was successful
        data (dict): Submitted data with id and created_at
        message (str): Status message
    """
    try:
        # Get JSON data
        try:
            data = request.get_json()
        except Exception:
            return jsonify({"success": False, "message": "Invalid request body"}), 400

        # Validate content exists
        content = data.get("content") if data else None
        if content is None:
            return jsonify({"success": False, "message": "Content is required"}), 400

        # Convert to string if needed
        content = str(content)

        # Validate content length (1MB limit)
        if len(content.encode("utf-8")) > 1024 * 1024:
            return (
                jsonify({"success": False, "message": "Content exceeds 1MB limit"}),
                400,
            )

        # Check if content is empty (only whitespace)
        if not content.strip():
            return (
                jsonify({"success": False, "message": "Content cannot be empty"}),
                400,
            )

        # Get client info
        ip_address = request.remote_addr
        user_agent = request.headers.get("User-Agent", "")

        # Add submission
        submission = add_submission(
            content=content, ip_address=ip_address, user_agent=user_agent
        )

        # Log submission
        logger.info(
            f"Text submission created: id={submission['id']}, length={len(content)}"
        )

        return (
            jsonify(
                {
                    "success": True,
                    "data": {
                        "id": submission["id"],
                        "created_at": submission["created_at"],
                    },
                    "message": "Submission successful",
                }
            ),
            201,
        )

    except Exception as e:
        logger.error(f"Error submitting text: {str(e)}", exc_info=True)
        return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500


@text_submission_bp.route("/submissions", methods=["POST"])
@register_api(path="/api/v1/submissions", method="POST", category="文本共享", description="获取文本提交列表（分页）")
def get_submissions_list():
    """
    Get paginated list of submissions with optional filters.

    Request body:
        page (int): Page number (default: 1)
        per_page (int): Items per page (default: 20, max: 100)
        start_date (str): Start date filter YYYY-MM-DD (optional)
        end_date (str): End date filter YYYY-MM-DD (optional)
        keyword (str): Search keyword (optional)
        case_sensitive (bool): Case-sensitive search (default: false)

    Response:
        success (bool): Whether request was successful
        data (dict): Paginated results
            items (list): List of submission records
            total (int): Total number of matching submissions
            page (int): Current page number
            per_page (int): Items per page
            total_pages (int): Total number of pages
    """
    try:
        # Get JSON data
        data = request.get_json() or {}

        # Parse parameters
        page = int(data.get("page", 1))
        per_page = int(data.get("per_page", 20))
        start_date = data.get("start_date")
        end_date = data.get("end_date")
        keyword = data.get("keyword")
        case_sensitive = data.get("case_sensitive", False)

        # Validate parameters
        if page < 1:
            page = 1
        if per_page < 1:
            per_page = 20
        if per_page > 100:
            per_page = 100

        # Validate date format
        if start_date:
            try:
                datetime.strptime(start_date, "%Y-%m-%d")
            except ValueError:
                return (
                    jsonify(
                        {
                            "success": False,
                            "message": "Invalid start_date format. Use YYYY-MM-DD",
                        }
                    ),
                    400,
                )

        if end_date:
            try:
                datetime.strptime(end_date, "%Y-%m-%d")
            except ValueError:
                return (
                    jsonify(
                        {
                            "success": False,
                            "message": "Invalid end_date format. Use YYYY-MM-DD",
                        }
                    ),
                    400,
                )

        # Get submissions
        result = get_submissions(
            page=page,
            per_page=per_page,
            start_date=start_date,
            end_date=end_date,
            keyword=keyword,
            case_sensitive=case_sensitive,
        )

        # Log query
        logger.info(
            f"Submissions list queried: page={page}, per_page={per_page}, "
            f"total={result['total']}, keyword={keyword}"
        )

        return jsonify({"success": True, "data": result}), 200

    except Exception as e:
        logger.error(f"Error getting submissions list: {str(e)}", exc_info=True)
        return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500


@text_submission_bp.route("/text_submission", methods=["GET"])
@register_api(path="/api/v1/text_submission", method="GET", category="文本共享", description="渲染文本共享页面")
def text_submission_page():
    """
    Renders the text submission HTML page.
    """
    return render_template("text_submission.html")
