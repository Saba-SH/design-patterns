from src.data.objects import Product
from src.items.item import Batch, Item


def product_as_item(product: Product) -> Item:
    return Item(product.name, product.price, product.id)


def product_as_batch(product: Product, amount: int) -> Batch:
    return Batch(Item(product.name, product.price, product.id), amount)
