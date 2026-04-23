from django.urls import path

from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('signup/', views.signup, name='signup'),
    path('contact/', views.contact, name='contact'),
    path('staff-login/', views.staff_login, name='staff_login'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-success/<int:order_id>/', views.order_success, name='order_success'),
    path('verify-payment/<int:order_id>/', views.verify_payment, name='verify_payment'),
]
