from decimal import Decimal
from uuid import UUID

from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import serializers
from apps.vending.exceptions import OrderError, UserNotFound, VendingMachineSlotNotFound

from apps.vending.models import VendingMachineSlot, User
from apps.vending.serializers import VendingMachineSlotSerializer, UserSerializer
from apps.vending.services import BalanceOperatorService, OrderOperatorService
from apps.vending.validators import ListSlotsValidator, LoginValidator, OrderViewValidator, BalanceViewValidator

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
    def post(self, request: Request) -> Response:
        validator = LoginValidator(data=request.data)
        validator.is_valid(raise_exception=True)
        name = validator.validated_data["name"]
        user, created = User.objects.get_or_create(
            name__iexact=name, defaults={"name": name})
        user_serializer = UserSerializer(user)
        return Response(data=user_serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


class ProductView(APIView):

    def get(self, request: Request) -> Response:
        slots = VendingMachineSlot.objects.order_by("row", "column")
        slots_serializer = VendingMachineSlotSerializer(
            slots, many=True)
        result = []
        for slot in slots_serializer.data:
            new_product = {
                **slot["product"],
                "quantity": slot["quantity"],
                "slot_id": slot["id"]
            }
            if len(result) < slot["row"]:
                result.append([new_product])
            else:
                result[slot["row"] - 1].append(new_product)
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
        validator = BalanceViewValidator(data=request.data)
        validator.is_valid(raise_exception=True)
        dto = validator.to_dto()
        service = BalanceOperatorService()
        try:
            user = service.execute(dto)
        except UserNotFound as e:
            return Response(status=status.HTTP_404_NOT_FOUND, data={"message": str(e)},)
        user_serializer = UserSerializer(user)
        return Response(data=user_serializer.data)


class OrderView(APIView):

    @extend_schema(
        request=inline_serializer(
            name="OrderViewInSerializer",
            fields={
                "user_id": serializers.UUIDField(),
                "slot_id": serializers.UUIDField(),
            },
        ),
    )
    def post(self, request) -> Response:
        validator = OrderViewValidator(data=request.data)
        validator.is_valid(raise_exception=True)
        dto = validator.to_dto()
        service = OrderOperatorService()
        try:
            user = service.execute(dto)
        except UserNotFound as e:
            return Response(status=status.HTTP_404_NOT_FOUND, data={"message": str(e)})
        except VendingMachineSlotNotFound as e:
            return Response(status=status.HTTP_404_NOT_FOUND, data={"message": str(e)})
        except OrderError as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": str(e)})
        user_serializer = UserSerializer(user)
        return Response(data=user_serializer.data)
