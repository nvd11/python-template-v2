"""API 请求数据模型定义."""

from datetime import date
from enum import Enum
from typing import Annotated

from pydantic import BaseModel, Field, field_validator


class SearchType(str, Enum):
    """搜索类型枚举."""

    ALL = "all"
    PROMPT = "prompt"
    RESPONSE = "response"


class SearchRequest(BaseModel):
    """搜索请求参数模型."""

    query: Annotated[
        str,
        Field(
            min_length=1,
            max_length=100,
            description="搜索关键词",
            examples=["502", "timeout", "广州"]
        )
    ]

    search_date: Annotated[
        date | None,
        Field(
            alias="date",
            description="日期分区过滤 (YYYY-MM-DD)",
            examples=["2026-09-04"]
        )
    ] = None

    search_type: Annotated[
        SearchType,
        Field(description="搜索目标类型")
    ] = SearchType.ALL

    limit: Annotated[
        int,
        Field(ge=1, le=200, description="返回结果数量限制")
    ] = 50

    request_ids: Annotated[
        list[str] | None,
        Field(description="精确 request_id 列表过滤")
    ] = None

    @field_validator("query", mode="before")
    @classmethod
    def sanitize_query(cls, v: str) -> str:
        """清理搜索关键词."""
        if isinstance(v, str):
            return v.strip().lower()
        return v

    @field_validator("request_ids", mode="before")
    @classmethod
    def parse_request_ids(cls, v: str | list[str] | None) -> list[str] | None:
        """解析 request_ids 参数."""
        if v is None:
            return None
        if isinstance(v, str):
            return [rid.strip() for rid in v.split(",") if rid.strip()]
        return v

    @property
    def date_pattern(self) -> str:
        """获取日期匹配模式."""
        if self.search_date:
            return self.search_date.strftime("%Y-%m-%d")
        return "2026-*"

    @property
    def has_id_filter(self) -> bool:
        """检查是否有精确 ID 过滤."""
        return self.request_ids is not None and len(self.request_ids) > 0


class HealthCheckRequest(BaseModel):
    """健康检查请求模型 (预留扩展)."""

    detailed: bool = Field(
        default=False,
        description="是否返回详细健康信息"
    )
