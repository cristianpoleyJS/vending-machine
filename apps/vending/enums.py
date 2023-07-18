
from enum import Enum


class BalanceTypeOperation(str, Enum):
    ADD = "add"
    REFUND = "refund"
    ORDER_PRODUCT = "order_product"
