from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .models import Order, OrderItem, Product


def _get_cart(session):
    return session.setdefault('cart', {})


def _cart_items(cart):
    products = Product.objects.filter(id__in=cart.keys())
    items = []
    total = Decimal('0.00')
    for product in products:
        quantity = cart.get(str(product.id), 0)
        line_total = product.price * quantity
        total += line_total
        items.append({
            'product': product,
            'quantity': quantity,
            'line_total': line_total,
        })
    return items, total


def product_list(request):
    query = request.GET.get('q', '').strip()
    category = request.GET.get('category', '').strip()

    products = Product.objects.all().order_by('-created_at')
    if query:
        products = products.filter(Q(name__icontains=query) | Q(brand__icontains=query))
    if category:
        products = products.filter(category=category)

    context = {
        'products': products,
        'query': query,
        'selected_category': category,
        'categories': Product.CATEGORY_CHOICES,
    }
    return render(request, 'shop/product_list.html', context)


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = _get_cart(request.session)
    key = str(product.id)
    cart[key] = cart.get(key, 0) + 1
    request.session.modified = True
    messages.success(request, f'Added {product.name} to cart.')
    return redirect('product_list')


@login_required
def remove_from_cart(request, product_id):
    cart = _get_cart(request.session)
    key = str(product_id)
    if key in cart:
        del cart[key]
        request.session.modified = True
    return redirect('cart')


@login_required
def cart_view(request):
    cart = _get_cart(request.session)
    items, total = _cart_items(cart)
    return render(request, 'shop/cart.html', {'items': items, 'total': total})


@login_required
def checkout(request):
    cart = _get_cart(request.session)
    items, total = _cart_items(cart)
    if not items:
        messages.warning(request, 'Your cart is empty.')
        return redirect('product_list')

    if request.method == 'POST':
        name = request.POST.get('customer_name', '').strip()
        email = request.POST.get('customer_email', '').strip() or request.user.email
        address = request.POST.get('shipping_address', '').strip()

        if not all([name, email, address]):
            messages.error(request, 'Please fill in all checkout fields.')
            return render(
                request,
                'shop/checkout.html',
                {'items': items, 'total': total, 'form_data': request.POST},
            )

        with transaction.atomic():
            order = Order.objects.create(
                customer_name=name,
                customer_email=email,
                shipping_address=address,
                total=total,
                status=Order.STATUS_PENDING,
            )
            for item in items:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    quantity=item['quantity'],
                    unit_price=item['product'].price,
                )

        request.session['cart'] = {}
        request.session.modified = True
        return redirect('order_success', order_id=order.id)

    form_data = {
        'customer_name': request.user.get_full_name() or request.user.username,
        'customer_email': request.user.email,
    }
    return render(request, 'shop/checkout.html', {'items': items, 'total': total, 'form_data': form_data})


@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'shop/order_success.html', {'order': order})
