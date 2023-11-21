# Generated by Django 4.1.7 on 2023-02-21 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0005_userproduct_date_added_userproduct_date_updated"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userproduct",
            name="date_added",
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name="userproduct",
            name="date_updated",
            field=models.DateTimeField(auto_now=True),
        ),
    ]