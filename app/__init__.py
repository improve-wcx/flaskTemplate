#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import os

from flask import Flask

# from app.routes.admin import admin_bp  # Uncomment when needed
# Log application ready
from app.api_registry import get_registry_count
from app.routes.api import api_bp
from app.routes.demo_protobuf import demo_protobuf_bp

# 注册蓝图
from app.routes.main import main_bp
from app.routes.rel_map import rel_map_bp
from app.routes.static_resources import static_bp
from app.routes.text_submission import text_submission_bp
from config import get_config
from utils.logger import configure_logger_paths, setup_logger

# 定义蓝图分类映射
blueprint_categories = {
    "main": "系统",
    "api": "系统",
    "demo_protobuf": "Protobuf 演示",
    "static_bp": "静态资源",
    "rel_map": "关系图",
    "admin": "管理",
    "text_submission": "文本共享",
}


def create_app(config_name=None):
    """
    Application factory function.

    Args:
        config_name: Configuration name ('development', 'testing', 'production')

    Returns:
        Configured Flask application instance
    """
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "development")

    # Log application initialization
    logger = logging.getLogger(__name__)
    logger.info(f"Initializing Flask application with config: {config_name}")

    # Load configuration from JSON
    config = get_config(config_name)
    logger.info("Configuration loaded successfully")

    # Configure logger paths BEFORE creating the logger
    logging_config = config.get("logging", {})
    log_dir = logging_config.get("log_dir", "logs")
    app_log_file = logging_config.get("app_log_file", "app.log")
    trace_log_file = logging_config.get("trace_log_file", "trace.log")

    configure_logger_paths(
        log_dir=log_dir, app_log_file=app_log_file, trace_log_file=trace_log_file
    )
    logger.info(f"Logger paths configured: log_dir={log_dir}")

    # Setup logger
    logger = setup_logger(
        name="app", level=getattr(logging, logging_config.get("level", "DEBUG"))
    )

    # Create Flask app
    app = Flask(__name__)
    logger.info("Flask app instance created")

    # Apply configuration
    app_config = config.get("app", {})
    app.debug = app_config.get("debug", False)
    app.testing = app_config.get("testing", False)
    logger.info(f"Configuration applied: debug={app.debug}, testing={app.testing}")

    # Security settings
    security = config.get("security", {})
    app.secret_key = security.get("secret_key", "dev-secret-key")

    # JSON configuration - support Chinese characters
    app.json.ensure_ascii = False
    logger.info("JSON encoding configured for Chinese support")

    # 定义路由收集函数
    def _collect_routes(blueprint, category: str):
        """收集蓝图中的所有路由"""
        from app.api_registry import _api_registry

        for rule in app.url_map.iter_rules():
            # 只收集当前蓝图的路由
            if not rule.endpoint.startswith(blueprint.name + "."):
                continue

            # 排除 Flask 内置的静态文件端点（仅排除确切的 'static'）
            if rule.endpoint == "static":
                continue

            # 收集路由
            full_path = rule.rule.rstrip("/") if rule.rule != "/" else rule.rule

            for method in rule.methods:
                if method in ["HEAD", "OPTIONS"]:
                    continue

                key = f"{method}:{full_path}"

                if key not in _api_registry:
                    _api_registry[key] = {
                        "path": full_path,
                        "method": method,
                        "category": category,
                        "description": "",
                        "function": rule.endpoint,
                        "module": blueprint.name,
                    }

        count = len(
            [
                k
                for k in _api_registry
                if _api_registry[k].get("module") == blueprint.name
            ]
        )
        app.logger.info(
            f"Collected {count} routes from blueprint {blueprint.name} "
            f"(category: {category})"
        )

    logger.info("Registering blueprints...")
    app.register_blueprint(main_bp)
    logger.info("Registered blueprint: main_bp")
    app.register_blueprint(api_bp)
    logger.info("Registered blueprint: api_bp")
    app.register_blueprint(demo_protobuf_bp)
    logger.info("Registered blueprint: demo_protobuf_bp")
    app.register_blueprint(static_bp)
    logger.info("Registered blueprint: static_bp")
    app.register_blueprint(rel_map_bp)
    logger.info("Registered blueprint: rel_map_bp")
    app.register_blueprint(text_submission_bp)
    logger.info("Registered blueprint: text_submission_bp")
    # app.register_blueprint(admin_bp)  # Uncomment when needed

    # Auto-collect blueprint routes
    logger.info("Collecting routes from blueprints...")
    _collect_routes(main_bp, blueprint_categories["main"])
    _collect_routes(api_bp, blueprint_categories["api"])
    _collect_routes(demo_protobuf_bp, blueprint_categories["demo_protobuf"])
    _collect_routes(static_bp, blueprint_categories["static_bp"])
    _collect_routes(rel_map_bp, blueprint_categories["rel_map"])
    _collect_routes(text_submission_bp, blueprint_categories["text_submission"])
    # _collect_routes(admin_bp, blueprint_categories['admin'])  # Uncomment when needed

    logger.info("Route collection completed")

    # Before request hook
    @app.before_request
    def before_request():
        """Set up request_id for tracing and log the request."""
        from flask import g, request

        from utils.logger import set_request_id

        # Generate and set request_id for this request
        request_id = set_request_id()

        # Store in Flask's g object for access in routes
        g.request_id = request_id

        # Log the incoming request with request_id
        app.logger.info(
            "%s %s", request.method, request.path, extra={"request_id": request_id}
        )

    # After request hook
    @app.after_request
    def after_request(response):
        """Log the response with request_id."""
        from flask import g, request

        from utils.logger import get_request_id

        # Get request_id from g or context
        request_id = getattr(g, "request_id", None) or get_request_id()

        # Log response with request_id
        app.logger.info(
            "%s %s %d %s",
            request.method,
            request.path,
            response.status_code,
            request.remote_addr,
            extra={"request_id": request_id},
        )

        return response

    logger.info("Flask application initialized successfully")
    logger.info(f"Total APIs registered: {get_registry_count()}")

    return app
