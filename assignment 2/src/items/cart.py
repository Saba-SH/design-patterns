from dataclasses import dataclass, field
from typing import List

from src.items.item import Sellable


@dataclass
class Cart:
    _name: str = field(default="")
    _items: List[Sellable] = field(default_factory=list[Sellable])

    def name(self) -> str:
        return "Shopping Cart " + self._name

    def price(self) -> float:
        return sum(item.price() for item in self._items)

    def add(self, item: Sellable) -> None:
        self._items.append(item)

    def get_items(self) -> List[Sellable]:
        return self._items

    def remove_one(self, item_name: str) -> None:
        for i in range(len(self._items)):
            if self._items[i].name() == item_name:
                self._items.pop(i)
                break

    def remove(self, item_name: str) -> None:
        self._items = [item for item in self._items if item.name() != item_name]

    def empty(self) -> None:
        self._items.clear()

    def item_amount(self, item_name: str) -> int:
        return len([1 for item in self._items if item.name() == item_name])

    def total_items(self) -> int:
        return len(self._items)
