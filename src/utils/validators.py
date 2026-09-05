"""自定义校验器模块."""

import re
from datetime import datetime


class DateValidator:
    """日期校验器."""

    DATE_FORMAT = "%Y-%m-%d"
    DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")

    @classmethod
    def validate_date_string(cls, v: str | None) -> str | None:
        """校验日期字符串格式."""
        if v is None:
            return None

        v = v.strip()

        if not cls.DATE_PATTERN.match(v):
            raise ValueError(f"Invalid date format: {v}. Expected: YYYY-MM-DD")

        try:
            datetime.strptime(v, cls.DATE_FORMAT)
        except ValueError as e:
            raise ValueError(f"Invalid date: {v}") from e

        return v


class KeywordValidator:
    """关键词校验器."""

    MIN_LENGTH = 1
    MAX_LENGTH = 100

    FORBIDDEN_PATTERNS = [
        re.compile(r"[;\'\"\\]"),
    ]

    @classmethod
    def validate_keyword(cls, v: str) -> str:
        """校验搜索关键词."""
        if not v:
            raise ValueError("Keyword cannot be empty")

        v = v.strip()

        if len(v) < cls.MIN_LENGTH:
            raise ValueError(f"Keyword too short (min {cls.MIN_LENGTH})")

        if len(v) > cls.MAX_LENGTH:
            raise ValueError(f"Keyword too long (max {cls.MAX_LENGTH})")

        for pattern in cls.FORBIDDEN_PATTERNS:
            if pattern.search(v):
                raise ValueError("Keyword contains forbidden characters")

        return v


class RequestIDValidator:
    """Request ID 校验器."""

    PATTERN = re.compile(r"^[0-9a-zA-Z_-]+$")
    MAX_IDS = 100

    @classmethod
    def validate_request_ids(
        cls,
        v: str | list[str] | None
    ) -> list[str] | None:
        """校验 request_id 列表."""
        if v is None:
            return None

        if isinstance(v, str):
            ids = [rid.strip() for rid in v.split(",") if rid.strip()]
        else:
            ids = v

        if len(ids) > cls.MAX_IDS:
            raise ValueError(f"Too many request IDs (max {cls.MAX_IDS})")

        for rid in ids:
            if not cls.PATTERN.match(rid):
                raise ValueError(f"Invalid request ID format: {rid}")

        return ids
