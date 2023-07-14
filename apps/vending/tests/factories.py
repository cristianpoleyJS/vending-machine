from _decimal import Decimal
from datetime import datetime
from factory import Faker, SubFactory
from factory.django import DjangoModelFactory
from apps.vending.models import Product, VendingMachineSlot, User


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    id = Faker("uuid4")
    name = "Snickers Bar"
    description = "Delicious chocolate bar with peanuts"
    price = Decimal("10.40")
    created_at = datetime(2023, 5, 30, 12)
    updated_at = datetime(2023, 5, 30, 23)


class VendingMachineSlotFactory(DjangoModelFactory):
    class Meta:
        model = VendingMachineSlot

    id = Faker("uuid4")
    product = SubFactory(ProductFactory)
    quantity = 10
    row = 1
    column = 1


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    name = "Joan Pradels"
    balance = Decimal("10.40")
    created_at = datetime(2023, 5, 30, 12)
