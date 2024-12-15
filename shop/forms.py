from django import forms
from .models import Product, User


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'comment', 'quantity', 'category', 'images']


class SellerUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['full_name', 'phone']

    image = forms.ImageField(required=False)

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        return phone

