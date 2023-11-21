from django import forms
from .models import UserProduct


class UserProductForm(forms.ModelForm):
    class Meta:
        model = UserProduct
        fields = ['product', 'quantity', 'is_for_sale']


