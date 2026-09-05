"""搜索路由测试."""

import pytest


class TestSearchRouter:
    """搜索路由测试类."""

    def test_search_endpoint_success(self, client):
        """测试搜索端点成功."""
        response = client.get(
            "/search",
            params={"q": "test", "limit": 10}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert "request_ids" in data["data"]
        assert "search_time_ms" in data["data"]

    def test_search_endpoint_with_date(self, client):
        """测试带日期的搜索."""
        response = client.get(
            "/search",
            params={"q": "test", "date": "2026-09-04", "limit": 10}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert data["data"]["date_pattern"] == "2026-09-04"

    def test_search_endpoint_with_type(self, client):
        """测试带类型的搜索."""
        response = client.get(
            "/search",
            params={"q": "test", "type": "prompt", "limit": 10}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert data["data"]["search_type"] == "prompt"

    def test_search_endpoint_validation_error(self, client):
        """测试搜索参数校验错误."""
        response = client.get(
            "/search",
            params={"q": "", "limit": 10}  # 空关键词
        )
        assert response.status_code == 422

    def test_search_by_ids_endpoint(self, client):
        """测试精确 ID 搜索端点."""
        response = client.get(
            "/search/ids",
            params={"request_ids": "req-001,req-002", "limit": 10}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
