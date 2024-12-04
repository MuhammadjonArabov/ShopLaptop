from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category
from .forms import ProductForm

def product_list(request):
    products = Product.objects.filter(status=True)
    return render(request, 'products/product_list.html', {'products': products})

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            # Login qilgan foydalanuvchi seller sifatida qo'shiladi
            product = form.save(commit=False)
            product.seller = request.user.seller_profile  # Seller profilini bog'lash
            product.save()
            return redirect('product_list')
    else:
        form = ProductForm()

    categories = Category.objects.all()  # Barcha kategoriyalarni olish
    return render(request, 'products/add_product.html', {'form': form, 'categories': categories})