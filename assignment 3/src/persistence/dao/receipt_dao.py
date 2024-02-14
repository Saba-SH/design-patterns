from dataclasses import dataclass
from sqlite3 import Connection
from typing import List, Protocol

from src.entities.models import Product, ProductInReceipt, Receipt
from src.static.constants import RECEIPT_CLOSED, RECEIPT_OPEN


class ReceiptDAO(Protocol):
    def create_receipt(self) -> Receipt:
        raise NotImplementedError

    def add_product_to_receipt(
        self, receipt_id: int, product: Product, quantity: int
    ) -> Receipt:
        raise NotImplementedError

    def get_receipt_by_id(self, receipt_id: int) -> Receipt:
        raise NotImplementedError

    def close_receipt(self, receipt_id: int) -> None:
        raise NotImplementedError

    def delete_receipt(self, receipt_id: int) -> None:
        raise NotImplementedError

    def get_all_receipts(self) -> List[Receipt]:
        raise NotImplementedError


@dataclass
class SqliteReceiptDAO(ReceiptDAO):
    connection: Connection

    def create_receipt(self) -> Receipt:
        cursor = self.connection.cursor()
        cursor.execute(
            "INSERT INTO receipts (status, total) VALUES (?, ?)", (RECEIPT_OPEN, 0)
        )
        receipt_id = cursor.lastrowid
        self.connection.commit()
        return Receipt(id=receipt_id, status=RECEIPT_OPEN, products=[], total=0)

    def get_products_for_receipt(self, receipt_id: int) -> List[ProductInReceipt]:
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT * FROM products_in_receipts WHERE receipt_id = ?", (receipt_id,)
        )
        rows = cursor.fetchall()
        return [
            ProductInReceipt(
                id=row[0],
                receipt_id=row[1],
                product_id=row[2],
                quantity=row[3],
                price=row[4],
                total=row[5],
            )
            for row in rows
        ]

    def get_receipt_by_id(self, receipt_id: int) -> Receipt:
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT id, status, total FROM receipts WHERE id = ?", (receipt_id,)
        )
        row = cursor.fetchone()
        if row:
            receipt = Receipt(id=row[0], status=row[1], products=[], total=row[2])
            products = self.get_products_for_receipt(receipt_id)
            receipt.products = products
            return receipt
        else:
            raise ValueError(f"Receipt with id<{receipt_id}> does not exist")

    def close_receipt(self, receipt_id: int) -> None:
        # check that receipt exists and raise an error if it doesn't
        self.get_receipt_by_id(receipt_id)

        cursor = self.connection.cursor()
        cursor.execute(
            "UPDATE receipts SET status = ? WHERE id = ?", (RECEIPT_CLOSED, receipt_id)
        )
        self.connection.commit()

    def add_product_to_receipt(
        self, receipt_id: int, product: Product, quantity: int
    ) -> Receipt:
        cursor = self.connection.cursor()

        product_total = product.price * quantity

        cursor.execute(
            "INSERT INTO products_in_receipts \n"
            "(receipt_id, product_id, quantity, price, total)\n"
            "VALUES (?, ?, ?, ?, ?)",
            (receipt_id, product.id, quantity, product.price, product_total),
        )

        cursor.execute(
            """
            UPDATE receipts
            SET total = total + ?
            WHERE id = ?
        """,
            (product_total, receipt_id),
        )

        self.connection.commit()

        return self.get_receipt_by_id(receipt_id)

    def delete_receipt(self, receipt_id: int) -> None:
        receipt = self.get_receipt_by_id(receipt_id)
        if receipt.status == RECEIPT_CLOSED:
            raise AssertionError(f"Receipt with id<{receipt_id}> is closed.")

        # Delete the receipt from the database
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM receipts WHERE id = ?", (receipt_id,))
        self.connection.commit()

    def get_all_receipts(self) -> List[Receipt]:
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM receipts")
        rows = cursor.fetchall()
        return [
            Receipt(id=row[0], status=row[1], products=[], total=row[2]) for row in rows
        ]
