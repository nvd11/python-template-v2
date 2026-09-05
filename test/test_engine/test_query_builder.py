"""查询构建器测试."""

import pytest

from src.engine.query_builder import FileType, QueryBuilder, QueryOptions


class TestQueryBuilder:
    """查询构建器测试类."""

    def test_build_search_query_with_keyword(self):
        """测试构建带关键词的搜索查询."""
        builder = QueryBuilder("/data/payloads")
        options = QueryOptions(
            keyword="502",
            date_pattern="2026-09-04",
            file_type=FileType.ALL,
            limit=50
        )
        sql, params = builder.build_search_query(options)

        assert "LIKE ?" in sql
        assert params[0] == "/data/payloads/2026-09-04/*/*.json"
        assert params[1] == "%502%"
        assert params[2] == 50

    def test_build_search_query_with_request_ids(self):
        """测试构建带 ID 列表的搜索查询."""
        builder = QueryBuilder("/data/payloads")
        options = QueryOptions(
            request_ids=["req-001", "req-002"],
            limit=100
        )
        sql, params = builder.build_search_query(options)

        assert "IN (?, ?)" in sql
        assert "req-001" in params
        assert "req-002" in params

    def test_build_file_glob_prompt(self):
        """测试构建 prompt 文件 glob."""
        builder = QueryBuilder("/data/payloads")
        options = QueryOptions(file_type=FileType.PROMPT)
        glob = builder._build_file_glob(options)

        assert glob.endswith("prompt.json")

    def test_build_file_glob_response(self):
        """测试构建 response 文件 glob."""
        builder = QueryBuilder("/data/payloads")
        options = QueryOptions(file_type=FileType.RESPONSE)
        glob = builder._build_file_glob(options)

        assert glob.endswith("response.json")

    def test_build_count_query(self):
        """测试构建计数查询."""
        builder = QueryBuilder("/data/payloads")
        options = QueryOptions(keyword="test")
        sql, params = builder.build_count_query(options)

        assert "COUNT" in sql
        assert "DISTINCT" in sql
