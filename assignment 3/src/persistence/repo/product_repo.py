from dataclasses import dataclass
from typing import List, Protocol

from src.entities.models import Product
from src.persistence.dao.product_dao import ProductDAO


class ProductRepository(Protocol):
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
class DAOProductRepository(ProductRepository):
    dao: ProductDAO

    def create_product(
        self, unit_id: int, name: str, barcode: str, price: float
    ) -> Product:
        return self.dao.create_product(unit_id, name, barcode, price)  # type: ignore

    def get_product_by_id(self, product_id: int) -> Product:
        return self.dao.get_product_by_id(product_id)

    def get_all_products(self) -> List[Product]:
        return self.dao.get_all_products()  # type: ignore

    def update_product(self, updated_product: Product) -> None:
        self.dao.update_product(updated_product)
