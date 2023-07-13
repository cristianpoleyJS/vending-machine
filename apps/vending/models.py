from django.db import models
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal


class Product(models.Model):
    class Meta:
        db_table = "product"

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4(), editable=False)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000, default="")
    price = models.DecimalField(max_digits=4, decimal_places=2, validators=[
                                MinValueValidator(Decimal("0.00"))])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)


class VendingMachineSlot(models.Model):
    class Meta:
        db_table = "vending_machine_slot"

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4(), editable=False)
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    quantity = models.IntegerField(
        validators=[MaxValueValidator(100), MinValueValidator(0)])
    row = models.IntegerField(
        validators=[MaxValueValidator(10), MinValueValidator(1)])
    column = models.IntegerField(
        validators=[MaxValueValidator(10), MinValueValidator(1)])


class User(models.Model):
    class Meta:
        db_table = "user"

    name = models.CharField(max_length=200, primary_key=True, editable=False)
    balance = models.DecimalField(max_digits=4, decimal_places=2, validators=[
                                  MinValueValidator(Decimal("0.00"))])
    created_at = models.DateTimeField(auto_now_add=True)
