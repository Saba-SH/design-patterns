from dataclasses import dataclass

from src.persistence.repo.product_repo import ProductRepository
from src.persistence.repo.receipt_repo import ReceiptRepository
from src.persistence.repo.sales_repo import SalesRepository
from src.persistence.repo.unit_repo import UnitRepository


@dataclass
class POSRepository:
    unit_repository: UnitRepository
    product_repository: ProductRepository
    receipt_repository: ReceiptRepository
    sales_repository: SalesRepository
