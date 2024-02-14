from dataclasses import dataclass
from typing import Callable, List

from src.data.objects import SoldItem
from src.data.repository import DiscountRepository
from src.items.cart import Cart
from src.items.item import Batch
from src.items.receipt import Receipt
from src.static.static import RECEIPT_PENDING


@dataclass
class Cashier:
    @staticmethod
    def serve_customer(
        cart: Cart,
        customer_number: int,
        payment_methods: List[str],
        discount_repository: DiscountRepository,
        discount_pct_calculator: Callable[[int], int] = lambda x: 0,
    ) -> Receipt:
        receipt = Receipt(cart, customer_number, RECEIPT_PENDING, [])
        receipt.open()

        for i, item in enumerate(cart.get_items()):
            if isinstance(item, Batch):
                try:
                    discount = [
                        d
                        for d in discount_repository.discounts_for_product(item.item.id)
                        if d.batch_size == item.amount
                    ][0].discount_pct
                except ValueError:
                    discount = 0

                total = (
                    item.price()
                    * item.amount
                    * (100 - discount - discount_pct_calculator(customer_number))
                    / 100
                )

                sold_item = SoldItem(
                    item.item.id,
                    item.amount,
                    total / item.amount,
                    total,
                    payment_methods[i],
                )
                receipt.add_sold_item(sold_item)
            else:
                itemid = getattr(item, "id", 0)

                try:
                    discount = [
                        d
                        for d in discount_repository.discounts_for_product(itemid)
                        if d.batch_size == 1
                    ][0].discount_pct
                except ValueError:
                    discount = 0
                except IndexError:
                    discount = 0

                total = (
                    item.price()
                    * (100 - discount - discount_pct_calculator(customer_number))
                    / 100
                )

                sold_item = SoldItem(itemid, 1, total, total, payment_methods[i])
                receipt.add_sold_item(sold_item)

        receipt.close()

        return receipt
