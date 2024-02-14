from dataclasses import dataclass, field
from typing import Callable, List

from src.data.objects import SoldItem
from src.items.cart import Cart
from src.items.item import Item
from src.static.static import RECEIPT_CLOSED, RECEIPT_OPEN, RECEIPT_PENDING


@dataclass
class Receipt:
    cart: Cart = field(default_factory=Cart)
    customer_number: int = field(default=0)
    status: int = field(default=RECEIPT_PENDING)
    sold_items: List[SoldItem] = field(default_factory=list)

    def open(self) -> None:
        self.status = RECEIPT_OPEN

    def close(self) -> None:
        self.status = RECEIPT_CLOSED

    def add_item(self, item: Item) -> None:
        self.cart.add(item)

    def add_sold_item(self, item: SoldItem) -> None:
        self.sold_items.append(item)

    def get_sold_items(self) -> List[SoldItem]:
        return self.sold_items

    def total(
        self, discount_pct_calculator: Callable[[int], int] = lambda x: 0
    ) -> float:
        return self.cart.price() * (
            (100 - discount_pct_calculator(self.customer_number)) / 100
        )
