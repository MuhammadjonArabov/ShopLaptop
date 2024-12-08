from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import User, Seller, Customer


def register_user(request, user_type='customer'):
    if request.method == "POST":
        full_name = request.POST['full_name']
        phone = request.POST['phone']
        password = request.POST['password']

        if User.objects.filter(phone=phone).exists():
            error_msg = 'Bu telefon raqami allaqachon ro‘yxatdan o‘tgan.'
            template = 'products/seller_register.html' if user_type == 'seller' else 'products/register.html'
            return render(request, template, {'error': error_msg})

        user = User.objects.create_user(full_name=full_name, phone=phone, password=password,
                                        is_seller=(user_type == 'seller'))
        if user_type == 'seller':
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
    return register_user(request, user_type='seller')
