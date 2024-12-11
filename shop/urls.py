from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('seller-register/', views.seller_register, name='seller_register'),
    path('add-product/', views.add_product, name='add_product')
]
