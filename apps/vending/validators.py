from decimal import Decimal
from rest_framework import serializers

from apps.vending.enums import BalanceTypeOperation
from apps.vending.request_dto import BalanceOperationDto, OrderOperationDto


class ListSlotsValidator(serializers.Serializer):
    quantity = serializers.IntegerField(
        required=False, min_value=0, default=None)


class LoginValidator(serializers.Serializer):
    name = serializers.CharField(required=True, max_length=200)


class BalanceViewValidator(serializers.Serializer):
    user_id = serializers.UUIDField(required=True)
    type_operation = serializers.ChoiceField(
        choices=[BalanceTypeOperation.ADD.value, BalanceTypeOperation.REFUND.value, BalanceTypeOperation.ORDER_PRODUCT.value])
    amount = serializers.DecimalField(
        required=False, max_digits=4, decimal_places=2)

    def to_dto(self) -> BalanceOperationDto:
        return BalanceOperationDto(
            user_id=self.validated_data["user_id"],
            type_operation=BalanceTypeOperation(
                self.validated_data["type_operation"]),
            amount=self.validated_data.get("amount"),
        )

    def validate(self, data):
        if data.get("type_operation") == BalanceTypeOperation.ADD and data.get("amount") is None:
            raise serializers.ValidationError(
                "Amount is required when type_operation is add"
            )
        return data

    def validate_amount(self, amount):
        if amount < Decimal("0.00"):
            raise serializers.ValidationError(
                "Amount must to be greater than 0.00"
            )
        return amount


class OrderViewValidator(serializers.Serializer):
    slot_id = serializers.UUIDField(required=True)
    user_id = serializers.UUIDField(required=True)

    def to_dto(self) -> OrderOperationDto:
        return OrderOperationDto(
            user_id=self.validated_data["user_id"],
            slot_id=self.validated_data["slot_id"],
        )
