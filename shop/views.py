from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import User, Seller, Customer


def register(request):
    if request.method == "POST":
        full_name = request.POST['full_name']
        phone = request.POST['phone']
        password = request.POST['password']

        if User.objects.filter(phone=phone).exists():
            return render(request, 'products/register.html', {'error': 'Bu telefon raqami allaqachon ro‘yxatdan o‘tgan.'})

        user = User.objects.create_user(full_name=full_name, phone=phone, password=password)
        Customer.objects.create(user=user)  
        login(request, user)
        return redirect('index')

    return render(request, 'products/register.html')


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


def seller_register(request):
    if request.method == "POST":
        full_name = request.POST['full_name']
        phone = request.POST['phone']
        password = request.POST['password']

        if User.objects.filter(phone=phone).exists():
            return render(request, 'products/seller_register.html', {'error': 'Bu telefon raqami allaqachon ro‘yxatdan o‘tgan.'})

        user = User.objects.create_user(full_name=full_name, phone=phone, password=password, is_seller=True)
        Seller.objects.create(user=user)
        login(request, user)
        return redirect('index')

    return render(request, 'products/seller_register.html')


@login_required
def index(request):
    return render(request, 'products/index.html', {'user': request.user})
