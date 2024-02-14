from dataclasses import dataclass, field
from typing import List, Tuple

from src.data.objects import SoldItem
from src.data.repository import DiscountRepository, ProductRepository, SalesRepository
from src.items.adapter import product_as_batch, product_as_item
from src.items.cart import Cart
from src.items.item import Sellable
from src.items.receipt import Receipt
from src.store.cashier import Cashier
from src.store.manager import Manager
from src.store.terminal import PaymentInfo, Terminal


@dataclass
class Store:
    product_repository: ProductRepository
    discount_repository: DiscountRepository
    sales_repository: SalesRepository
    cashier: Cashier = field(default_factory=Cashier)
    manager: Manager = field(default_factory=Manager)
    terminal: Terminal = field(default_factory=Terminal)
    sold_items: List[SoldItem] = field(default_factory=list)

    def get_sold_items(self) -> List[SoldItem]:
        return self.sold_items

    def add_receipt(self, receipt: Receipt) -> None:
        self.sold_items += receipt.get_sold_items()

    def get_product_info(self) -> List[str]:
        info = ["Products:"]

        products = self.product_repository.all_products()
        for product in products:
            item = product_as_item(product)
            info.append(f"{item.name()} - Price: {item.price():.2f}")

        return info

    def get_discount_info(self) -> List[str]:
        info = ["Discounts:"]

        discounts = self.discount_repository.all_discounts()
        for discount in discounts:
            discounted_product = self.product_repository.get_product_by_id(
                discount.product_id
            )
            if discount.batch_size == 1:
                item: Sellable = product_as_item(discounted_product)
            else:
                item = product_as_batch(discounted_product, discount.batch_size)
            info.append(f"Discount for {item.name()}: " f"{discount.discount_pct}%")

        return info

    def get_revenue_info(self) -> List[PaymentInfo]:
        return self.terminal.get_revenue_info()

    def sold_item_description(self, item: SoldItem) -> str:
        item_name = self.product_repository.get_product_by_id(item.id).name
        return (
            f"{item_name}: {item.units} unit(s), "
            f"price: {item.price}, total: {item.total}"
        )

    def serve_customer(
        self, cart: Cart, customer_num: int, payment_methods: List[str]
    ) -> Tuple[Receipt, str]:
        receipt = self.cashier.serve_customer(
            cart, customer_num, payment_methods, self.discount_repository
        )

        self.add_receipt(receipt)

        receipt_description = ""
        for sold_item in receipt.get_sold_items():
            receipt_description += self.sold_item_description(sold_item) + "\n"

        for sold_item in receipt.get_sold_items():
            if sold_item.payment_method == "cash":
                self.terminal.pay_by_cash(sold_item.total)
            elif sold_item.payment_method == "card":
                self.terminal.pay_by_card(sold_item.total)

            self.sales_repository.add_sale(sold_item)

        return receipt, receipt_description

    def clear_register(self) -> None:
        self.sold_items = []
        self.terminal.cash = 0
        self.terminal.card = 0
