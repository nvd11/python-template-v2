"""路径处理工具模块."""

import re
from pathlib import Path
from typing import Iterator


class PathUtils:
    """路径处理工具类."""

    DATE_DIR_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")
    REQUEST_ID_PATTERN = re.compile(r"^[0-9a-zA-Z_-]+$")

    @staticmethod
    def is_valid_date_dir(dirname: str) -> bool:
        """检查是否为有效的日期目录名."""
        return bool(PathUtils.DATE_DIR_PATTERN.match(dirname))

    @staticmethod
    def is_valid_request_id(request_id: str) -> bool:
        """检查是否为有效的 request_id."""
        return bool(PathUtils.REQUEST_ID_PATTERN.match(request_id))

    @staticmethod
    def extract_request_id(file_path: str | Path) -> str | None:
        """从文件路径提取 request_id."""
        path = Path(file_path)
        parent = path.parent.name
        if PathUtils.is_valid_request_id(parent):
            return parent
        return None

    @staticmethod
    def extract_file_type(file_path: str | Path) -> str | None:
        """从文件路径提取文件类型."""
        path = Path(file_path)
        filename = path.name.lower()

        if filename == "prompt.json":
            return "prompt"
        elif filename == "response.json":
            return "response"

        return None

    @staticmethod
    def iter_payload_files(
        root: Path,
        date_pattern: str = "*",
        file_type: str = "*.json"
    ) -> Iterator[Path]:
        """迭代遍历报文文件."""
        for date_dir in root.glob(date_pattern):
            if not date_dir.is_dir():
                continue
            if not PathUtils.is_valid_date_dir(date_dir.name):
                continue

            for request_dir in date_dir.iterdir():
                if not request_dir.is_dir():
                    continue
                if not PathUtils.is_valid_request_id(request_dir.name):
                    continue

                for file_path in request_dir.glob(file_type):
                    if file_path.is_file():
                        yield file_path
