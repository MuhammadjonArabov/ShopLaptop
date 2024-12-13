from unicodedata import category

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import User, Seller, Customer, Category, Product


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
        return redirect('index')

    template = 'products/seller_register.html' if user_type == 'seller' else 'products/register.html'
    return render(request, template)



def login_view(request):
    if request.method == "POST":
        phone = request.POST['phone']
        password = request.POST['password']
        user = authenticate(request, phone=phone, password=password)

        if user:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'products/login.html', {'error': 'Telefon yoki parol noto‘g‘ri.'})

    return render(request, 'products/login.html')


@login_required
def index(request):
    return render(request, 'products/index.html', {'user': request.user})


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
        return redirect('index')

    return render(request, 'products/seller_register.html')
@login_required
def add_product(request):
    if not hasattr(request.user, 'seller'):
        return redirect('index')

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

        return redirect('index')

    return render(request, 'products/add_product.html', {'categories': categories})


def product_list(request):
        products = Product.objects.filter(status=True)
        context = {
            'products': products
        }
        return render(request, 'products/product_list.html', context)

