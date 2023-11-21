# Generated by Django 4.1.7 on 2023-02-20 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                ("user_name", models.CharField(max_length=255, unique=True)),
                ("name", models.CharField(max_length=255)),
                ("family", models.CharField(max_length=255)),
                ("email", models.EmailField(max_length=255, unique=True)),
                ("phone_number", models.CharField(max_length=255, unique=True)),
                ("age", models.PositiveIntegerField(null=True)),
                ("register_date", models.DateTimeField(auto_now_add=True)),
                (
                    "card_number",
                    models.CharField(
                        blank=True, max_length=200, null=True, unique=True
                    ),
                ),
                ("address", models.TextField(max_length=1000)),
                ("is_active", models.BooleanField(default=True)),
                ("is_admin", models.BooleanField(default=False)),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
