# Generated by Django 5.1.7 on 2025-04-26 04:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("ecommerceapp", "0005_purchaseorder_sellerproduct"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="orderitem",
            name="sellerProduct",
        ),
    ]
