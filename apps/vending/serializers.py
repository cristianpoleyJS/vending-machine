from rest_framework import serializers


class ProductSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()
    description = serializers.CharField()
    price = serializers.DecimalField(max_digits=4, decimal_places=2)


class VendingMachineSlotSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    quantity = serializers.IntegerField()
    row = serializers.IntegerField()
    column = serializers.IntegerField()
    product = ProductSerializer()


class UserSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()
    balance = serializers.DecimalField(
        max_digits=4, decimal_places=2, default=0.00)
