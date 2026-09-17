"""MySQL database integration.

所有数据库操作失败时抛出 :class:`MySQLDatabaseError`（而不是静默打印），
便于调用方在业务层捕获并处理。支持 ``with`` 语句自动关闭连接。
"""

from __future__ import annotations

import logging
from typing import Any, Iterable, Mapping, Sequence

import mysql.connector
from mysql.connector import Error as MySQLConnectorError

logger = logging.getLogger(__name__)


class MySQLDatabaseError(RuntimeError):
    """Raised when a MySQL operation fails."""


class MySQLDatabase:
    """A thin, exception-based wrapper around ``mysql.connector``.

    Examples:
        >>> with MySQLDatabase(config) as db:
        ...     rows = db.fetch_query("SELECT 1")
    """

    def __init__(self, config: Mapping[str, Any]) -> None:
        self.config = config
        # mysql.connector.connect() 可能返回连接池/抽象连接，具体类型随版本而变，这里按 Any 处理
        self.connection: Any = None
        self.connect()

    def __enter__(self) -> "MySQLDatabase":
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.close()

    def connect(self) -> None:
        """Establish the connection. Raises :class:`MySQLDatabaseError` on failure."""
        try:
            config = dict(self.config)
            # The connector's C extension can crash the process on Windows
            # with newer Python versions. Use the safer pure-Python
            # implementation by default while allowing callers to opt in to
            # the C extension explicitly with ``use_pure=False``.
            config.setdefault("use_pure", True)
            self.connection = mysql.connector.connect(**config)
        except MySQLConnectorError as err:
            self.connection = None
            raise MySQLDatabaseError(f"连接 MySQL 失败: {err}") from err
        logger.info("Connected to MySQL database")

    def close(self) -> None:
        """Close the connection if open. Safe to call multiple times."""
        if self.connection is not None:
            try:
                self.connection.close()
            except MySQLConnectorError as err:  # pragma: no cover - defensive
                raise MySQLDatabaseError(f"关闭 MySQL 连接失败: {err}") from err
            self.connection = None
            logger.info("MySQL connection closed")

    def _require_connection(self) -> Any:
        if self.connection is None:
            raise MySQLDatabaseError("数据库未连接，请先调用 connect()")
        return self.connection

    def _cursor(self, dictionary: bool = False):
        return self._require_connection().cursor(dictionary=dictionary)

    def execute_query(self, query: str, params: Any = None) -> None:
        """Execute a single query (with optional params) and commit.

        Accepts a list of param rows to run ``executemany``, mirroring the
        previous behavior.
        """
        cursor = self._cursor()
        try:
            if params is not None:
                if isinstance(params, list):
                    cursor.executemany(query, params)
                else:
                    cursor.execute(query, params)
            else:
                cursor.execute(query)
            self._require_connection().commit()
        except MySQLConnectorError as err:
            raise MySQLDatabaseError(f"执行查询失败: {err}") from err
        finally:
            cursor.close()

    def execute_many(self, query: str, params_list: Sequence[Sequence[Any]]) -> None:
        """Execute a batch query via ``executemany`` and commit."""
        cursor = self._cursor()
        try:
            cursor.executemany(query, params_list)
            self._require_connection().commit()
        except MySQLConnectorError as err:
            raise MySQLDatabaseError(f"批量执行失败: {err}") from err
        finally:
            cursor.close()

    def fetch_query(self, query: str, params: Any = None, dictionary: bool = False) -> list[Any]:
        """Execute a query and return all rows.

        An empty result (no rows) is returned as ``[]``; a failed query raises
        :class:`MySQLDatabaseError`.
        """
        cursor = self._cursor(dictionary=dictionary)
        try:
            if params is not None:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchall()
        except MySQLConnectorError as err:
            raise MySQLDatabaseError(f"查询失败: {err}") from err
        finally:
            cursor.close()

    def call_procedure(self, proc_name: str, params: Any = None) -> list[Mapping[str, Any]] | None:
        """Call a stored procedure and return its result sets (or ``None``)."""
        cursor = self._cursor(dictionary=True)
        try:
            if params is not None:
                args: Iterable[Any] = params if isinstance(params, (list, tuple)) else (params,)
                cursor.callproc(proc_name, args)
            else:
                cursor.callproc(proc_name)
            results: list[Mapping[str, Any]] = []
            for result in cursor.stored_results():
                results.extend(result.fetchall())
            self._require_connection().commit()
            return results or None
        except MySQLConnectorError as err:
            self._require_connection().rollback()
            raise MySQLDatabaseError(f"存储过程调用错误: {err}") from err
        finally:
            cursor.close()


__all__ = ["MySQLDatabase", "MySQLDatabaseError"]
