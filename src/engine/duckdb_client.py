"""DuckDB 客户端封装模块."""

import asyncio
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from typing import Any

from loguru import logger

from src.configs.config import Settings


@dataclass
class QueryResult:
    """查询结果数据类."""

    rows: list[dict[str, Any]]
    row_count: int
    execution_time_ms: float
    query: str


class QueryTimeoutError(Exception):
    """查询超时异常."""
    pass


class QueryExecutionError(Exception):
    """查询执行异常."""
    pass


class DuckDBClient:
    """DuckDB 客户端类.

    负责管理 DuckDB 连接、执行查询和结果解析.
    使用线程池执行阻塞的 DuckDB 操作，避免阻塞事件循环.
    """

    def __init__(self, settings: Settings) -> None:
        """初始化 DuckDB 客户端.

        Args:
            settings: 应用配置
        """
        self._settings = settings
        self._thread_pool = ThreadPoolExecutor(
            max_workers=4,
            thread_name_prefix="duckdb-worker"
        )

    async def execute(
        self,
        sql: str,
        params: list[Any] | None = None,
        timeout: float | None = None
    ) -> QueryResult:
        """异步执行 SQL 查询.

        Args:
            sql: SQL 查询语句
            params: 查询参数
            timeout: 查询超时时间(秒)

        Returns:
            QueryResult: 查询结果

        Raises:
            QueryTimeoutError: 查询超时
            QueryExecutionError: 查询执行失败
        """
        timeout = timeout or 10.0

        loop = asyncio.get_event_loop()

        try:
            result = await asyncio.wait_for(
                loop.run_in_executor(
                    self._thread_pool,
                    self._execute_sync,
                    sql,
                    params or []
                ),
                timeout=timeout
            )
            return result
        except asyncio.TimeoutError:
            logger.error(f"Query timeout after {timeout}s")
            raise QueryTimeoutError(f"Query timeout after {timeout} seconds")
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            raise QueryExecutionError(f"Query execution failed: {e}") from e

    def _execute_sync(
        self,
        sql: str,
        params: list[Any]
    ) -> QueryResult:
        """同步执行 SQL 查询.

        Args:
            sql: SQL 查询语句
            params: 查询参数

        Returns:
            QueryResult: 查询结果
        """
        start_time = time.time()

        # 模板项目返回模拟结果
        logger.debug(f"Mock query executed: {sql[:100]}...")

        execution_time = (time.time() - start_time) * 1000

        return QueryResult(
            rows=[],
            row_count=0,
            execution_time_ms=execution_time,
            query=sql
        )

    def close(self) -> None:
        """关闭客户端，释放资源."""
        self._thread_pool.shutdown(wait=True)

    def __enter__(self) -> "DuckDBClient":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()
