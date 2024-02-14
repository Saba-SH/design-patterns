from typing import List

from pydantic import BaseModel


class Unit(BaseModel):
    id: int
    name: str


class Product(BaseModel):
    id: int
    unit_id: int
    name: str
    barcode: str
    price: float


class ProductInReceipt(BaseModel):
    id: int
    receipt_id: int
    product_id: int
    quantity: int
    price: float
    total: float


class Receipt(BaseModel):
    id: int
    status: str
    products: List[ProductInReceipt]
    total: float


class SaleReport(BaseModel):
    id: int
    n_receipts: int
    revenue: float
