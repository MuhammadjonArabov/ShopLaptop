from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('seller_register/', views.seller_register, name='seller_register'),
    path('', views.index, name='index'),
]
