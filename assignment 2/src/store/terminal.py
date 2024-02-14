from dataclasses import dataclass
from typing import List


@dataclass
class PaymentInfo:
    payment_type: str
    paid_amount: float


class Terminal:
    cash: float
    card: float

    def __init__(self) -> None:
        self.cash = 0.0
        self.card = 0.0

    def pay_by_cash(self, total: float) -> None:
        self.cash += total

    def pay_by_card(self, total: float) -> None:
        self.card += total

    def get_revenue_info(self) -> List[PaymentInfo]:
        res = [PaymentInfo("cash", self.cash), PaymentInfo("card", self.card)]
        return res
