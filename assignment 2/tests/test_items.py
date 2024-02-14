from src.items.cart import Cart
from src.items.item import Batch, Discounted, Item
from src.items.receipt import Receipt
from src.static.static import RECEIPT_CLOSED, RECEIPT_OPEN, RECEIPT_PENDING


def test_item_price() -> None:
    item = Item("item0", 5)
    assert item.price() == 5


def test_batch_price() -> None:
    item = Item("item0", 5)
    batch = Batch(item, 3)

    assert batch.price() == 3 * 5


def test_cart_add() -> None:
    item = Item("item0", 5)
    cart = Cart()
    cart.add(item)

    assert cart.total_items() == 1
    assert (
        cart._items[0].name() == item.name() and cart._items[0].price() == item.price()
    )


def test_cart_with_single_item_price() -> None:
    item = Item("item0", 5)
    cart = Cart()
    cart.add(item)

    assert cart.price() == 5 and item.price() == cart.price()


def test_cart_with_multiple_items_price() -> None:
    item0 = Item("item0", 5)
    item1 = Item("item1", 5)
    item2 = Item("item2", 5)

    item2_batch = Batch(item2, 3)

    cart = Cart()

    for i in range(3):
        cart.add(item0)
        cart.add(item1)

    cart.add(item2_batch)

    assert cart.price() == 3 * item0.price() + 3 * item1.price() + item2_batch.price()


def test_cart_remove() -> None:
    item = Item("item0", 5)
    cart = Cart()
    cart.add(item)
    cart.remove(item.name())

    assert cart.total_items() == 0


def test_cart_item_amount() -> None:
    item0 = Item("item0", 5)
    item1 = Item("Item1", 5)
    item2 = Item("Item2", 5)
    cart = Cart()

    for i in range(5):
        cart.add(item0)

    for i in range(3):
        cart.add(item1)

    assert cart.item_amount(item0.name()) == 5
    assert cart.item_amount(item1.name()) == 3
    assert cart.item_amount(item2.name()) == 0
    assert cart.item_amount(item0.name()) == 5


def test_cart_remove_from_big_cart() -> None:
    item0 = Item("item0", 5)
    item1 = Item("item1", 5)
    item2 = Item("item2", 5)
    item3 = Item("item3", 5)
    cart = Cart()

    for i in range(3):
        cart.add(item0)
        cart.add(item1)
        cart.add(item2)
        cart.add(item3)

    cart.remove(item1.name())

    assert cart.total_items() == 9

    assert cart.item_amount(item1.name()) == 0
    assert cart.item_amount(item0.name()) == 3
    assert cart.item_amount(item2.name()) == 3
    assert cart.item_amount(item3.name()) == 3

    cart.remove(item2.name())

    assert cart.total_items() == 6

    assert cart.item_amount(item1.name()) == 0
    assert cart.item_amount(item2.name()) == 0
    assert cart.item_amount(item0.name()) == 3
    assert cart.item_amount(item3.name()) == 3


def test_cart_remove_one() -> None:
    item0 = Item("item0", 5)
    item1 = Item("item1", 5)
    item2 = Item("item2", 5)
    item3 = Item("item3", 5)
    cart = Cart()

    for i in range(4):
        cart.add(item0)
        cart.add(item1)
        cart.add(item2)
        cart.add(item3)

    cart.remove_one(item0.name())
    assert cart.item_amount(item0.name()) == 3

    cart.remove_one(item0.name())
    assert cart.item_amount(item0.name()) == 2

    cart.remove_one(item1.name())
    assert cart.item_amount(item1.name()) == 3

    cart.remove_one(item2.name())
    cart.remove_one(item2.name())
    assert cart.item_amount(item2.name()) == 2


def test_cart_empty() -> None:
    item0 = Item("item0", 5)
    item1 = Item("item1", 5)
    cart = Cart()

    for i in range(3):
        cart.add(item0)
        cart.add(item1)

    cart.empty()

    assert cart.total_items() == 0


def test_discount() -> None:
    item0 = Item("item0", 5)

    item0_disc = Discounted(item0, 10)

    assert item0_disc.price() == item0.price() * 90 / 100

    item0_batch_disc = Discounted(Batch(item0, 3), 15)

    assert item0_batch_disc.price() == item0.price() * 3 * 85 / 100


def test_receipt_open() -> None:
    receipt = Receipt()

    assert receipt.status == RECEIPT_PENDING

    receipt.open()

    assert receipt.status == RECEIPT_OPEN
    receipt.add_item(Item("item0", 5))
    assert receipt.status == RECEIPT_OPEN


def test_receipt_close() -> None:
    receipt = Receipt()

    assert receipt.status == RECEIPT_PENDING

    receipt.open()
    receipt.add_item(Item("item0", 5))

    receipt.close()
    assert receipt.status == RECEIPT_CLOSED
