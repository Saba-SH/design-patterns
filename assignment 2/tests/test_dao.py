from tests.conftest import discount_dao, product_dao, sales_dao


def test_products_add_get_all_len(product_dao) -> None:
    all_products = product_dao.get_all_products()

    assert len(all_products) == 3


def test_products_add_get_all_value(product_dao) -> None:
    all_products = product_dao.get_all_products()

    product_names = [p.name for p in all_products]

    assert "p1" in product_names
    assert "p2" in product_names
    assert "p3" in product_names


def test_products_get_by_name(product_dao) -> None:
    p1 = product_dao.get_by_name("p1")
    assert p1.name == "p1" and p1.price == 1
    p2 = product_dao.get_by_name("p2")
    assert p2.name == "p2" and p2.price == 3
    p3 = product_dao.get_by_name("p3")
    assert p3.name == "p3" and p3.price == 5


def test_discounts_get_all_len(discount_dao) -> None:
    all_discounts = discount_dao.get_all_discounts()

    assert len(all_discounts) == 4


def test_discounts_get_all_value(discount_dao) -> None:
    all_discounts = discount_dao.get_all_discounts()

    product_ids = [d.product_id for d in all_discounts]

    assert 1 in product_ids
    assert 2 in product_ids
    assert 3 not in product_ids


def test_discounts_multiple_batch_sizes(discount_dao) -> None:
    discounts = discount_dao.get_discounts_for_product(1)

    bsize_and_pct = sorted([(d.batch_size, d.discount_pct) for d in discounts])

    assert bsize_and_pct == [(1, 15), (3, 20), (5, 25)]


def test_discounts_one_batch(discount_dao) -> None:
    discounts = discount_dao.get_discounts_for_product(2)

    bsize_and_pct = sorted([(d.batch_size, d.discount_pct) for d in discounts])

    assert bsize_and_pct == [(4, 10)]


def test_sales_get_all_len(sales_dao) -> None:
    all_sales = sales_dao.get_all_sales()

    assert len(all_sales) == 8


def test_sales_for_product(sales_dao) -> None:
    sales_for_1 = sales_dao.get_sales_for_product(1)
    assert len(sales_for_1) == 3

    sales_for_2 = sales_dao.get_sales_for_product(2)
    assert len(sales_for_2) == 3

    sales_for_3 = sales_dao.get_sales_for_product(3)
    assert len(sales_for_3) == 2


def test_sales_payment_method(sales_dao) -> None:
    cash_amount = sales_dao.get_total_for_payment_method("cash")
    card_amount = sales_dao.get_total_for_payment_method("card")

    assert cash_amount == 12
    assert card_amount == 43
