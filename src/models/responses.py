"""API 响应数据模型定义."""

from datetime import datetime
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class BaseResponse(BaseModel, Generic[T]):
    """基础响应模型."""

    code: int = Field(default=0, description="业务状态码")
    message: str = Field(default="success", description="响应消息")
    data: T | None = Field(default=None, description="响应数据")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class SearchResultItem(BaseModel):
    """单个搜索结果项."""

    request_id: str = Field(description="请求唯一标识")
    file_path: str = Field(description="匹配文件路径")
    file_type: str = Field(description="文件类型")
    matched_snippet: str | None = Field(default=None, description="匹配内容片段")
    relevance_score: float | None = Field(default=None, ge=0.0, le=1.0)


class SearchResponseData(BaseModel):
    """搜索响应数据."""

    query: str = Field(description="原始搜索关键词")
    date_pattern: str = Field(description="使用的日期匹配模式")
    search_type: str = Field(description="搜索类型")
    total_matches: int = Field(description="总匹配数量")
    returned_count: int = Field(description="实际返回数量")
    search_time_ms: float = Field(description="搜索耗时 (毫秒)")
    request_ids: list[str] = Field(description="匹配的 request_id 列表")
    results: list[SearchResultItem] | None = Field(default=None)


class HealthResponseData(BaseModel):
    """健康检查响应数据."""

    status: str = Field(description="服务状态")
    service: str = Field(description="服务名称")
    version: str = Field(description="服务版本")
    storage_available: bool = Field(description="存储是否可用")
    storage_path: str | None = Field(default=None)
    uptime_seconds: float | None = Field(default=None)


# 类型别名
SearchResponse = BaseResponse[SearchResponseData]
HealthResponse = BaseResponse[HealthResponseData]
