# Generated by Django 4.2.2 on 2023-07-14 11:49

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('vending', '0007_alter_product_id_alter_vendingmachineslot_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.CharField(blank=True, default=None, max_length=1000),
        ),
        migrations.AlterField(
            model_name='product',
            name='id',
            field=models.UUIDField(default=uuid.UUID('fd51f55d-1972-480e-97e9-daf5248bdfbd'), editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='vendingmachineslot',
            name='id',
            field=models.UUIDField(default=uuid.UUID('0909a34b-cdcd-4025-a6e8-ea43d3b624ce'), editable=False, primary_key=True, serialize=False),
        ),
    ]
