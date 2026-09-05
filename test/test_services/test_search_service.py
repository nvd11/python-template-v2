"""搜索服务测试."""

import pytest

from src.configs.config import Settings
from src.models.requests import SearchRequest, SearchType
from src.services.search_service import SearchService


class TestSearchService:
    """搜索服务测试类."""

    @pytest.fixture
    def settings(self):
        """创建测试配置."""
        return Settings(
            app_name="TestApp",
            app_version="1.0.0",
            debug=True
        )

    @pytest.fixture
    def search_service(self, settings):
        """创建搜索服务实例."""
        return SearchService(settings)

    @pytest.mark.asyncio
    async def test_search_basic(self, search_service):
        """测试基本搜索功能."""
        request = SearchRequest(
            query="test",
            search_type=SearchType.ALL,
            limit=10
        )
        result = await search_service.search(request)

        assert result.total_count >= 0
        assert isinstance(result.request_ids, list)
        assert result.execution_time_ms >= 0

    @pytest.mark.asyncio
    async def test_search_with_snippet(self, search_service):
        """测试带片段的搜索."""
        request = SearchRequest(
            query="test",
            search_type=SearchType.ALL,
            limit=10
        )
        result = await search_service.search(request, include_snippet=True)

        assert result.total_count >= 0
        for item in result.items:
            if item.snippet:
                assert isinstance(item.snippet, str)

    def test_search_service_close(self, search_service):
        """测试服务关闭."""
        search_service.close()  # 应该不抛出异常
