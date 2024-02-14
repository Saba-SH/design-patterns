from dataclasses import dataclass

from src.entities.models import SaleReport
from src.persistence.dao.sales_dao import SalesDAO


class SalesRepository:
    def add_sale(self, revenue: float) -> None:
        raise NotImplementedError

    def generate_sales_report(self) -> SaleReport:
        raise NotImplementedError


@dataclass
class DAOSalesRepository(SalesRepository):
    dao: SalesDAO

    def add_sale(self, revenue: float) -> None:
        self.dao.add_sale(revenue)

    def generate_sales_report(self) -> SaleReport:
        return self.dao.generate_sales_report()
