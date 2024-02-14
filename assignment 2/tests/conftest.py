import os
import sqlite3
from sqlite3 import Connection

import pytest

from src.data.dao import (DiscountDAO, ProductDAO, SalesDAO, SqliteDiscountDAO,
                          SqliteProductDAO, SqliteSalesDAO)
from src.data.objects import Discount, Product, SoldItem

SOURCE_DB_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "src", "data", "store.db"
)


@pytest.fixture
def connection() -> Connection:
    source_conn = sqlite3.connect(SOURCE_DB_PATH)
    source_cur = source_conn.cursor()
    source_cur.execute("SELECT sql FROM sqlite_master WHERE type='table';")
    schema_sql = ";\n".join([row[0] for row in source_cur.fetchall()])

    memory_conn = sqlite3.connect(":memory:")
    memory_cur = memory_conn.cursor()
    memory_cur.executescript(schema_sql)

    memory_conn.commit()
    source_conn.close()

    yield memory_conn
    memory_conn.close()


@pytest.fixture
def product_dao(connection: Connection) -> ProductDAO:
    product_dao = SqliteProductDAO(connection)
    product_dao.add_product(Product(0, "p1", 1))
    product_dao.add_product(Product(0, "p2", 3))
    product_dao.add_product(Product(0, "p3", 5))

    return product_dao


@pytest.fixture
def discount_dao(connection: Connection) -> DiscountDAO:
    discount_dao = SqliteDiscountDAO(connection)

    discount_dao.add_discount(Discount(0, 1, 15, 1))
    discount_dao.add_discount(Discount(0, 1, 20, 3))
    discount_dao.add_discount(Discount(0, 1, 25, 5))

    discount_dao.add_discount(Discount(0, 2, 10, 4))

    return discount_dao


@pytest.fixture
def sales_dao(connection: Connection) -> SalesDAO:
    sales_dao = SqliteSalesDAO(connection)

    sales_dao.add_sale(SoldItem(1, 3, 1, 3, "cash"))
    sales_dao.add_sale(SoldItem(1, 1, 3, 3, "cash"))
    sales_dao.add_sale(SoldItem(1, 1, 1, 1, "cash"))
    sales_dao.add_sale(SoldItem(3, 1, 5, 5, "cash"))
    sales_dao.add_sale(SoldItem(2, 3, 3, 9, "card"))
    sales_dao.add_sale(SoldItem(2, 2, 3, 6, "card"))
    sales_dao.add_sale(SoldItem(2, 1, 3, 3, "card"))
    sales_dao.add_sale(SoldItem(3, 5, 5, 25, "card"))

    return sales_dao
