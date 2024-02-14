import pytest

from src.entities.models import Product
from src.persistence.dao.product_dao import ProductDAO


def test_get_all_no_products_empty_list(product_dao: ProductDAO) -> None:
    products = product_dao.get_all_products()
    assert len(products) == 0


def test_get_all_products(product_dao: ProductDAO) -> None:
    product_dao.create_product(unit_id=1, name="product1", barcode="111", price=20.99)
    product_dao.create_product(unit_id=2, name="product2", barcode="222", price=30.99)
    product_dao.create_product(unit_id=1, name="product3", barcode="333", price=40.99)

    products = product_dao.get_all_products()

    assert len(products) == 3
    assert all(isinstance(product, Product) for product in products)


def test_create_product(product_dao: ProductDAO) -> None:
    product_id = product_dao.create_product(1, "product1", "1234567890", 10.99)
    assert product_id is not None
    products = product_dao.get_all_products()
    assert len(products) == 1
    assert products[0].name == "product1"

    product_id = product_dao.create_product(1, "product2", "0987654321", 9.99)
    products = product_dao.get_all_products()
    assert len(products) == 2


def test_create_product_raises_error_on_existing_barcode(
    product_dao: ProductDAO,
) -> None:
    product_dao.create_product(1, "product1", "1234567890", 10.99)
    with pytest.raises(ValueError):
        product_dao.create_product(1, "product2", "1234567890", 3.99)


def test_get_product_by_id(product_dao: ProductDAO) -> None:
    retrieved_product = product_dao.create_product(1, "product1", "1234567890", 10.99)

    assert retrieved_product.id == retrieved_product.id
    assert retrieved_product.unit_id == 1
    assert retrieved_product.name == "product1"
    assert retrieved_product.barcode == "1234567890"
    assert retrieved_product.price == 10.99


def test_get_product_raises_error_on_nonexistent_id(product_dao: ProductDAO) -> None:
    with pytest.raises(ValueError):
        product_dao.get_product_by_id(1)

    product_dao.create_product(1, "product1", "1234567890", 10.99)

    with pytest.raises(ValueError):
        product_dao.get_product_by_id(2)
