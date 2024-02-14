import pytest

from src.entities.models import Product
from src.persistence.dao.receipt_dao import ReceiptDAO
from src.persistence.dao.unit_dao import UnitDAO


def test_create_receipt(receipt_dao: ReceiptDAO) -> None:
    receipt = receipt_dao.create_receipt()

    assert receipt.status == "open"
    assert receipt.total == 0
    assert len(receipt.products) == 0


def test_add_product_to_receipt(unit_dao: UnitDAO, receipt_dao: ReceiptDAO) -> None:
    unit_dao.create_unit("კგ")
    unit = unit_dao.get_unit_by_name("კგ")
    product = Product(id=0, unit_id=unit.id, name="Product", barcode="123", price=10.0)
    receipt = receipt_dao.create_receipt()

    updated_receipt = receipt_dao.add_product_to_receipt(
        receipt.id, product, quantity=2
    )

    assert updated_receipt.status == "open"
    assert updated_receipt.total == 20.0
    assert len(updated_receipt.products) == 1
    assert updated_receipt.products[0].product_id == product.id
    assert updated_receipt.products[0].quantity == 2
    assert updated_receipt.products[0].total == 20.0


def test_close_receipt(unit_dao: UnitDAO, receipt_dao: ReceiptDAO) -> None:
    unit_dao.create_unit("კგ")
    unit = unit_dao.get_unit_by_id(1)
    product = Product(id=1, unit_id=unit.id, name="Product", barcode="123", price=10.0)
    receipt = receipt_dao.create_receipt()

    updated_receipt = receipt_dao.add_product_to_receipt(
        receipt.id, product, quantity=2
    )
    receipt_dao.close_receipt(updated_receipt.id)

    closed_receipt = receipt_dao.get_receipt_by_id(updated_receipt.id)

    assert closed_receipt.status == "closed"


def test_delete_receipt(unit_dao: UnitDAO, receipt_dao: ReceiptDAO) -> None:
    unit_dao.create_unit("კგ")
    unit = unit_dao.get_unit_by_name("კგ")
    product = Product(id=1, unit_id=unit.id, name="Product", barcode="123", price=10.0)
    receipt = receipt_dao.create_receipt()

    updated_receipt = receipt_dao.add_product_to_receipt(
        receipt.id, product, quantity=2
    )
    receipt_dao.close_receipt(updated_receipt.id)

    with pytest.raises(AssertionError, match="Receipt with id<1> is closed."):
        receipt_dao.delete_receipt(updated_receipt.id)

    open_receipt = receipt_dao.create_receipt()
    receipt_dao.delete_receipt(open_receipt.id)

    with pytest.raises(ValueError, match="Receipt with id<2> does not exist"):
        receipt_dao.get_receipt_by_id(open_receipt.id)
