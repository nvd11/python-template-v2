"""API 路由模块初始化."""

from fastapi import APIRouter

from . import health, search

# 创建主路由
api_router = APIRouter()

# 注册子路由
api_router.include_router(health.router, tags=["Health"])
api_router.include_router(search.router, tags=["Search"])

__all__ = ["api_router"]
