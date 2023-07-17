from uuid import UUID

from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import serializers

from apps.vending.models import VendingMachineSlot, Product, User
from apps.vending.serializers import VendingMachineSlotSerializer, ProductSerializer, UserSerializer
from apps.vending.validators import ListSlotsValidator

from drf_spectacular.utils import extend_schema, inline_serializer


class VendingMachineSlotView(APIView):

    def get(self, request: Request) -> Response:
        validator = ListSlotsValidator(data=request.query_params)
        validator.is_valid(raise_exception=True)
        filters = {}
        if quantity := validator.validated_data["quantity"]:
            filters["quantity__lte"] = quantity

        slots = VendingMachineSlot.objects.filter(**filters)
        slots_serializer = VendingMachineSlotSerializer(slots, many=True)
        return Response(data=slots_serializer.data)


class VendingMachineSlotDetailView(APIView):

    def get(self, request, id: UUID) -> Response:
        slot = VendingMachineSlot.objects.get(id=id)
        slot_serializer = VendingMachineSlotSerializer(slot)
        return Response(data=slot_serializer.data)


class LoginView(APIView):

    @extend_schema(
        request=inline_serializer(
            name="LoginInlineSerializer",
            fields={
                "name": serializers.CharField()
            },
        ),
    )
    def post(self, request):
        try:
            name = request.data["name"].lower()
            user = User.objects.get(name=name)
            user_serializer = UserSerializer(user)
            return Response(data=user_serializer.data)
        except User.DoesNotExist:
            new_user = User.objects.update_or_create(name=name, balance=0.00)
            return Response(data=new_user)


class ProductView(APIView):

    def get(self, request) -> Response:
        slots = VendingMachineSlot.objects.order_by("row", "column")
        slots_serializer = VendingMachineSlotSerializer(
            slots, many=True)
        result = []
        for slot in slots_serializer.data:
            product = Product.objects.get(id=slot["product"]["id"])
            product_serializer = ProductSerializer(product)
            if len(result) < slot["row"]:
                result.append([product_serializer.data])
            else:
                result[slot["row"] - 1].append(product_serializer.data)
        return Response(data=result)


class BalanceView(APIView):

    @extend_schema(
        request=inline_serializer(
            name="BalanceInlineSerializer",
            fields={
                "user_id": serializers.UUIDField(),
                "type_operation": serializers.ChoiceField(
                    choices=["add", "refund"]),
                "amount": serializers.DecimalField(
                    max_digits=4, decimal_places=2, default=0.00)
            },
        ),
    )
    def post(self, request) -> Response:
        try:
            user = User.objects.get(id=request.data["user_id"])
            if request.data["type_operation"] == "refund":
                new_user = User.objects.update_or_create(
                    id=user.id,
                    defaults={
                        "name": user.name,
                        "balance": user.balance - int(request.data["amount"])
                    }
                )
                return Response(data=new_user)
            new_user = User.objects.update_or_create(
                id=user.id,
                defaults={
                    "name": user.name,
                    "balance": user.balance + int(request.data["amount"])
                }
            )
            return Response(data=new_user)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class OrderView(APIView):

    @extend_schema(
        request=inline_serializer(
            name="OrderViewInSerializer",
            fields={
                "user_id": serializers.UUIDField(),
                "product_id": serializers.UUIDField(),
            },
        ),
    )
    def post(self, request) -> Response:
        try:
            user = User.objects.get(id=request.data["user_id"])
            product = Product.objects.get(id=request.data["product_id"])
            new_user = User.objects.update(
                id=user.id,
                defaults={
                    "name": user.name,
                    "balance": user.balance - int(product["price"])
                }
            )
            Product.objects.update(
                id=product.id,
                defaults={
                    "name": product.name,
                    "description": product.description,
                    "price": product.price,
                    "quantity": product.quantity - 1
                }
            )
            return Response(data={
                "balance": new_user.balance,
            })
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
