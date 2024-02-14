import random
from typing import List, Tuple

from src.data.repository import ProductRepository
from src.items.adapter import product_as_item
from src.items.cart import Cart
from src.store.store import Store


def random_cart(product_repository: ProductRepository) -> Tuple[Cart, List[str]]:
    all_products = product_repository.all_products()
    chosen_products = random.sample(all_products, random.randint(1, len(all_products)))

    items = [product_as_item(p) for p in chosen_products]
    payment_methods = []

    cart = Cart()

    for item in items:
        for i in range(random.randint(1, 5)):
            cart.add(item)
            payment_methods.append(random.choice(["cash", "card"]))

    return cart, payment_methods


def x_report(store: Store) -> None:
    print("X REPORT\n")

    sold_items = store.get_sold_items()
    sold_item_ids = list(set([s.id for s in sold_items]))

    for sold_item_id in sold_item_ids:
        product_name = store.product_repository.get_product_by_id(sold_item_id).name
        print(
            f"Product: {product_name}, "
            f"Sales: {sum([s.units for s in sold_items if s.id == sold_item_id])}"
        )

    print()
    revenue_info = store.get_revenue_info()
    for payment_info in revenue_info:
        print(
            f"Payment: {payment_info.payment_type.capitalize()}, "
            f"Revenue: {payment_info.paid_amount:.2f}"
        )


def simulate(store: Store) -> None:
    for i in range(300):
        print(f"Serving customer {i}")
        cart, payment_methods = random_cart(store.product_repository)
        receipt, description = store.serve_customer(cart, i, payment_methods)

        print(description)

        if i % 20 == 19:
            xre = input("Make X report? y/n ")
            if xre[0] == "y":
                x_report(store)
                input("Enter anything to continue ")
            else:
                pass

        if i % 100 == 99:
            zre = input("Make Z report? y/n ")
            if zre[0] == "y":
                store.clear_register()
                print("Store register cleared")
                input("Enter anything to continue ")
            else:
                pass
