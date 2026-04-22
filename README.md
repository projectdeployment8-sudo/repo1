# Electronics E-commerce Website (Django)

A Django-based electronics e-commerce project with product listing, category filtering, search, shopping cart, checkout with QR placeholder, and admin order/product management.

## Features
- Product listing with category filter and search by name/brand.
- Session-based shopping cart.
- Checkout flow with QR payment placeholder.
- Order creation and success page.
- Admin dashboard to manage products and orders.

## Tech Stack
- Python
- Django
- SQLite
- HTML/CSS + Bootstrap

## Run Locally
1. Create and activate virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Apply migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
4. Create admin user:
   ```bash
   python manage.py createsuperuser
   ```
5. Start server:
   ```bash
   python manage.py runserver
   ```

Open:
- Shop: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/
