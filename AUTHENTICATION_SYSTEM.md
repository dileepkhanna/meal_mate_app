# Authentication System - Meal Mate

## Overview
The Meal Mate application now has **completely separated authentication systems** for customers and administrators.

---

## 🔐 Customer Authentication

### Database Model
- **Model**: `Customer` (extends Django's AbstractUser)
- **Table**: Custom customer table (delivery_customer)
- **Fields**: username, password, email, mobile, address
- **Flags**: `is_staff=False`, `is_superuser=False`

### Customer URLs
- **Sign Up**: `/signup/`
- **Sign In**: `/signin/`
- **Submit Sign Up**: `/signup/submit/`
- **Submit Login**: `/login/`

### Customer Features
- Mobile number field
- Delivery address field
- Shopping cart functionality
- Order placement
- Restaurant browsing

### Customer Access
- Can only access customer pages
- Cannot access admin panel
- Redirected if trying to use admin login

---

## 👨‍💼 Admin Authentication

### Database Model
- **Model**: `Customer` (same model, different flags)
- **Table**: Same customer table (delivery_customer)
- **Fields**: username, password, email, mobile (empty), address (empty)
- **Flags**: `is_staff=True`, `is_superuser=False`

### Admin URLs
- **Sign Up**: `/admin1/signup/`
- **Sign In**: `/admin1/signin/`
- **Submit Sign Up**: `/admin1/signup/submit/`
- **Submit Login**: `/admin1/login/`

### Admin Features
- **Access Code Required**: `ADMIN2024` (configurable in views.py)
- Restaurant management
- Menu management
- No shopping cart
- No order placement

### Admin Access
- Can only access admin panel
- Cannot access customer features
- Requires staff privileges

---

## 🔒 Security Features

### 1. **Separate Credentials**
- Both stored in `Customer` model
- Differentiated by `is_staff` flag
- Customers: `is_staff=False`
- Admins: `is_staff=True`

### 2. **Access Code Protection**
- Admin signup requires secret access code
- Code: `ADMIN2024` (change in `views.py` line ~115)
- Prevents unauthorized admin registration

### 3. **Role-Based Access Control**
- Customer login checks: `not is_staff and not is_superuser`
- Admin login checks: `is_staff or is_superuser`
- Cross-login attempts are blocked

### 4. **Duplicate Prevention**
- Checks both User and Customer tables for duplicates
- Prevents username/email conflicts
- Clear error messages

---

## 📝 How It Works

### Customer Registration Flow
1. User fills signup form at `/signup/`
2. System checks for duplicates in Customer table
3. Creates Customer with `is_staff=False`
4. Redirects to customer signin

### Customer Login Flow
1. User enters credentials at `/signin/`
2. System looks up in Customer table
3. Verifies user is NOT staff
4. Logs in and redirects to customer home

### Admin Registration Flow
1. Admin fills signup form at `/admin1/signup/`
2. System verifies admin access code
3. Checks for duplicates in both tables
4. Creates User with `is_staff=True`
5. Redirects to admin signin

### Admin Login Flow
1. Admin enters credentials at `/admin1/signin/`
2. System authenticates against User table
3. Verifies user IS staff or superuser
4. Logs in and redirects to admin dashboard

---

## 🛠️ Configuration

### Change Admin Access Code
Edit `delivery/views.py` around line 165:
```python
ADMIN_ACCESS_CODE = "YOUR_SECURE_CODE_HERE"  # Currently set to "1425"
```

### Create First Admin (Alternative Method)
Using Django shell:
```bash
python manage.py shell
```
```python
from delivery.models import Customer
Customer.objects.create_user(
    username='admin',
    password='your_password',
    email='admin@example.com',
    mobile='',
    address='',
    is_staff=True,
    is_superuser=True
)
```

---

## 🎨 UI Differences

### Customer Pages
- Burgundy and gold theme
- Shopping cart icon
- Restaurant browsing
- Order history

### Admin Pages
- Dark blue/black theme
- Shield icon branding
- Restaurant management
- Menu management
- No cart functionality

---

## ✅ Benefits

1. **Complete Separation**: No credential mixing
2. **Enhanced Security**: Access code for admin signup
3. **Clear Roles**: Distinct permissions and features
4. **Professional**: Separate branding and UI
5. **Scalable**: Easy to add more admin features

---

## 🚀 Testing

### Test Customer Account
1. Go to `/signup/`
2. Create account (no access code needed)
3. Login at `/signin/`
4. Access customer features

### Test Admin Account
1. Go to `/admin1/signup/`
2. Enter access code: `ADMIN2024`
3. Create admin account
4. Login at `/admin1/signin/`
5. Access admin panel

---

## 📌 Important Notes

- **Never share the admin access code publicly**
- Change the default access code in production
- Admins cannot place orders (by design)
- Customers cannot access admin panel (by design)
- Both systems use Django's authentication backend
- Passwords are hashed and secure

---

## 🔄 Migration Notes

If you have existing users:
- Existing Customer accounts remain unchanged
- Create new admin accounts using admin signup
- Old "admin" username may need migration if it exists in Customer table

---

**Last Updated**: 2024
**Version**: 1.0
