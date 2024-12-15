from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('', views.login_view, name='login'),
    path('seller-register/', views.seller_register, name='seller_register'),
    path('add-product/', views.add_product, name='add_product'),
    path('product-list/', views.product_list, name='product_list'),
    path('seller-profile/', views.seller_profile, name='seller_profile'),
    path('seller/update/', views.seller_update, name='seller_update'),
]
