from dataclasses import dataclass
from sqlite3 import Connection
from typing import Protocol

from src.entities.models import SaleReport


class SalesDAO(Protocol):
    def add_sale(self, revenue: float) -> None:
        raise NotImplementedError

    def generate_sales_report(self) -> SaleReport:
        raise NotImplementedError


@dataclass
class SqliteSalesDAO(SalesDAO):
    connection: Connection

    def make_one_sale(self) -> None:
        cursor = self.connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM sale_reports")
        count = cursor.fetchone()[0]

        if count != 1:
            if count != 0:
                cursor.execute("DELETE * FROM sale_reports")
                self.connection.commit()

            cursor.execute(
                "INSERT INTO sale_reports (n_receipts, revenue) VALUES (0, 0)"
            )

    def add_sale(self, revenue: float) -> None:
        self.make_one_sale()
        cursor = self.connection.cursor()
        cursor.execute(
            "UPDATE sale_reports SET "
            "n_receipts = n_receipts + 1, revenue = revenue + ? "
            "WHERE id = 1",
            (revenue,),
        )
        self.connection.commit()

    def generate_sales_report(self) -> SaleReport:
        self.make_one_sale()
        cursor = self.connection.cursor()
        cursor.execute("SELECT n_receipts, revenue FROM sale_reports WHERE id = 1")
        row = cursor.fetchone()
        return SaleReport(id=1, n_receipts=row[0], revenue=row[1])
