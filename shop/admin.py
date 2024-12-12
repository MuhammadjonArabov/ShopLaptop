from django.contrib import admin
from .models import Seller, Product, Customer, Cart, Order, OrderProduct, Review, Wishlist, Category, Payment, User
from django.contrib.auth.admin import UserAdmin

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Personal info', {'fields': ('full_name',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_customer', 'is_seller')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'password1', 'password2'),
        }),
    )
    list_display = ('phone', 'full_name', 'is_staff', 'is_superuser', 'is_seller', 'is_customer')
    search_fields = ('phone', 'full_name')
    ordering = ('phone',)

    def get_model_perms(self, request):
        if not request.user.is_staff:
            return {}
        return super().get_model_perms(request)


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at')
    search_fields = ('user__full_name',)
    list_filter = ('created_at',)

    def get_model_perms(self, request):
        if not request.user.is_staff:
            return {}
        return super().get_model_perms(request)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(user=request.user)
        return qs


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at')
    search_fields = ('user__full_name', 'user__phone')
    list_filter = ('created_at',)

    def get_model_perms(self, request):
        if not request.user.is_staff:
            return {}
        return super().get_model_perms(request)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(user=request.user)
        return qs


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'status', 'category', 'created_at')
    search_fields = ('name', 'comment')
    list_filter = ('status', 'category', 'sellers')
    autocomplete_fields = ('sellers', 'category')

    def get_model_perms(self, request):
        if not request.user.is_staff:
            return {}
        return super().get_model_perms(request)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(sellers=request.user)
        return qs


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)

    def get_model_perms(self, request):
        if not request.user.is_staff:
            return {}
        return super().get_model_perms(request)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('customer', 'product', 'quantity', 'all_sum', 'created_at', 'updated_at')
    search_fields = ('customer__user__full_name', 'product__name')
    list_filter = ('customer', 'created_at')

    def get_model_perms(self, request):
        if not request.user.is_staff:
            return {}
        return super().get_model_perms(request)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'total_amount', 'created_at', 'updated_at')
    search_fields = ('customer__user__full_name',)
    list_filter = ('created_at', 'customer')

    def get_model_perms(self, request):
        if not request.user.is_staff:
            return {}
        return super().get_model_perms(request)


@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price', 'order__customer')
    search_fields = ('order__id', 'product__name')
    list_filter = ('order__customer', 'product')

    def get_model_perms(self, request):
        if not request.user.is_staff:
            return {}
        return super().get_model_perms(request)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'customer', 'rating', 'created_at', 'updated_at')
    search_fields = ('product__name', 'customer__user__full_name')
    list_filter = ('rating', 'created_at')

    def get_model_perms(self, request):
        if not request.user.is_staff:
            return {}
        return super().get_model_perms(request)


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('customer', 'created_at', 'updated_at')
    search_fields = ('customer__user__full_name',)
    list_filter = ('created_at',)

    def get_model_perms(self, request):
        if not request.user.is_staff:
            return {}
        return super().get_model_perms(request)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'amount', 'payment_date', 'payment_method')
    search_fields = ('order__id', 'payment_method', 'order__customer__user__full_name')
    list_filter = ('payment_date', 'payment_method')

    def get_model_perms(self, request):
        if not request.user.is_staff:
            return {}
        return super().get_model_perms(request)
