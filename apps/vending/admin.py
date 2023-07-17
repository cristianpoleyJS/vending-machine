from django.contrib import admin
from apps.vending.models import Product, User, VendingMachineSlot


class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "description",
                    "created_at", "updated_at", "id"]
    ordering = ["-created_at"]


class VendingMachineSlotAdmin(admin.ModelAdmin):
    list_display = ["product", "quantity", "row", "column"]
    ordering = ["-row", "-column"]


class UserAdmin(admin.ModelAdmin):
    list_display = ["name", "balance", "created_at", "id"]
    ordering = ["-created_at"]


admin.site.register(Product, ProductAdmin)
admin.site.register(VendingMachineSlot, VendingMachineSlotAdmin)
admin.site.register(User, UserAdmin)
