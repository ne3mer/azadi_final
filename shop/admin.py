from django.contrib import admin
from .models import Product, UserProduct, PriceChange, User, ProductLocation


class ProductLocationInline(admin.TabularInline):
    model = ProductLocation


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductLocationInline]


admin.site.register(Product, ProductAdmin)
admin.site.register(UserProduct)
admin.site.register(PriceChange)
admin.site.register(ProductLocation)