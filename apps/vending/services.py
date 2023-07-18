from decimal import Decimal
from apps.vending.exceptions import OrderError, UserNotFound, VendingMachineSlotNotFound
from apps.vending.models import User, VendingMachineSlot
from apps.vending.validators import BalanceOperationDto, BalanceTypeOperation, OrderOperationDto


class BalanceOperatorService:

    def execute(self, dto: BalanceOperationDto) -> User:
        try:
            user = User.objects.get(id=dto.user_id)
        except User.DoesNotExist:
            raise UserNotFound(f"User not found with ID {dto.user_id}")

        if dto.type_operation == BalanceTypeOperation.REFUND:
            user.balance = Decimal("0.00")
        else:
            user.balance += dto.amount
        user.save()
        return user


class OrderOperatorService:

    def execute(self, dto: OrderOperationDto) -> User:
        try:
            user = User.objects.get(id=dto.user_id)
        except User.DoesNotExist:
            raise UserNotFound(f"User not found with ID {dto.user_id}")
        try:
            slot = VendingMachineSlot.objects.get(id=dto.slot_id)
        except VendingMachineSlot.DoesNotExist:
            raise VendingMachineSlotNotFound(
                f"Slot not found with ID {dto.slot_id}")

        if user.balance < slot.product.price:
            raise OrderError("Not enough balance")
        if slot.quantity == 0:
            raise OrderError("Not enough product quantity")

        slot.quantity -= 1
        slot.save()
        user.balance -= slot.product.price
        user.save()
        return user
