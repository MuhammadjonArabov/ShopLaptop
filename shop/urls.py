from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('', views.login_view, name='login'),
    path('seller_register/', views.seller_register, name='seller_register'),
]
