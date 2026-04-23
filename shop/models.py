from django.contrib.auth.models import User
from django.db import models


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('TV', 'TV'),
        ('Laptop', 'Laptop'),
        ('Mobile', 'Mobile'),
        ('Fridge', 'Fridge'),
        ('Accessories', 'Accessories'),
    ]

    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=120)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image = models.URLField(blank=True, help_text='Optional image URL')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} ({self.brand})'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return f'{self.user.username} - {self.phone}'


class Order(models.Model):
    STATUS_PENDING = 'Pending'
    STATUS_PAID = 'Paid'
    STATUS_DISPATCHED = 'Dispatched'
    STATUS_DELIVERED = 'Delivered'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_PAID, 'Paid'),
        (STATUS_DISPATCHED, 'Dispatched'),
        (STATUS_DELIVERED, 'Delivered'),
    ]

    customer_name = models.CharField(max_length=120)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=30, blank=True)
    shipping_address = models.TextField()
    customer_note = models.TextField(blank=True)
    payment_reference = models.CharField(max_length=120, blank=True)
    payment_submitted = models.BooleanField(default=False)
    payment_verified = models.BooleanField(default=False)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order #{self.pk} - {self.customer_name}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def line_total(self):
        return self.quantity * self.unit_price

    def __str__(self):
        return f'{self.product.name} x {self.quantity}'


class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    subject = models.CharField(max_length=150)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.subject} - {self.name}'
