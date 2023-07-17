from uuid import UUID

from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView

from apps.vending.models import VendingMachineSlot
from apps.vending.serializers import VendingMachineSlotSerializer
from apps.vending.validators import ListSlotsValidator


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
    def get(self, request: Request, id: UUID) -> Response:
        slot = VendingMachineSlot.objects.get(id=id)
        # if we don't pass many we can send only one slot
        slot_serializer = VendingMachineSlotSerializer(slot)
        return Response(data=slot_serializer.data)
