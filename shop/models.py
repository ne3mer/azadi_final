from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

from accounts.models import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, unique=True)
    image = models.ImageField(upload_to='products')
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    in_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    added_date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    description = models.TextField()
    price_history = models.ManyToManyField('PriceChange', blank=True, related_name='products')

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('accounts:price_change', args=[self.slug])


class UserProduct(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    is_for_sale = models.BooleanField(default=False)
    initial_price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f'{self.user.name} - {self.product.name}'

    def save(self, *args, **kwargs):
        if not self.pk:  # new instance
            self.initial_price = self.product.price
        super().save(*args, **kwargs)


class PriceChange(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    old_price = models.DecimalField(max_digits=6, decimal_places=2, editable=False)
    new_price = models.DecimalField(max_digits=6, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.product.name} - {self.created_at.date()}'

    def save(self, *args, **kwargs):
        if not self.pk:  # if the PriceChange is being created (not updated)
            self.old_price = self.product.price  # get the current price of the product
        super().save(*args, **kwargs)  # call the parent save method
        self.products.add(self.product)


class ProductLocation(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return f'{self.product.name} - ({self.latitude}, {self.longitude})'


@receiver(post_save, sender=PriceChange)
def update_product_price(sender, instance, created, **kwargs):
    if not created:  # if the PriceChange was updated (not created)
        instance.product.price = instance.new_price
        instance.product.save()
