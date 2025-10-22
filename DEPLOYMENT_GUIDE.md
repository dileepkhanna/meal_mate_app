# Meal Mate - Deployment Guide

## 🚀 Free Deployment Options

### 1. **Railway** (Recommended - Easiest)
Railway offers free hosting with automatic deployments from GitHub.

**Steps:**
1. Push your code to GitHub
2. Go to [Railway.app](https://railway.app)
3. Sign up with GitHub
4. Click "New Project" → "Deploy from GitHub repo"
5. Select your repository
6. Railway will automatically detect Django and deploy

**Environment Variables to set in Railway:**
```
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=*.railway.app
```

### 2. **Render** (Great Alternative)
Render provides free static site hosting and web services.

**Steps:**
1. Push code to GitHub
2. Go to [Render.com](https://render.com)
3. Create account and connect GitHub
4. Create "New Web Service"
5. Select your repository
6. Use these settings:
   - Build Command: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
   - Start Command: `gunicorn meal_mate.wsgi:application`

**Environment Variables for Render:**
```
DEBUG=False
SECRET_KEY=your-secret-key-here
PYTHON_VERSION=3.10.0
```

### 3. **PythonAnywhere** (Free Tier Available)
Good for Django applications with easy setup.

**Steps:**
1. Sign up at [PythonAnywhere.com](https://pythonanywhere.com)
2. Upload your code via Files tab
3. Create a new web app (Django)
4. Configure WSGI file
5. Install requirements in console

### 4. **Heroku** (Free tier discontinued but still popular)
If you have access to Heroku credits:

**Steps:**
1. Install Heroku CLI
2. Create `Procfile`: `web: gunicorn meal_mate.wsgi`
3. Add `gunicorn` to requirements.txt
4. Deploy: `heroku create your-app-name && git push heroku main`

## 📋 Pre-Deployment Checklist

### 1. Update Settings for Production
Create a `production_settings.py`:

```python
from .settings import *
import os

DEBUG = False
ALLOWED_HOSTS = ['*']  # Update with your domain

# Security settings
SECURE_SSL_REDIRECT = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

### 2. Add Required Dependencies
Add to `requirements.txt`:
```
gunicorn==21.2.0
whitenoise==6.6.0
```

### 3. Update Settings.py
```python
# Add to MIDDLEWARE (at the top)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add this
    # ... rest of middleware
]

# Static files configuration
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
```

### 4. Create Procfile (for Heroku/Railway)
```
web: gunicorn meal_mate.wsgi:application
release: python manage.py migrate
```

## 🔧 Local Development Setup

1. **Clone and Setup:**
```bash
git clone <your-repo>
cd meal-mate
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

2. **Database Setup:**
```bash
python manage.py migrate
python manage.py createsuperuser
```

3. **Run Development Server:**
```bash
python manage.py runserver
```

## 🎨 Features Implemented

### ✅ Modern UI/UX Improvements
- **Responsive Design**: Mobile-friendly layout
- **Modern Color Scheme**: Purple gradient theme
- **Card-based Layout**: Clean, modern cards for restaurants and menu items
- **Font Awesome Icons**: Beautiful icons throughout the app
- **Smooth Animations**: Fade-in effects and hover animations
- **Better Typography**: Improved fonts and spacing

### ✅ Security Fixes
- **Password Hashing**: Proper Django authentication system
- **CSRF Protection**: All forms protected
- **Input Validation**: Form validation and error handling
- **SQLite Database**: Easier deployment (no MySQL dependency)

### ✅ User Experience
- **Navigation Bar**: Consistent navigation across all pages
- **Success Messages**: User feedback for actions
- **Error Handling**: Proper error pages and messages
- **Cart Management**: Improved cart with quantity controls
- **Order Confirmation**: Beautiful order success page

### ✅ Admin Features
- **Admin Dashboard**: Clean admin interface
- **Restaurant Management**: Add/edit/delete restaurants
- **Menu Management**: Manage menu items

## 🔐 Default Admin Credentials
- **Username**: admin
- **Password**: admin
- **Email**: admin@mealmate.com

## 🎯 Recommended Deployment: Railway

Railway is the easiest option:
1. Push to GitHub
2. Connect Railway to your repo
3. Deploy automatically
4. Get a free `.railway.app` domain

**Total time: ~5 minutes!**

## 📱 Mobile Responsive
The app is now fully responsive and works great on:
- 📱 Mobile phones
- 📱 Tablets  
- 💻 Desktop computers

## 🎨 Color Scheme
- **Primary**: Purple gradient (#667eea to #764ba2)
- **Secondary**: Pink gradient (#f093fb to #f5576c)
- **Success**: Blue gradient (#4facfe to #00f2fe)
- **Background**: Purple gradient
- **Cards**: Clean white with shadows

Enjoy your modern, beautiful food delivery app! 🍕🚀