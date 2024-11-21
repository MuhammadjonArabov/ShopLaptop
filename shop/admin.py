from django.contrib import admin
from .models import Seller, Product, Customer, Cart, Order, OrderProduct, Review, Wishlist, Category, Payment

@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'created_at', 'updated_at')
    search_fields = ('full_name', 'phone')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'status', 'created_at', 'updated_at')
    search_fields = ('name', 'comment')
    list_filter = ('status',)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'created_at', 'updated_at')
    search_fields = ('full_name', 'phone')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('customer', 'product', 'quantity', 'all_sum', 'created_at', 'updated_at')
    search_fields = ('customer__full_name', 'product__name')
    list_filter = ('customer',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'total_amount', 'created_at', 'updated_at')
    search_fields = ('customer__full_name',)
    list_filter = ('customer',)

@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')
    search_fields = ('order__id', 'product__name')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'customer', 'rating', 'created_at', 'updated_at')
    search_fields = ('product__name', 'customer__full_name')

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('customer', 'created_at', 'updated_at')
    search_fields = ('customer__full_name',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'amount', 'payment_date', 'payment_method')
    search_fields = ('order__id', 'payment_method')