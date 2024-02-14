from dataclasses import dataclass, field
from typing import Protocol


class Sellable(Protocol):
    def name(self) -> str:
        pass

    def price(self) -> float:
        pass


@dataclass
class Item:
    _name: str
    _price: float
    id: int = field(default=0)

    def name(self) -> str:
        return self._name

    def price(self) -> float:
        return self._price


@dataclass
class Batch:
    item: Item
    amount: int

    def name(self) -> str:
        return "Batch of " + str(self.amount) + " " + self.item.name()

    def price(self) -> float:
        return self.item.price() * self.amount


@dataclass
class Discounted(Sellable):
    item: Sellable
    discount_pct: int

    def name(self) -> str:
        return self.item.name()

    def price(self) -> float:
        return self.item.price() * (100 - self.discount_pct) / 100
