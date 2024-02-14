import os
import sqlite3
from sqlite3 import Connection

import pytest

from src.persistence.dao.product_dao import ProductDAO, SqliteProductDAO
from src.persistence.dao.receipt_dao import ReceiptDAO, SqliteReceiptDAO
from src.persistence.dao.sales_dao import SalesDAO, SqliteSalesDAO
from src.persistence.dao.unit_dao import SqliteUnitDAO, UnitDAO

TABLES_SCRIPT_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "src", "db", "create_tables.sql"
)


@pytest.fixture
def in_memory_db() -> Connection:  # type: ignore
    connection = sqlite3.connect(":memory:")

    with open(TABLES_SCRIPT_PATH, "r") as sql_file:
        create_tables_sql = sql_file.read()
        connection.executescript(create_tables_sql)

    yield connection

    connection.close()


@pytest.fixture
def unit_dao(in_memory_db: Connection) -> UnitDAO:
    dao = SqliteUnitDAO(in_memory_db)

    return dao


@pytest.fixture
def product_dao(in_memory_db: Connection) -> ProductDAO:
    dao = SqliteProductDAO(in_memory_db)

    return dao


@pytest.fixture
def receipt_dao(in_memory_db: Connection) -> ReceiptDAO:
    dao = SqliteReceiptDAO(in_memory_db)

    return dao


@pytest.fixture
def sales_dao(in_memory_db: Connection) -> SalesDAO:
    dao = SqliteSalesDAO(in_memory_db)

    return dao
