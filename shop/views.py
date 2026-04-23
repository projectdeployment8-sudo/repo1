from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ContactForm, SignupForm
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
        items.append(
            {
                'product': product,
                'quantity': quantity,
                'line_total': line_total,
            }
        )
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


def signup(request):
    if request.user.is_authenticated:
        return redirect('product_list')

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully. You are now logged in.')
            return redirect('product_list')
    else:
        form = SignupForm()

    return render(request, 'registration/signup.html', {'form': form})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thanks for contacting us. We received your details.')
            return redirect('contact')
    else:
        initial = {}
        if request.user.is_authenticated:
            initial = {
                'name': request.user.get_full_name() or request.user.username,
                'email': request.user.email,
            }
        form = ContactForm(initial=initial)

    return render(request, 'shop/contact.html', {'form': form})


def staff_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('/admin/')

    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        if user.is_staff:
            login(request, user)
            return redirect('/admin/')
        messages.error(request, 'This login is for admin/staff only.')
    return render(request, 'registration/staff_login.html', {'form': form})


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if product.stock <= 0:
        messages.error(request, f'{product.name} is out of stock.')
        return redirect('product_list')

    cart = _get_cart(request.session)
    key = str(product.id)
    if cart.get(key, 0) >= product.stock:
        messages.warning(request, 'Cannot add more than available stock.')
        return redirect('product_list')

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
        phone = request.POST.get('customer_phone', '').strip()
        address = request.POST.get('shipping_address', '').strip()
        note = request.POST.get('customer_note', '').strip()
        payment_reference = request.POST.get('payment_reference', '').strip()
        payment_submitted = request.POST.get('payment_submitted') == 'on'

        if not all([name, email, phone, address, payment_reference]) or not payment_submitted:
            messages.error(request, 'Please complete all checkout fields and confirm QR payment submission.')
            return render(
                request,
                'shop/checkout.html',
                {'items': items, 'total': total, 'form_data': request.POST},
            )

        with transaction.atomic():
            for item in items:
                if item['quantity'] > item['product'].stock:
                    messages.error(request, f'Not enough stock for {item["product"].name}.')
                    return redirect('cart')

            order = Order.objects.create(
                customer_name=name,
                customer_email=email,
                customer_phone=phone,
                shipping_address=address,
                customer_note=note,
                payment_reference=payment_reference,
                payment_submitted=True,
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
                item['product'].stock -= item['quantity']
                item['product'].save(update_fields=['stock'])

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


@login_required
@user_passes_test(lambda u: u.is_staff)
def verify_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.payment_verified = True
    order.status = Order.STATUS_PAID
    order.save(update_fields=['payment_verified', 'status'])
    messages.success(request, f'Payment verified for order #{order.id}.')
    return redirect('/admin/shop/order/')
