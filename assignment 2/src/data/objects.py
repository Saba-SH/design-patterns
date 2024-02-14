from dataclasses import dataclass


@dataclass
class Product:
    id: int
    name: str
    price: float


@dataclass
class Discount:
    id: int
    product_id: int
    discount_pct: int
    batch_size: int


@dataclass
class SoldItem:
    id: int
    units: int
    price: float
    total: float
    payment_method: str


@dataclass
class Sale:
    id: int
    product_id: int
    amount: int
    amount_paid: float
    payment_method: str
