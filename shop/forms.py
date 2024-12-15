from django import forms
from .models import Product, User


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'quantity', 'comment', 'images']

class SellerUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['full_name', 'phone']


    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        return phone