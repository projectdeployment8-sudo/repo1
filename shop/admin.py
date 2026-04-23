from django.contrib import admin

from .models import ContactMessage, Order, OrderItem, Product, UserProfile


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'category', 'price', 'stock', 'created_at')
    list_filter = ('category', 'brand')
    search_fields = ('name', 'brand')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone')
    search_fields = ('user__username', 'user__email', 'phone')


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'customer_name',
        'customer_email',
        'customer_phone',
        'total',
        'payment_submitted',
        'payment_verified',
        'status',
        'created_at',
    )
    list_filter = ('status', 'payment_submitted', 'payment_verified', 'created_at')
    search_fields = ('customer_name', 'customer_email', 'payment_reference')
    inlines = [OrderItemInline]


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'subject', 'created_at')
    search_fields = ('name', 'email', 'subject')
    list_filter = ('created_at',)
