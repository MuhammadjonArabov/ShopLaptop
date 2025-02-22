from django.http import HttpResponseForbidden, HttpResponseNotAllowed
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import SellerUpdateForm, ProductForm
from .models import User, Seller, Customer, Category, Product, Cart


def register_user(request, user_type='customer'):
    if request.method == "POST":
        full_name = request.POST['full_name']
        phone = request.POST['phone']
        password = request.POST['password']

        if User.objects.filter(phone=phone).exists():
            error_msg = 'Bu telefon raqami allaqachon ro‘yxatdan o‘tgan.'
            template = 'products/seller_register.html' if user_type == 'seller' else 'products/register.html'
            return render(request, template, {'error': error_msg})

        is_seller = user_type == 'seller'
        is_customer = not is_seller

        user = User.objects.create_user(
            full_name=full_name,
            phone=phone,
            password=password,
            is_seller=is_seller,
            is_customer=is_customer,
            is_staff=True,
        )

        if is_seller:
            Seller.objects.create(user=user)
        else:
            Customer.objects.create(user=user)

        login(request, user)
        return redirect('product_list')

    template = 'products/seller_register.html' if user_type == 'seller' else 'products/register.html'
    return render(request, template)


def login_view(request):
    if request.method == "POST":
        phone = request.POST['phone']
        password = request.POST['password']
        user = authenticate(request, phone=phone, password=password)

        if user:
            login(request, user)
            return redirect('product_list')
        else:
            return render(request, 'products/login.html', {'error': 'Telefon yoki parol noto‘g‘ri.'})

    return render(request, 'products/login.html')



def register(request):
    return register_user(request, user_type='customer')


def seller_register(request):
    if request.method == "POST":
        full_name = request.POST['full_name']
        phone = request.POST['phone']
        password = request.POST['password']
        image = request.FILES.get('image')

        if User.objects.filter(phone=phone).exists():
            error_msg = 'Bu telefon raqami allaqachon ro‘yxatdan o‘tgan.'
            return render(request, 'products/seller_register.html', {'error': error_msg})

        user = User.objects.create_user(
            full_name=full_name,
            phone=phone,
            password=password,
            is_seller=True,
            is_customer=True,
            is_staff=True,
        )

        Seller.objects.create(user=user, image=image)

        login(request, user)
        return redirect('product_list')

    return render(request, 'products/seller_register.html')


@login_required
def add_product(request):
    if not hasattr(request.user, 'seller'):
        return redirect('product_list')

    seller = request.user.seller
    categories = Category.objects.all()

    if request.method == "POST":
        name = request.POST['name']
        price = request.POST['price']
        comment = request.POST.get('comment', '')
        quantity = request.POST['quantity']
        category_id = request.POST['category']
        category = Category.objects.get(id=category_id)
        image = request.FILES.get('images', None)

        product = Product.objects.create(
            name=name,
            price=price,
            comment=comment,
            quantity=quantity,
            category=category,
            seller=seller,
            status=False
        )

        if image:
            product.images = image
        product.save()

        return redirect('product_list')

    return render(request, 'products/add_product.html', {'categories': categories})


def product_list(request):
    products = Product.objects.filter(status=True)
    context = {
        'products': products
    }
    return render(request, 'products/product_list.html', context)


@login_required
def seller_profile(request):
    if not hasattr(request.user, 'seller'):
        messages.error(request, "Siz seller emassiz!")
        return redirect('index')

    seller = request.user.seller
    products = Product.objects.filter(seller=seller, status=True)
    product_count = products.count()
    total_quantity = sum(product.quantity for product in products)

    context = {
        'seller': seller,
        'products': products,
        'product_count': product_count,
        'total_quantity': total_quantity,
    }
    return render(request, 'products/seller.html', context)


@login_required
def seller_update(request):
    if not request.user.is_seller:
        messages.error(request, "Faqat sotuvchilar o'z profillarini yangilashlari mumkin.")
        return redirect('product_list')

    seller = request.user.seller

    if request.method == 'POST':
        form = SellerUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()

            if 'image' in request.FILES:
                seller.image = request.FILES['image']
                seller.save()

            messages.success(request, 'Profil muvaffaqiyatli yangilandi..')
            return redirect('seller_profile')
    else:
        form = SellerUpdateForm(instance=request.user)

    return render(request, 'products/seller_update.html', {'form': form, 'seller': seller})


def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            if 'images' in request.FILES:
                product.images = request.FILES['images']
                product.save()
            return redirect('seller_profile')
    else:
        form = ProductForm(instance=product)

    return render(request, 'products/product_update.html', {'form': form, 'product': product})


def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk, status=True)

    if request.method == 'POST':
        product.delete()
        return redirect('seller_profile')

    return HttpResponseNotAllowed(['POST'])

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    customer = request.user.is_customer

    cart_item, created = Cart.objects.get_or_create(
        product=product,
        customer=customer,
        defaults={'quantity': 1, 'all_sum': product.price}
    )

    if not created:
        cart_item.quantity += 1
        cart_item.all_sum = cart_item.quantity * product.price
        cart_item.save()

    messages.success(request, f"{product.name} savatga qo'shildi.")
    return redirect('product_list')
