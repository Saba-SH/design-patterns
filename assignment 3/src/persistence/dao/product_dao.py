from dataclasses import dataclass
from sqlite3 import Connection
from typing import List, Protocol

from src.entities.models import Product


class ProductDAO(Protocol):
    def create_product(
        self, unit_id: int, name: str, barcode: str, price: float
    ) -> Product:
        raise NotImplementedError

    def get_product_by_id(self, product_id: int) -> Product:
        raise NotImplementedError

    def get_all_products(self) -> List[Product]:
        raise NotImplementedError

    def update_product(self, updated_product: Product) -> None:
        raise NotImplementedError


@dataclass
class SqliteProductDAO(ProductDAO):
    connection: Connection

    def create_product(
        self, unit_id: int, name: str, barcode: str, price: float
    ) -> Product:
        error_msg_on_exist = f"Product with barcode<{barcode}> already exists."
        try:
            self.get_product_by_barcode(barcode)
            raise ValueError(error_msg_on_exist)
        except ValueError as e:
            if str(e) == error_msg_on_exist:
                raise

            cursor = self.connection.cursor()
            cursor.execute(
                "INSERT INTO products "
                "(unit_id, name, barcode, price) VALUES (?, ?, ?, ?)",
                (unit_id, name, barcode, price),
            )
            self.connection.commit()
            return self.get_product_by_barcode(barcode)

    def get_product_by_id(self, product_id: int) -> Product:
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        row = cursor.fetchone()
        if row:
            return Product(
                id=row[0], unit_id=row[1], name=row[2], barcode=row[3], price=row[4]
            )
        else:
            raise ValueError(f"Product with id<{product_id}> does not exist")

    def get_product_by_barcode(self, barcode: str) -> Product:
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM products WHERE barcode = ?", (barcode,))
        row = cursor.fetchone()
        if row:
            return Product(
                id=row[0], unit_id=row[1], name=row[2], barcode=row[3], price=row[4]
            )
        else:
            raise ValueError(f"Unit with barcode<{barcode}> does not exist")

    def get_all_products(self) -> List[Product]:
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM products")
        rows = cursor.fetchall()
        return [
            Product(
                id=row[0], unit_id=row[1], name=row[2], barcode=row[3], price=row[4]
            )
            for row in rows
        ]

    def update_product(self, updated_product: Product) -> None:
        try:
            old_product = self.get_product_by_id(updated_product.id)
            # The fields that are None in updated_product will be
            # taken from old_product. others will be taken from updated_product
            new_product_values = {
                attr: getattr(updated_product, attr)
                if getattr(updated_product, attr) is not None
                else getattr(old_product, attr)
                for attr in Product.__annotations__
            }
            p = Product(**new_product_values, id=old_product.id)
            cursor = self.connection.cursor()
            cursor.execute(
                "UPDATE products SET \n"
                "unit_id = ?, name = ?, barcode = ?, price = ?\n"
                "WHERE id = ?",
                (p.unit_id, p.name, p.barcode, p.price, p.id),
            )
            self.connection.commit()
        except ValueError:
            raise ValueError(f"Product with id<{updated_product.id}> does not exist.")
