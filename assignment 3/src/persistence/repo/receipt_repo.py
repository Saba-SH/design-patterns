from dataclasses import dataclass
from typing import Protocol

from src.entities.models import Product, Receipt
from src.persistence.dao.receipt_dao import ReceiptDAO


class ReceiptRepository(Protocol):
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


@dataclass
class DAOReceiptRepository(ReceiptRepository):
    dao: ReceiptDAO

    def create_receipt(self) -> Receipt:
        return self.dao.create_receipt()

    def add_product_to_receipt(
        self, receipt_id: int, product: Product, quantity: int
    ) -> Receipt:
        return self.dao.add_product_to_receipt(receipt_id, product, quantity)

    def get_receipt_by_id(self, receipt_id: int) -> Receipt:
        return self.dao.get_receipt_by_id(receipt_id)

    def close_receipt(self, receipt_id: int) -> None:
        self.dao.close_receipt(receipt_id)

    def delete_receipt(self, receipt_id: int) -> None:
        self.dao.delete_receipt(receipt_id)
