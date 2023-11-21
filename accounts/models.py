from django.contrib.auth.models import AbstractBaseUser
from django.db import models

from shop.models import Product
from .managers import UserManager


class User(AbstractBaseUser):
    name = models.CharField(max_length=255)
    family = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=255, unique=True, db_index=True)
    age = models.PositiveIntegerField(null=True)
    register_date = models.DateTimeField(auto_now_add=True)
    card_number = models.CharField(max_length=200, unique=True, null=True, blank=True)
    address = models.TextField(max_length=1000)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    # every thing that added in username_field should be __ unique = true
    USERNAME_FIELD = 'phone_number'

    # every thing that added in required-fields only use in createsuperuser
    REQUIRED_FIELDS = ['email', 'name']

    def __str__(self):
        return self.name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    def full_name(self, name, family):
        full_name = f'{name} + " " + {family}'
        return full_name


class OtpCode(models.Model):
    phone_number = models.CharField(max_length=11, unique=True)
    code = models.PositiveSmallIntegerField()
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.phone_number} - {self.code} - {self.created}'


