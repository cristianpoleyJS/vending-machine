from decimal import Decimal
from uuid import UUID
from attr import dataclass

from apps.vending.enums import BalanceTypeOperation


@dataclass
class BalanceOperationDto:
    user_id: UUID
    type_operation: BalanceTypeOperation
    amount: Decimal | None


@dataclass
class OrderOperationDto:
    slot_id: UUID
    user_id: UUID
