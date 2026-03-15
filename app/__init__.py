""" Flask application factory.
Usage: from app import app
app.run()
Or with run.py: python run.py
"""
import os
from flask import Flask
from utils.logger import setup_logger
from config import get_config

def create_app(config_name=None):
    """ Application factory function.
    Args:
        config_name: Configuration name ('development', 'testing', 'production')
    Returns:
        Configured Flask application instance
    """
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    # Load configuration from JSON
    config = get_config(config_name)
    
    # Create Flask app
    app = Flask(__name__)
    
    # Apply configuration
    app_config = config.get('app', {})
    app.debug = app_config.get('debug', False)
    app.testing = app_config.get('testing', False)
    
    # Security settings
    security = config.get('security', {})
    app.secret_key = security.get('secret_key', 'dev-secret-key')
    
    # JSON 配置 - 支持中文显示
    app.json.ensure_ascii = False
    
    # 定义路由收集函数
    def _collect_routes(blueprint, category: str):
        """收集蓝图中的所有路由"""
        from app.api_registry import _api_registry
        
        for rule in app.url_map.iter_rules():
            if not rule.endpoint.startswith(blueprint.name + '.'):
                continue
            if rule.endpoint == 'static' or rule.endpoint.startswith(blueprint.name + '.static'):
                continue
            
            full_path = rule.rule.rstrip('/') if rule.rule != '/' else rule.rule
            
            for method in rule.methods:
                if method in ['HEAD', 'OPTIONS']:
                    continue
                
                key = f"{method}:{full_path}"
                if key not in _api_registry:
                    _api_registry[key] = {
                        'path': full_path,
                        'method': method,
                        'category': category,
                        'description': '',
                        'function': rule.endpoint,
                        'module': blueprint.name
                    }
        
        count = len([k for k in _api_registry if _api_registry[k].get('module') == blueprint.name])
        app.logger.info(f"Collected {count} routes from blueprint {blueprint.name} (category: {category})")
    
    # 注册蓝图
    from app.routes.main import main_bp
    from app.routes.api import api_bp
    from app.routes.demo_protobuf import demo_protobuf_bp
    # from app.routes.admin import admin_bp  # Uncomment when needed
    
    # 定义蓝图分类映射
    blueprint_categories = {
        'main': '系统',
        'api': '系统',
        'demo_protobuf': 'Protobuf 演示',
        'admin': '管理'
    }
    
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(demo_protobuf_bp)
    # app.register_blueprint(admin_bp)  # Uncomment when needed
    
    # 自动收集蓝图路由
    _collect_routes(main_bp, blueprint_categories['main'])
    _collect_routes(api_bp, blueprint_categories['api'])
    _collect_routes(demo_protobuf_bp, blueprint_categories['demo_protobuf'])
    # _collect_routes(admin_bp, blueprint_categories['admin'])  # Uncomment when needed
    
    # Before request hook
    @app.before_request
    def before_request():
        """Set up request_id for tracing and log the request."""
        from flask import request, g
        from utils.logger import set_request_id
        
        # Generate and set request_id for this request
        request_id = set_request_id()
        
        # Store in Flask's g object for access in routes
        g.request_id = request_id
        
        # Log the incoming request with request_id
        app.logger.info("%s %s", request.method, request.path, extra={'request_id': request_id})
    
    # After request hook
    @app.after_request
    def after_request(response):
        """Log the response with request_id."""
        from flask import request, g
        from utils.logger import get_request_id
        
        # Get request_id from g or context
        request_id = getattr(g, 'request_id', None) or get_request_id()
        
        # Log response with request_id
        app.logger.info(
            "%s %s %d %s",
            request.method,
            request.path,
            response.status_code,
            request.remote_addr,
            extra={'request_id': request_id}
        )
        
        return response
    
    # Return the app instance
    return app
