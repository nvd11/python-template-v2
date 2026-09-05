"""搜索业务逻辑服务模块."""

import re
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from loguru import logger

from src.configs.config import Settings
from src.models.requests import SearchRequest, SearchType


@dataclass
class SearchResultItem:
    """搜索结果项数据类."""

    request_id: str
    file_path: str
    file_type: str
    snippet: str | None = None
    score: float | None = None


@dataclass
class SearchResult:
    """搜索结果数据类."""

    total_count: int
    request_ids: list[str]
    items: list[SearchResultItem]
    execution_time_ms: float


class SearchExecutionError(Exception):
    """搜索执行异常."""
    pass


class SearchService:
    """搜索服务类.

    负责编排搜索业务流程.
    """

    # request_id 提取正则表达式
    REQUEST_ID_PATTERN = re.compile(
        r"([0-9a-zA-Z_-]+)/(prompt|response)\.json"
    )

    def __init__(self, settings: Settings) -> None:
        """初始化搜索服务.

        Args:
            settings: 应用配置
        """
        self._settings = settings

    async def search(
        self,
        request: SearchRequest,
        include_snippet: bool = False
    ) -> SearchResult:
        """执行搜索操作.

        Args:
            request: 搜索请求参数
            include_snippet: 是否包含匹配内容片段

        Returns:
            SearchResult: 搜索结果

        Raises:
            SearchExecutionError: 搜索执行失败
        """
        start_time = time.time()

        # 模板项目返回模拟数据
        logger.info(f"Mock search executed: query='{request.query}'")

        # 模拟搜索结果
        items = [
            SearchResultItem(
                request_id="req-001",
                file_path="/data/2026-09-04/req-001/prompt.json",
                file_type="prompt",
                snippet="...mock snippet..." if include_snippet else None,
                score=0.95
            ),
            SearchResultItem(
                request_id="req-002",
                file_path="/data/2026-09-04/req-002/response.json",
                file_type="response",
                snippet="...mock snippet..." if include_snippet else None,
                score=0.87
            ),
        ]

        # 提取去重的 request_id 列表
        seen_ids: set[str] = set()
        unique_ids: list[str] = []
        for item in items:
            if item.request_id and item.request_id not in seen_ids:
                seen_ids.add(item.request_id)
                unique_ids.append(item.request_id)

        execution_time = (time.time() - start_time) * 1000

        logger.info(
            f"Search completed: query='{request.query}', "
            f"found={len(unique_ids)} unique IDs, "
            f"time={execution_time:.2f}ms"
        )

        return SearchResult(
            total_count=len(items),
            request_ids=unique_ids,
            items=items,
            execution_time_ms=execution_time
        )

    def close(self) -> None:
        """关闭服务，释放资源."""
        pass
