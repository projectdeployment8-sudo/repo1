# Electronics E-commerce Website (Django)

A Django-based electronics e-commerce project with attractive landing page, product browsing, cart and checkout, signup/login, and admin operations.

## Features
- User signup with phone number.
- User login using username, email, or phone number.
- Separate admin login link (`/staff-login/`) not shown in main navbar.
- Product listing with category filter and search by name/brand.
- Stock support for products (visible/editable by admins).
- Session-based shopping cart.
- Checkout flow with detailed customer info and QR payment reference submission.
- Payment verification flag for admins.
- Contact page available after login.
- Admin dashboard to manage products, orders, stock, and contact messages.

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
- Contact Page: http://127.0.0.1:8000/contact/ (login required)
- Admin Panel: http://127.0.0.1:8000/admin/
