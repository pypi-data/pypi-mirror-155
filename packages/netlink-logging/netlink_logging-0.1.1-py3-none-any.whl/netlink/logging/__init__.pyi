import logging
from typing import Optional

# noinspection PyPep8Naming
class logger:
    level: int
    @staticmethod
    def trace(msg: str, *args: list, **kwargs: dict[str]): ...
    @staticmethod
    def debug(msg: str, *args: list, **kwargs: dict[str]): ...
    @staticmethod
    def verbose(msg: str, *args: list, **kwargs: dict[str]): ...
    @staticmethod
    def info(msg: str, *args: list, **kwargs: dict[str]): ...
    @staticmethod
    def success(msg: str, *args: list, **kwargs: dict[str]): ...
    @staticmethod
    def warning(msg: str, *args: list, **kwargs: dict[str]): ...
    @staticmethod
    def error(msg: str, *args: list, **kwargs: dict[str]): ...
    @staticmethod
    def critical(msg: str, *args: list, **kwargs: dict[str]): ...
    @staticmethod
    def log(level: int, msg: str, *args: list, **kwargs: dict[str]): ...
    @staticmethod
    def set_level(level: int): ...
    @staticmethod
    def set_file(
        filename: Optional[str] = None,
        formatter: logging.Formatter = None,
        mode: str = "a",
        max_bytes: int = 100 * 1024 * 1024,
        backup_count: int = 5,
        encoding: str = "utf-8",
        log_level: Optional[int] = None,
        disable_stderr_logger: bool = False,
    ): ...
