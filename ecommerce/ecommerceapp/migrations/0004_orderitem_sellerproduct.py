# Generated by Django 5.1.7 on 2025-04-26 04:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ecommerceapp", "0003_purchaseorder_orderitem"),
    ]

    operations = [
        migrations.AddField(
            model_name="orderitem",
            name="sellerProduct",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="ecommerceapp.seller",
            ),
            preserve_default=False,
        ),
    ]
