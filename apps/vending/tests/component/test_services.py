from decimal import Decimal
import pytest
from apps.vending.enums import BalanceTypeOperation
from apps.vending.exceptions import OrderError
from apps.vending.request_dto import BalanceOperationDto, OrderOperationDto
from apps.vending.services import BalanceOperatorService, OrderOperatorService

from apps.vending.tests.factories import UserFactory, VendingMachineSlotFactory


@pytest.mark.django_db
def test_should_increase_balance_of_user():
    user = UserFactory(balance=Decimal("0.00"))
    dto = BalanceOperationDto(user_id=user.id, amount=Decimal(
        "10.00"), type_operation=BalanceTypeOperation.ADD)
    service = BalanceOperatorService()
    service.execute(dto)
    user.refresh_from_db()
    assert user.balance == Decimal("10.00")


@pytest.mark.django_db
def test_should_raise_error_if_increase_a_negative_number():
    user = UserFactory(balance=Decimal("1.00"))
    dto = BalanceOperationDto(user_id=user.id, amount=Decimal(
        "-10.00"), type_operation=BalanceTypeOperation.ADD)
    service = BalanceOperatorService()
    with pytest.raises(ValueError):
        service.execute(dto)


@pytest.mark.django_db
def test_should_raise_error_if_order_product_with_price_higher_than_balance():
    user = UserFactory(balance=Decimal("1.00"))
    slot = VendingMachineSlotFactory(product__price=Decimal("2.00"))
    dto = OrderOperationDto(user_id=user.id, slot_id=slot.id)
    service = OrderOperatorService()
    with pytest.raises(OrderError):
        service.execute(dto)


@pytest.mark.django_db
def test_should_raise_error_if_order_a_slot_with_quantity_zero():
    user = UserFactory(balance=Decimal("1.00"))
    slot = VendingMachineSlotFactory(
        product__price=Decimal("2.00"), quantity=0)
    dto = OrderOperationDto(user_id=user.id, slot_id=slot.id)
    service = OrderOperatorService()
    with pytest.raises(OrderError):
        service.execute(dto)


@pytest.mark.django_db
def test_should_decrease_quantity_and_update_user_balance_after_order_product():
    user = UserFactory(balance=Decimal("10.00"))
    slot = VendingMachineSlotFactory(
        product__price=Decimal("2.00"), quantity=5)
    dto = OrderOperationDto(user_id=user.id, slot_id=slot.id)
    service = OrderOperatorService()
    service.execute(dto)
    user.refresh_from_db()
    slot.refresh_from_db()
    assert slot.quantity == 4
    assert user.balance == Decimal("8.00")
