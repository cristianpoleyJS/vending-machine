from django.db.utils import IntegrityError
import pytest
from decimal import Decimal, InvalidOperation
from apps.vending.models import Product, VendingMachineSlot, User
from apps.vending.tests.factories import ProductFactory, VendingMachineSlotFactory, UserFactory
from django.core.exceptions import ValidationError


@pytest.mark.django_db
class TestProductModel:

    @pytest.mark.parametrize(
        "name,price,description",
        [
            ("Ramon de pitis", "4.99", None),
            ("Mariano Delgado", "0.00", None),
            ("Sin animo de lucro", "2.99", "de algeciras")
        ],
        ids=["with_name_and_price", "price_0", "with_description"]
    )
    def test_product_creation(self, name: str, price: Decimal, description: str):
        test_product = ProductFactory(
            name=name, price=Decimal(price), description=description)

        stored_product = Product.objects.get(id=test_product.id)

        assert stored_product.price == Decimal(price)
        assert stored_product.name == name
        assert stored_product.description == description

    @pytest.mark.parametrize(
        "name,price,description,expected_error",
        [
            (None, "1.95",  None, IntegrityError),
            ("Mariano Delgado", None, None, TypeError),
            ("Ramon de Pitis", "199999", None, InvalidOperation),
            ("Sin animo de lucro", None, 44, TypeError)
        ],
        ids=["without_name", "without_price",
             "without_big_price", "wrong_description"]
    )
    def test_product_creation_fail(self, name: str, price: Decimal, description: str, expected_error: Exception):
        with pytest.raises(expected_error):
            ProductFactory(
                name=name, price=Decimal(price), description=description)


@pytest.fixture
def product_fixture():
    return ProductFactory(name="Joan Pradels")


@pytest.mark.django_db
class TestVendingMachineSlotModel:

    @pytest.mark.parametrize(
        "quantity,row,column",
        [
            (10, 1, 1),
            (0, 10, 10),
            (1, 5, 5)

        ],
        ids=["with_quantity", "with_row_and_column", "with_all"]
    )
    def test_vending_machine_slot_creation(self, quantity, row, column, product_fixture):
        test_vending_machine_slot = VendingMachineSlotFactory(
            product=product_fixture, quantity=quantity, row=row, column=column)

        stored_vending_machine_slot = VendingMachineSlot.objects.get(
            id=test_vending_machine_slot.id)

        assert stored_vending_machine_slot.quantity == quantity
        assert stored_vending_machine_slot.row == row
        assert stored_vending_machine_slot.column == column
        assert str(stored_vending_machine_slot.product.id) == product_fixture.id

    @pytest.mark.parametrize(
        "quantity,row,column,expected_error",
        [
            (None, 1, 1, IntegrityError),
            (10, None, 1, IntegrityError),
            (10, 1, None, IntegrityError),
        ],
        ids=["without_quantity", "without_row", "without_column",]
    )
    def test_vending_machine_slot_creation_fail(self, quantity, row, column, expected_error, product_fixture):
        with pytest.raises(expected_error):
            VendingMachineSlotFactory(
                product=product_fixture, quantity=quantity, row=row, column=column)


@pytest.mark.django_db
class TestUserModel:

    def test_user_creation(self):
        test_user = UserFactory(
            name="Cristian", balance="15")

        stored_user = User.objects.get(name=test_user.name)

        assert stored_user.name == "Cristian"
        assert stored_user.balance == Decimal("15")
