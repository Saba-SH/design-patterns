from tests.conftest import discount_dao, product_dao

from src.data.repository import DAODiscountRepository
from src.items.adapter import product_as_item
from src.items.cart import Cart
from src.items.item import Item
from src.static.static import RECEIPT_CLOSED
from src.store.cashier import Cashier
from src.store.terminal import Terminal


def test_terminal() -> None:
    terminal = Terminal()

    assert terminal.cash == 0
    assert terminal.card == 0

    terminal.pay_by_cash(3.30)
    terminal.pay_by_card(4.40)

    assert terminal.cash == 3.30
    assert terminal.card == 4.40


def test_terminal_revenue_info() -> None:
    terminal = Terminal()

    terminal.pay_by_cash(3.30)
    terminal.pay_by_card(4.40)

    terminal.pay_by_cash(2.60)
    terminal.pay_by_card(4.50)

    revenue_info = terminal.get_revenue_info()

    for info in revenue_info:
        assert info.payment_type in ["cash", "card"]

        if info.payment_type == "cash":
            assert info.paid_amount == 3.30 + 2.60
        else:
            assert info.paid_amount == 4.40 + 4.50


def test_cashier_serve_closes_receipt(discount_dao) -> None:
    item = Item("item0", 5)
    cart = Cart()
    cart.add(item)
    cashier = Cashier()

    receipt = cashier.serve_customer(cart, 0, ["cash"], DAODiscountRepository(discount_dao))

    assert receipt.status == RECEIPT_CLOSED


def test_cashier_serve_receipt_values(product_dao, discount_dao) -> None:
    i1 = product_as_item(product_dao.get_by_id(1))
    i3 = product_as_item(product_dao.get_by_id(3))
    cart = Cart()
    cart.add(i1)
    cart.add(i3)
    cashier = Cashier()

    receipt = cashier.serve_customer(cart, 0, ["cash", "card"], DAODiscountRepository(discount_dao))

    sold_items = receipt.get_sold_items()
    ids = [si.id for si in sold_items]
    units = [si.units for si in sold_items]

    assert 1 in ids
    assert 2 not in ids
    assert 3 in ids

    assert 1 in units
    assert 2 not in units
    assert 3 not in units
