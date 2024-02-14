from dataclasses import dataclass
from sqlite3 import Connection
from typing import List, Protocol

from src.data.objects import Discount, Product, Sale, SoldItem


class ProductDAO(Protocol):
    def add_product(self, product: Product) -> None:
        raise NotImplementedError

    def get_all_products(self) -> List[Product]:
        raise NotImplementedError

    def get_by_id(self, product_id: int) -> Product:
        raise NotImplementedError

    def get_by_name(self, product_name: str) -> Product:
        raise NotImplementedError


class DiscountDAO(Protocol):
    def add_discount(self, discount: Discount) -> None:
        raise NotImplementedError

    def get_all_discounts(self) -> List[Discount]:
        raise NotImplementedError

    def get_by_id(self, discount_id: int) -> Discount:
        raise NotImplementedError

    def get_discounts_for_product(self, product_id: int) -> List[Discount]:
        raise NotImplementedError


class SalesDAO(Protocol):
    def add_sale(self, item: SoldItem) -> None:
        raise NotImplementedError

    def get_all_sales(self) -> List[Sale]:
        raise NotImplementedError

    def get_sales_for_product(self, product_id: int) -> List[Sale]:
        raise NotImplementedError

    def get_total_for_payment_method(self, payment_method: str) -> float:
        raise NotImplementedError


@dataclass
class SqliteProductDAO:
    connection: Connection

    def add_product(self, product: Product) -> None:
        cur = self.connection.cursor()
        cur.execute(
            "INSERT INTO products (name, price) VALUES (?, ?)",
            (product.name, product.price),
        )
        cur.close()
        self.connection.commit()

    def get_all_products(self) -> List[Product]:
        cur = self.connection.cursor()
        cur.execute("SELECT * FROM products")
        rows = cur.fetchall()
        cur.close()

        if rows:
            return [Product(*row) for row in rows]
        else:
            raise ValueError("No products in the database")

    def get_by_id(self, product_id: int) -> Product:
        cur = self.connection.cursor()
        cur.execute("SELECT * FROM products WHERE id=?", (product_id,))
        row = cur.fetchone()
        cur.close()

        if row:
            return Product(*row)
        else:
            raise ValueError(f"Product with id {product_id} not found")

    def get_by_name(self, product_name: str) -> Product:
        cur = self.connection.cursor()
        cur.execute("SELECT * FROM products WHERE name=?", (product_name,))
        row = cur.fetchone()
        cur.close()

        if row:
            return Product(*row)
        else:
            raise ValueError(f"Product with name {product_name} not found")


@dataclass
class SqliteDiscountDAO:
    connection: Connection

    def add_discount(self, discount: Discount) -> None:
        cur = self.connection.cursor()
        cur.execute(
            "INSERT INTO discounts (product_id, discount_pct, batch_size)"
            " VALUES (?, ?, ?)",
            (discount.product_id, discount.discount_pct, discount.batch_size),
        )
        cur.close()
        self.connection.commit()

    def get_all_discounts(self) -> List[Discount]:
        cur = self.connection.cursor()
        cur.execute("SELECT * FROM discounts")
        rows = cur.fetchall()
        cur.close()

        if rows:
            return [Discount(*row) for row in rows]
        else:
            raise ValueError("No discounts in the database")

    def get_by_id(self, discount_id: int) -> Discount:
        cur = self.connection.cursor()
        cur.execute("SELECT * FROM discounts WHERE id=?", (discount_id,))
        row = cur.fetchone()
        cur.close()

        if row:
            return Discount(*row)
        else:
            raise ValueError(f"Discount with id {discount_id} not found")

    def get_discounts_for_product(self, product_id: int) -> List[Discount]:
        cur = self.connection.cursor()
        cur.execute("SELECT * FROM discounts " "WHERE product_id=?", (product_id,))
        rows = cur.fetchall()
        cur.close()

        if rows:
            return [Discount(*row) for row in rows]
        else:
            raise ValueError(f"Discount for product with" f" id {product_id} not found")


@dataclass
class SqliteSalesDAO(SalesDAO):
    connection: Connection

    def add_sale(self, item: SoldItem) -> None:
        cur = self.connection.cursor()
        cur.execute(
            "INSERT INTO sales "
            "(product_id, amount, amount_paid, payment_method)"
            " VALUES (?, ?, ?, ?)",
            (item.id, item.units, item.total, item.payment_method),
        )
        cur.close()
        self.connection.commit()

    def get_all_sales(self) -> List[Sale]:
        cur = self.connection.cursor()
        cur.execute("SELECT * FROM sales")
        rows = cur.fetchall()
        cur.close()

        if rows:
            return [Sale(*row) for row in rows]
        else:
            raise ValueError("No sales in the database")

    def get_sales_for_product(self, product_id: int) -> List[Sale]:
        cur = self.connection.cursor()
        cur.execute("SELECT * FROM sales WHERE product_id=?", (product_id,))
        rows = cur.fetchall()
        cur.close()

        if rows:
            return [Sale(*row) for row in rows]
        else:
            raise ValueError(
                f"No sales for the product " f"with id {product_id} in the database"
            )

    def get_total_for_payment_method(self, payment_method: str) -> float:
        cur = self.connection.cursor()
        cur.execute(
            "SELECT SUM(amount_paid) FROM sales WHERE payment_method = ?",
            (payment_method,),
        )
        row = cur.fetchone()
        cur.close()

        if row:
            try:
                return float(row[0])
            except TypeError:
                return 0.00
        else:
            raise ValueError(f"No sales by method {payment_method}")
