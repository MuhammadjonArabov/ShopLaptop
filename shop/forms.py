from django import forms
from .models import Product, Seller


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'quantity', 'comment', 'images']

class SellerUpdateForm(forms.ModelForm):
    class Meta:
        model = Seller
        fields = ['image', 'user']