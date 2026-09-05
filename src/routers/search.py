"""搜索路由模块."""

import time
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from loguru import logger

from src.configs.config import Settings, get_settings
from src.models.requests import SearchRequest, SearchType
from src.models.responses import SearchResponse, SearchResponseData, SearchResultItem
from src.services.search_service import SearchExecutionError, SearchService

router = APIRouter()


def get_settings_dep() -> Settings:
    """获取配置依赖."""
    return get_settings()


def get_search_service(
    settings: Annotated[Settings, Depends(get_settings_dep)]
) -> SearchService:
    """获取搜索服务依赖."""
    return SearchService(settings)


@router.get(
    "/search",
    response_model=SearchResponse,
    summary="全文搜索",
    description="在本地存储的 JSON 报文中执行全文关键词搜索"
)
async def search_payloads(
    settings: Annotated[Settings, Depends(get_settings_dep)],
    search_service: Annotated[SearchService, Depends(get_search_service)],
    q: Annotated[
        str,
        Query(
            min_length=1,
            max_length=100,
            description="搜索关键词",
            examples=["502", "timeout"]
        )
    ],
    date: Annotated[
        str | None,
        Query(
            description="日期分区 (YYYY-MM-DD)",
            pattern=r"^\d{4}-\d{2}-\d{2}$",
            examples=["2026-09-04"]
        )
    ] = None,
    type: Annotated[
        SearchType,
        Query(description="搜索目标类型")
    ] = SearchType.ALL,
    limit: Annotated[
        int,
        Query(ge=1, le=200, description="返回结果数量限制")
    ] = 50,
    request_ids: Annotated[
        str | None,
        Query(
            description="精确 request_id 列表 (逗号分隔)",
            examples=["req-001,req-002"]
        )
    ] = None,
    include_snippet: Annotated[
        bool,
        Query(description="是否包含匹配内容片段")
    ] = False
) -> SearchResponse:
    """执行全文搜索.

    支持两种模式:
    1. 关键词搜索: 提供 q 参数，扫描指定日期范围内的所有报文
    2. 精确 ID 查询: 提供 request_ids 参数，仅查询指定 ID 的报文
    """
    start_time = time.time()

    # 构建请求模型
    try:
        search_request = SearchRequest(
            query=q,
            search_date=date,
            search_type=type,
            limit=min(limit, 200),
            request_ids=request_ids
        )
    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "error_code": "VALIDATION_ERROR",
                "error_message": str(e)
            }
        )

    # 执行搜索
    try:
        result = await search_service.search(
            request=search_request,
            include_snippet=include_snippet
        )
    except SearchExecutionError as e:
        logger.error(f"Search execution failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error_code": "SEARCH_EXECUTION_ERROR",
                "error_message": str(e)
            }
        )

    # 计算耗时
    elapsed_ms = round((time.time() - start_time) * 1000, 2)

    # 构建响应
    response_data = SearchResponseData(
        query=search_request.query,
        date_pattern=search_request.date_pattern,
        search_type=search_request.search_type.value,
        total_matches=result.total_count,
        returned_count=len(result.request_ids),
        search_time_ms=elapsed_ms,
        request_ids=result.request_ids,
        results=[
            SearchResultItem(
                request_id=item.request_id,
                file_path=item.file_path,
                file_type=item.file_type,
                matched_snippet=item.snippet if include_snippet else None,
                relevance_score=item.score
            )
            for item in result.items
        ] if include_snippet else None
    )

    logger.info(
        f"Search completed: q='{q}', date={date}, "
        f"found={len(result.request_ids)}, time={elapsed_ms}ms"
    )

    return SearchResponse(data=response_data)


@router.get(
    "/search/ids",
    response_model=SearchResponse,
    summary="精确 ID 搜索",
    description="根据 request_id 列表精确查询报文内容"
)
async def search_by_ids(
    settings: Annotated[Settings, Depends(get_settings_dep)],
    search_service: Annotated[SearchService, Depends(get_search_service)],
    request_ids: Annotated[
        str,
        Query(
            description="request_id 列表 (逗号分隔)",
            examples=["req-001,req-002,req-003"]
        )
    ],
    limit: Annotated[
        int,
        Query(ge=1, le=200, description="返回结果数量限制")
    ] = 50
) -> SearchResponse:
    """根据精确 ID 列表搜索."""
    # 复用主搜索接口
    return await search_payloads(
        settings=settings,
        search_service=search_service,
        q="",
        date=None,
        type=SearchType.ALL,
        limit=limit,
        request_ids=request_ids,
        include_snippet=True
    )
