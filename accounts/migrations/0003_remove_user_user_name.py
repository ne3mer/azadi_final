# Generated by Django 4.1.7 on 2023-02-20 15:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_otpcode"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="user_name",
        ),
    ]
