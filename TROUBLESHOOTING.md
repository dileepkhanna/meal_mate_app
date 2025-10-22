# 🔧 Troubleshooting Guide

## ✅ Issue Fixed: WhiteNoise Module Error

**Error**: `ModuleNotFoundError: No module named 'whitenoise'`

**Solution**: 
```bash
pip install whitenoise gunicorn
```

This has been fixed and the server is now running successfully!

## Common Issues & Solutions

### 1. Server Won't Start

**Problem**: Server fails to start or shows errors

**Solutions**:
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Check for migration issues
python manage.py makemigrations
python manage.py migrate

# Clear Python cache
python manage.py clean_pyc
```

### 2. Static Files Not Loading

**Problem**: CSS/Images not displaying

**Solutions**:
```bash
# Collect static files
python manage.py collectstatic --noinput

# Check settings.py has:
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
```

### 3. Database Errors

**Problem**: Database migration errors

**Solutions**:
```bash
# Delete database and start fresh
del db.sqlite3

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Load sample data
python create_sample_data.py
```

### 4. Login Issues

**Problem**: Can't login with admin credentials

**Solutions**:
```bash
# Create new superuser
python manage.py createsuperuser --username admin --email admin@mealmate.com

# Use password: admin (or your chosen password)
```

### 5. Template Errors

**Problem**: Template not found or rendering errors

**Solutions**:
- Check that templates are in `delivery/templates/delivery/`
- Verify `APP_DIRS: True` in settings.py TEMPLATES
- Clear browser cache (Ctrl+Shift+R)

### 6. Port Already in Use

**Problem**: Port 8000 is already in use

**Solutions**:
```bash
# Use different port
python manage.py runserver 8080

# Or kill the process using port 8000
# Windows:
netstat -ano | findstr :8000
taskkill /PID <process_id> /F
```

### 7. CSS Not Updating

**Problem**: CSS changes not reflecting

**Solutions**:
```bash
# Hard refresh browser
Ctrl + Shift + R (Windows/Linux)
Cmd + Shift + R (Mac)

# Collect static files again
python manage.py collectstatic --noinput --clear
```

### 8. Import Errors

**Problem**: Module import errors

**Solutions**:
```bash
# Verify virtual environment is activated
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Reinstall requirements
pip install -r requirements.txt
```

### 9. CSRF Token Errors

**Problem**: CSRF verification failed

**Solutions**:
- Ensure `{% csrf_token %}` is in all forms
- Check MIDDLEWARE includes CsrfViewMiddleware
- Clear browser cookies

### 10. Payment Integration Issues

**Problem**: Razorpay not working

**Solutions**:
- Update Razorpay keys in settings.py:
```python
RAZORPAY_KEY_ID = "your_test_key"
RAZORPAY_KEY_SECRET = "your_test_secret"
```
- Get test keys from: https://dashboard.razorpay.com/

## Quick Health Check

Run these commands to verify everything is working:

```bash
# 1. Check Python version (should be 3.8+)
python --version

# 2. Check Django installation
python -m django --version

# 3. Check for errors
python manage.py check

# 4. Test database connection
python manage.py dbshell
.exit

# 5. List installed packages
pip list

# 6. Run tests (if any)
python manage.py test
```

## Development Server Commands

```bash
# Start server
python manage.py runserver

# Start on different port
python manage.py runserver 8080

# Start on all interfaces (for network access)
python manage.py runserver 0.0.0.0:8000

# Stop server
Ctrl + C
```

## Database Commands

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Open database shell
python manage.py dbshell

# Show migrations
python manage.py showmigrations
```

## Useful Django Commands

```bash
# Check for problems
python manage.py check

# Collect static files
python manage.py collectstatic

# Clear sessions
python manage.py clearsessions

# Create app
python manage.py startapp app_name

# Django shell
python manage.py shell
```

## Browser Issues

### Clear Cache
- **Chrome**: Ctrl+Shift+Delete → Clear browsing data
- **Firefox**: Ctrl+Shift+Delete → Clear recent history
- **Edge**: Ctrl+Shift+Delete → Clear browsing data

### Hard Refresh
- **Windows**: Ctrl+Shift+R or Ctrl+F5
- **Mac**: Cmd+Shift+R

### Disable Cache (DevTools)
1. Open DevTools (F12)
2. Go to Network tab
3. Check "Disable cache"

## Getting Help

If you're still experiencing issues:

1. **Check the error message**: Read the full error in terminal
2. **Check browser console**: F12 → Console tab
3. **Check Django logs**: Look at terminal output
4. **Search the error**: Google the specific error message
5. **Django documentation**: https://docs.djangoproject.com/

## Current Status

✅ **Server Running**: http://127.0.0.1:8000/
✅ **No Errors**: All systems operational
✅ **Database**: Connected and migrated
✅ **Static Files**: Loading correctly
✅ **Authentication**: Working properly

**Your website is working perfectly! 🎉**

If you encounter any new issues, check this guide first!