import os
import sqlite3

import typer

from src.data.dao import SqliteDiscountDAO, SqliteProductDAO, SqliteSalesDAO
from src.data.repository import (DAODiscountRepository, DAOProductRepository,
                                 DAOSalesRepository)
from src.simulation.simulation import simulate
from src.store.store import Store

app = typer.Typer()

DB_PATH = os.path.join(os.getcwd(), "src", "data", "store.db")


@app.command("list")
def list_command() -> None:
    conn = sqlite3.connect(DB_PATH)

    product_dao = SqliteProductDAO(conn)
    discount_dao = SqliteDiscountDAO(conn)
    sales_dao = SqliteSalesDAO(conn)

    product_repository = DAOProductRepository(product_dao)
    discount_repository = DAODiscountRepository(discount_dao)
    sales_repository = DAOSalesRepository(sales_dao)

    store = Store(product_repository, discount_repository, sales_repository)

    product_desc = store.get_product_info()
    discount_desc = store.get_discount_info()

    print("STORE INFORMATION: \n")
    print("\n".join(product_desc) + "\n")
    print("\n".join(discount_desc) + "\n")


@app.command("simulate")
def simulate_command() -> None:
    conn = sqlite3.connect(DB_PATH)

    product_dao = SqliteProductDAO(conn)
    discount_dao = SqliteDiscountDAO(conn)
    sales_dao = SqliteSalesDAO(conn)

    product_repository = DAOProductRepository(product_dao)
    discount_repository = DAODiscountRepository(discount_dao)
    sales_repository = DAOSalesRepository(sales_dao)

    store = Store(product_repository, discount_repository, sales_repository)

    simulate(store)


@app.command("report")
def report_command() -> None:
    conn = sqlite3.connect(DB_PATH)
    product_dao = SqliteProductDAO(conn)
    sales_dao = SqliteSalesDAO(conn)
    products_repository = DAOProductRepository(product_dao)
    sales_repository = DAOSalesRepository(sales_dao)

    all_products = products_repository.all_products()

    print("INFORMATION ON STORE OPERATION\n")

    print("Sales Report:")
    for product in all_products:
        try:
            sales_for_product = sum(
                [s.amount for s in sales_repository.sales_for_product(product.id)]
            )
        except ValueError:
            sales_for_product = 0
        print(f"{product.name} - {sales_for_product}")

    print()
    print("Revenue Report:")
    for method in ["cash", "card"]:
        revenue_from_method = sales_repository.revenue_from_payment_method(method)
        print(f"{method.capitalize()}: {revenue_from_method:.2f}")

    print()


if __name__ == "__main__":
    app()
