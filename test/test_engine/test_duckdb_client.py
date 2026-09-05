"""DuckDB 客户端测试."""

import pytest

from src.configs.config import Settings
from src.engine.duckdb_client import DuckDBClient, QueryExecutionError, QueryTimeoutError


class TestDuckDBClient:
    """DuckDB 客户端测试类."""

    @pytest.fixture
    def settings(self):
        """创建测试配置."""
        return Settings()

    @pytest.fixture
    def duckdb_client(self, settings):
        """创建 DuckDB 客户端实例."""
        return DuckDBClient(settings)

    @pytest.mark.asyncio
    async def test_execute_query(self, duckdb_client):
        """测试执行查询."""
        result = await duckdb_client.execute("SELECT 1 as test")
        assert result.row_count >= 0
        assert result.execution_time_ms >= 0

    def test_client_close(self, duckdb_client):
        """测试客户端关闭."""
        duckdb_client.close()  # 应该不抛出异常
