"""健康检查路由测试."""

import pytest


class TestHealthRouter:
    """健康检查路由测试类."""

    def test_health_check(self, client):
        """测试健康检查端点."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert data["data"]["status"] in ["ok", "error"]
        assert data["data"]["service"] == "PythonTemplateV2"

    def test_health_check_detailed(self, client):
        """测试详细健康检查端点."""
        response = client.get("/health?detailed=true")
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert "uptime_seconds" in data["data"]

    def test_readiness_check(self, client):
        """测试就绪检查端点."""
        response = client.get("/ready")
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0

    def test_liveness_check(self, client):
        """测试存活检查端点."""
        response = client.get("/live")
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert data["data"]["status"] == "ok"
