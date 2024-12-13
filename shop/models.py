from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
import re
from django.core.exceptions import ValidationError


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True


def validate_phone(value):
    pattern = r'^\+998[0-9]{9}$'
    if not re.match(pattern, value):
        raise ValidationError(f"{value} noto'g'ri telefon raqami formatida.")



class CustomerUserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError("Telefon no'mer ta'lab qilinadi!")
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(phone, password, **extra_fields)

class User(AbstractUser):
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_groups',
        blank=True
    )
    username = None
    phone = models.CharField(max_length=13, unique=True, validators=[validate_phone])
    full_name = models.CharField(max_length=250)
    is_seller = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []
    objects = CustomerUserManager()



class Seller(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seller')
    images = models.ImageField(upload_to='seller_images/', blank=True, null=True)

    def __str__(self):
        return self.user.full_name


class Customer(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer')

    def __str__(self):
        return self.user.full_name



class Category(BaseModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name



class Product(BaseModel):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    comment = models.TextField(blank=True)
    quantity = models.IntegerField()
    seller = models.ForeignKey(Seller, related_name='products', on_delete=models.CASCADE)  
    category = models.ForeignKey(Category, related_name='category', on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    images = models.ImageField(upload_to='product_images/', blank=True, null=True)

    def __str__(self):
        return self.name





class Cart(BaseModel):
    product = models.ForeignKey(Product, related_name='carts', on_delete=models.SET_NULL, null=True)
    customer = models.ForeignKey(Customer, related_name='carts', on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()
    all_sum = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Cart of {self.customer} for {self.product}'



class Order(BaseModel):
    customer = models.ForeignKey(Customer, related_name='orders', on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderProduct')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Order {self.id} by {self.customer}'


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, related_name='order_products', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_products', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.quantity} of {self.product.name} in Order {self.order.id}'


class Review(BaseModel):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, related_name='reviews', on_delete=models.CASCADE)
    rating = models.IntegerField()  # 1 dan 5 gacha
    comment = models.TextField(blank=True)

    def __str__(self):
        return f'Review for {self.product.name} by {self.customer.full_name}'



class Wishlist(BaseModel):
    customer = models.ForeignKey(Customer, related_name='wishlists', on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, related_name='wishlists')

    def __str__(self):
        return f'Wishlist of {self.customer.full_name}'


class Payment(BaseModel):
    order = models.ForeignKey(Order, related_name='payments', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50)

    def __str__(self):
        return f'Payment of {self.amount} for Order {self.order.id}'
