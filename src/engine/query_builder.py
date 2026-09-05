"""SQL 查询构建器模块."""

import re
from dataclasses import dataclass
from enum import Enum
from typing import Any


class FileType(str, Enum):
    """文件类型枚举."""

    PROMPT = "prompt"
    RESPONSE = "response"
    ALL = "all"


@dataclass
class QueryOptions:
    """查询选项数据类."""

    keyword: str | None = None
    date_pattern: str = "2026-*"
    file_type: FileType = FileType.ALL
    request_ids: list[str] | None = None
    limit: int = 50
    include_content: bool = False


class QueryBuilder:
    """SQL 查询构建器.

    负责构建类型安全、参数化的 DuckDB 查询语句.
    """

    REQUEST_ID_REGEX = r"([0-9a-zA-Z_-]+)/(prompt|response)\.json"

    def __init__(self, storage_root: str) -> None:
        """初始化查询构建器.

        Args:
            storage_root: 存储根目录路径
        """
        self._storage_root = storage_root.rstrip("/")

    def build_search_query(self, options: QueryOptions) -> tuple[str, list[Any]]:
        """构建搜索查询.

        Args:
            options: 查询选项

        Returns:
            tuple[str, list]: SQL 语句和参数列表
        """
        file_glob = self._build_file_glob(options)
        select_clause = self._build_select_clause(options)
        from_clause = "FROM read_json_auto(?, filename=true, ignore_errors=true)"
        where_clause, where_params = self._build_where_clause(options)
        group_by_clause = self._build_group_by_clause(options)
        limit_clause = "LIMIT ?"

        sql_parts = [
            f"SELECT {select_clause}",
            from_clause,
            where_clause,
            group_by_clause,
            limit_clause
        ]

        sql = "\n".join(filter(None, sql_parts))
        params = [file_glob] + where_params + [options.limit]

        return sql, params

    def _build_file_glob(self, options: QueryOptions) -> str:
        """构建文件 glob 模式."""
        if options.file_type == FileType.PROMPT:
            filename = "prompt.json"
        elif options.file_type == FileType.RESPONSE:
            filename = "response.json"
        else:
            filename = "*.json"

        return f"{self._storage_root}/{options.date_pattern}/*/{filename}"

    def _build_select_clause(self, options: QueryOptions) -> str:
        """构建 SELECT 子句."""
        fields = [
            f"regexp_extract(filename, '{self.REQUEST_ID_REGEX}', 1) AS request_id",
            f"regexp_extract(filename, '{self.REQUEST_ID_REGEX}', 2) AS file_type",
            "filename AS file_path"
        ]

        if options.include_content:
            fields.append("json AS content")

        return ",\n    ".join(fields)

    def _build_where_clause(
        self,
        options: QueryOptions
    ) -> tuple[str, list[Any]]:
        """构建 WHERE 子句."""
        conditions: list[str] = []
        params: list[Any] = []

        if options.keyword:
            conditions.append("lower(CAST(json AS VARCHAR)) LIKE ?")
            params.append(f"%{options.keyword.lower()}%")

        if options.request_ids:
            placeholders = ", ".join(["?" for _ in options.request_ids])
            conditions.append(
                f"regexp_extract(filename, '{self.REQUEST_ID_REGEX}', 1) IN ({placeholders})"
            )
            params.extend(options.request_ids)

        if not conditions:
            return "", []

        return "WHERE " + " AND ".join(conditions), params

    def _build_group_by_clause(self, options: QueryOptions) -> str:
        """构建 GROUP BY 子句."""
        fields = ["request_id", "file_type", "file_path"]

        if options.include_content:
            fields.append("content")

        return "GROUP BY " + ", ".join(fields)

    def build_count_query(self, options: QueryOptions) -> tuple[str, list[Any]]:
        """构建计数查询."""
        file_glob = self._build_file_glob(options)

        sql = f"""
            SELECT COUNT(DISTINCT regexp_extract(filename, '{self.REQUEST_ID_REGEX}', 1)) AS total_count
            FROM read_json_auto(?, filename=true, ignore_errors=true)
        """

        where_clause, where_params = self._build_where_clause(options)
        if where_clause:
            sql += f" {where_clause}"

        params = [file_glob] + where_params

        return sql, params
