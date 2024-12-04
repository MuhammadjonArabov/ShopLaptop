from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category
from .forms import ProductForm

def product_list(request):
    products = Product.objects.filter(status=True)
    return render(request, 'products/product_list.html', {'products': products})

def add_product(request):
    if request.method == "POST":
        name = request.POST['name']
        price = request.POST['price']
        quantity = request.POST['quantity']
        comment = request.POST.get('comment', '')
        images = request.FILES.get('images')
        category_id = request.POST['category']
        category = get_object_or_404(Category, id=category_id)

        product = Product.objects.create(
            name=name,
            price=price,
            quantity=quantity,
            comment=comment,
            images=images,
            category=category,
            status=False
        )
        return redirect('product_list')

    categories = Category.objects.all()  # Barcha kategoriyalarni olish
    return render(request, 'products/add_product.html', {'categories': categories})