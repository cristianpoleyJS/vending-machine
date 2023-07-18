from decimal import Decimal
from uuid import UUID
from attr import dataclass

from apps.vending.enums import BalanceTypeOperation


@dataclass
class BalanceOperationDto:
    user_id: UUID
    type_operation: BalanceTypeOperation
    amount: Decimal | None

    def __post_init__(self):  # it will be executed after the object is created
        if self.amount < Decimal("0.00"):
            raise ValueError("Amount cannot be a negative number")


@dataclass
class OrderOperationDto:
    slot_id: UUID
    user_id: UUID
