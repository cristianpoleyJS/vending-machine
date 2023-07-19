from decimal import Decimal
from unittest.mock import ANY

import pytest
from rest_framework import status

from apps.vending.models import Product, User, VendingMachineSlot
from apps.vending.tests.factories import ProductFactory, VendingMachineSlotFactory


@pytest.fixture
def products_list() -> list[Product]:
    return [ProductFactory(name=f"Product {i}") for i in range(1, 11)]


@pytest.fixture
def slots_grid(products_list) -> list[VendingMachineSlot]:
    """returns a grid of slots of 5x2"""
    slots = []
    for row in range(1, 3):
        for column in range(1, 6):
            slot = VendingMachineSlotFactory(
                product=products_list.pop(), row=row, column=column, quantity=column-1
            )
            slots.append(slot)
    return slots


@pytest.fixture
def products_grid(products_list) -> list[Product]:
    """returns a grid of product of 2x2"""
    result = []
    for row in range(1, 2):
        for column in range(1, 2):
            product = ProductFactory(
                product=products_list.pop(), row=row, column=column, quantity=column-1
            )
            result.append(product)
    return result


@pytest.mark.django_db
class TestLogin:

    def test_login_returns_expected_response_when_user_not_exist(self, client):
        response = client.post("/login/", {
            "name": "Juan Praderas"
        })

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["name"] == "Juan Praderas"

    def test_login_returns_expected_response_when_user_exist(self, client):
        response = client.post("/login/", {
            "name": "Juan Praderas"
        })

        assert response.status_code == status.HTTP_201_CREATED

        user = User.objects.get(id=response.json()["id"])
        user.balance = Decimal("10.40")
        user.save()

        new_response = client.post("/login/", {
            "name": user.name
        })

        assert new_response.status_code == status.HTTP_200_OK
        assert new_response.json()["name"] == "Juan Praderas"
        assert new_response.json()["balance"] == '10.40'


@pytest.mark.django_db
class TestListVendingMachineSlots:

    def test_list_slots_returns_expected_response(self, client, slots_grid):
        response = client.get("/slots/")

        expected_response = [
            {
                "id": ANY,
                "quantity": 0,
                "row": 1,
                "column": 1,
                "product": {"id": ANY, "name": "Product 10", "description": ANY, "price": "10.40"},
            },
            {
                "id": ANY,
                "quantity": 1,
                "row": 1,
                "column": 2,
                "product": {"id": ANY, "name": "Product 9", "description": ANY, "price": "10.40"},
            },
            {
                "id": ANY,
                "quantity": 2,
                "row": 1,
                "column": 3,
                "product": {"id": ANY, "name": "Product 8", "description": ANY, "price": "10.40"},
            },
            {
                "id": ANY,
                "quantity": 3,
                "row": 1,
                "column": 4,
                "product": {"id": ANY, "name": "Product 7", "description": ANY, "price": "10.40"},
            },
            {
                "id": ANY,
                "quantity": 4,
                "row": 1,
                "column": 5,
                "product": {"id": ANY, "name": "Product 6", "description": ANY, "price": "10.40"},
            },
            {
                "id": ANY,
                "quantity": 0,
                "row": 2,
                "column": 1,
                "product": {"id": ANY, "name": "Product 5", "description": ANY, "price": "10.40"},
            },
            {
                "id": ANY,
                "quantity": 1,
                "row": 2,
                "column": 2,
                "product": {"id": ANY, "name": "Product 4", "description": ANY, "price": "10.40"},
            },
            {
                "id": ANY,
                "quantity": 2,
                "row": 2,
                "column": 3,
                "product": {"id": ANY, "name": "Product 3", "description": ANY, "price": "10.40"},
            },
            {
                "id": ANY,
                "quantity": 3,
                "row": 2,
                "column": 4,
                "product": {"id": ANY, "name": "Product 2", "description": ANY, "price": "10.40"},
            },
            {
                "id": ANY,
                "quantity": 4,
                "row": 2,
                "column": 5,
                "product": {"id": ANY, "name": "Product 1", "description": ANY, "price": "10.40"},
            },
        ]

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == expected_response

    def test_invalid_quantity_filter_returns_bad_request(self, client):
        response = client.get("/slots/?quantity=-1")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {"quantity": [
            "Ensure this value is greater than or equal to 0."]}

    def test_list_slots_returns_filtered_response(self, client, slots_grid):
        response = client.get("/slots/?quantity=1")

        expected_response = [
            {
                "id": ANY,
                "quantity": 0,
                "row": 1,
                "column": 1,
                "product": {"id": ANY, "name": "Product 10", "description": ANY, "price": "10.40"},
            },
            {
                "id": ANY,
                "quantity": 1,
                "row": 1,
                "column": 2,
                "product": {"id": ANY, "name": "Product 9", "description": ANY, "price": "10.40"},
            },
            {
                "id": ANY,
                "quantity": 0,
                "row": 2,
                "column": 1,
                "product": {"id": ANY, "name": "Product 5", "description": ANY, "price": "10.40"},
            },
            {
                "id": ANY,
                "row": 2,
                "column": 2,
                "quantity": 1,
                "product": {"id": ANY, "name": "Product 4", "description": ANY, "price": "10.40"},
            },
        ]

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == expected_response


@pytest.mark.django_db
class TestListProducts:

    def test_list_products_returns_expected_response(self, client, slots_grid):
        response = client.get("/products/")

        expected_response = [
            [
                {
                    'id': ANY,
                    'name': 'Product 10',
                    'description': 'Delicious chocolate bar with peanuts',
                    'price': '10.40',
                    'quantity': 0,
                    'slot_id': ANY
                },
                {
                    'id': ANY,
                    'name': 'Product 9',
                    'description': 'Delicious chocolate bar with peanuts',
                    'price': '10.40',
                    'quantity': 1,
                    'slot_id': ANY
                },
                {
                    'id': ANY,
                    'name': 'Product 8',
                    'description': 'Delicious chocolate bar with peanuts',
                    'price': '10.40',
                    'quantity': 2,
                    'slot_id': ANY
                },
                {
                    'id': ANY,
                    'name': 'Product 7',
                    'description': 'Delicious chocolate bar with peanuts',
                    'price': '10.40',
                    'quantity': 3,
                    'slot_id': ANY
                },
                {
                    'id': ANY,
                    'name': 'Product 6',
                    'description': 'Delicious chocolate bar with peanuts',
                    'price': '10.40',
                    'quantity': 4,
                    'slot_id': ANY
                }
            ],
            [
                {
                    'id': ANY,
                    'name': 'Product 5',
                    'description': 'Delicious chocolate bar with peanuts',
                    'price': '10.40',
                    'quantity': 0,
                    'slot_id': ANY
                },
                {
                    'id': ANY,
                    'name': 'Product 4',
                    'description': 'Delicious chocolate bar with peanuts',
                    'price': '10.40',
                    'quantity': 1,
                    'slot_id': ANY
                },
                {
                    'id': ANY,
                    'name': 'Product 3',
                    'description': 'Delicious chocolate bar with peanuts',
                    'price': '10.40',
                    'quantity': 2,
                    'slot_id': ANY
                },
                {
                    'id': ANY,
                    'name': 'Product 2',
                    'description': 'Delicious chocolate bar with peanuts',
                    'price': '10.40',
                    'quantity': 3,
                    'slot_id': ANY
                },
                {
                    'id': ANY,
                    'name': 'Product 1',
                    'description': 'Delicious chocolate bar with peanuts',
                    'price': '10.40',
                    'quantity': 4,
                    'slot_id': ANY
                }
            ]
        ]

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == expected_response
