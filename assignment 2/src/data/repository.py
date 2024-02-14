from asyncio import Protocol
from dataclasses import dataclass
from typing import List

from src.data.dao import DiscountDAO, ProductDAO, SalesDAO
from src.data.objects import Discount, Product, Sale, SoldItem


class ProductRepository(Protocol):
    def add_product(self, product: Product) -> None:
        raise NotImplementedError

    def all_products(self) -> List[Product]:
        raise NotImplementedError

    def get_product_by_name(self, product_name: str) -> Product:
        raise NotImplementedError

    def get_product_by_id(self, product_id: int) -> Product:
        raise NotImplementedError


class DiscountRepository(Protocol):
    def add_discount(self, discount: Discount) -> None:
        raise NotImplementedError

    def all_discounts(self) -> List[Discount]:
        raise NotImplementedError

    def discounts_for_product(self, product_id: int) -> List[Discount]:
        raise NotImplementedError

    def get_discount_by_id(self, discount_id: int) -> Discount:
        raise NotImplementedError


class SalesRepository(Protocol):
    def add_sale(self, item: SoldItem) -> None:
        raise NotImplementedError

    def all_sales(self) -> List[Sale]:
        raise NotImplementedError

    def sales_for_product(self, product_id: int) -> List[Sale]:
        raise NotImplementedError

    def revenue_from_payment_method(self, payment_method: str) -> float:
        raise NotImplementedError


@dataclass
class DAOProductRepository(ProductRepository):
    product_dao: ProductDAO

    def add_product(self, product: Product) -> None:
        self.product_dao.add_product(product)

    def all_products(self) -> List[Product]:
        return self.product_dao.get_all_products()

    def get_product_by_name(self, product_name: str) -> Product:
        return self.product_dao.get_by_name(product_name)

    def get_product_by_id(self, product_id: int) -> Product:
        return self.product_dao.get_by_id(product_id)


@dataclass
class DAODiscountRepository(DiscountRepository):
    discount_dao: DiscountDAO

    def add_discount(self, discount: Discount) -> None:
        self.discount_dao.add_discount(discount)

    def all_discounts(self) -> List[Discount]:
        return self.discount_dao.get_all_discounts()

    def discounts_for_product(self, product_id: int) -> List[Discount]:
        return self.discount_dao.get_discounts_for_product(product_id)

    def get_discount_by_id(self, discount_id: int) -> Discount:
        return self.discount_dao.get_by_id(discount_id)


@dataclass
class DAOSalesRepository(SalesRepository):
    sales_dao: SalesDAO

    def add_sale(self, item: SoldItem) -> None:
        self.sales_dao.add_sale(item)

    def all_sales(self) -> List[Sale]:
        return self.sales_dao.get_all_sales()

    def sales_for_product(self, product_id: int) -> List[Sale]:
        return self.sales_dao.get_sales_for_product(product_id)

    def revenue_from_payment_method(self, payment_method: str) -> float:
        return self.sales_dao.get_total_for_payment_method(payment_method)
