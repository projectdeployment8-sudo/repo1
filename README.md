# Electronics E-commerce Website (Django)

A Django-based electronics e-commerce project with attractive landing page, category filtering, search, cart, checkout with QR payment confirmation, user signup/login, contact form, and admin operations.

## Features
- User signup and login.
- Separate staff/admin login route.
- Product listing with category filter and search by name/brand.
- Stock support for products (visible/editable by admins).
- Session-based shopping cart.
- Checkout flow with detailed customer info and QR payment reference submission.
- Payment verification flag for admins.
- Contact page for user queries.
- Admin dashboard to manage products, orders, stock, and contact messages.

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
- Landing/Shop: http://127.0.0.1:8000/
- User Login: http://127.0.0.1:8000/accounts/login/
- User Signup: http://127.0.0.1:8000/signup/
- Staff Login: http://127.0.0.1:8000/staff-login/
- Contact Page: http://127.0.0.1:8000/contact/
- Admin Panel: http://127.0.0.1:8000/admin/
