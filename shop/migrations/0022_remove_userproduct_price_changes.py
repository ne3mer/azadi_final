# Generated by Django 4.1.7 on 2023-03-01 08:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0021_userproduct_price_changes"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="userproduct",
            name="price_changes",
        ),
    ]
