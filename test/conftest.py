"""pytest fixtures 配置."""

import pytest
from fastapi.testclient import TestClient

from src.main import create_app


@pytest.fixture
def app():
    """创建测试应用实例."""
    return create_app()


@pytest.fixture
def client(app):
    """创建测试客户端."""
    return TestClient(app)
