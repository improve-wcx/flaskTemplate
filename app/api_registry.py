"""
接口注册器 - 动态管理所有 Web 接口

提供接口注册、查询和元数据管理功能。
在应用启动时自动收集所有注册的路由，生成接口列表。
"""

import logging
from functools import wraps
from typing import Dict, List

logger = logging.getLogger(__name__)

# 全局接口注册表
_api_registry: Dict[str, dict] = {}


def register_api(
    path: str, method: str = "GET", category: str = "默认", description: str = ""
):
    """
    装饰器：注册接口到全局注册表

    Args:
        path: 接口路径
        method: HTTP 方法
        category: 接口分类
        description: 接口描述

    Example:
        @register_api('/api/users', 'GET', '用户管理', '获取用户列表')
        @users_bp.route('/users', methods=['GET'])
        def list_users():
            ...
    """

    def decorator(func):
        # Generate unique key
        key = f"{method}:{path}"

        # Register to global registry
        _api_registry[key] = {
            "path": path,
            "method": method,
            "category": category,
            "description": description,
            "function": func.__name__,
            "module": func.__module__,
        }

        logger.debug(f"Registered API: {method} {path} [{category}]")
        print(f"[DEBUG] API registered: {method} {path} [{category}]")

        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    return decorator


def get_all_apis() -> List[dict]:
    """
    获取所有注册的接口

    Returns:
        接口列表，每个接口包含 path, method, category, description
    """
    return list(_api_registry.values())


def get_apis_by_category() -> Dict[str, List[dict]]:
    """
    按分类获取所有接口

    Returns:
        按分类分组的接口字典
    """
    categorized = {}
    for api in _api_registry.values():
        category = api["category"]
        if category not in categorized:
            categorized[category] = []
        categorized[category].append(
            {
                "path": api["path"],
                "method": api["method"],
                "description": api["description"],
            }
        )

    logger.info(f"Retrieved APIs for {len(categorized)} categories")
    return categorized


def clear_registry():
    """清空注册表（用于测试）"""
    _api_registry.clear()
    logger.info("API registry cleared")


def get_registry_count() -> int:
    """获取注册表中的接口数量"""
    return len(_api_registry)


def auto_register_blueprint(bp, category_prefix: str = ""):
    """
    自动注册蓝图中的所有路由

    Args:
        bp: Flask Blueprint 对象
        category_prefix: 分类前缀（可选）

    Note:
        此函数会在应用启动时由 app/__init__.py 调用
    """
    # 注意：蓝图的路由在注册后才能获取
    # 这里只记录蓝图信息，实际路由在注册时收集
    logger.info(f"Blueprint registered: {bp.name} (category: {category_prefix})")
