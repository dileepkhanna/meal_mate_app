# Railway Deployment Debugging Guide

## 🔍 How to Check Logs and Find Errors

### Step 1: View Railway Logs

**Option A: Via Railway Dashboard**
1. Go to https://railway.app/dashboard
2. Click on your project
3. Click on "Deployments" tab
4. Click on the latest deployment
5. Click "View Logs"
6. Look for ERROR messages in red

**Option B: Via Railway CLI**
```bash
# Install Railway CLI if not installed
npm install -g @railway/cli

# Login
railway login

# Link to your project
railway link

# View logs
railway logs

# Follow logs in real-time
railway logs --follow

# View more lines
railway logs --lines 500
```

### Step 2: Common Error Patterns

Look for these in your logs:

#### Error 1: ModuleNotFoundError
```
ModuleNotFoundError: No module named 'delivery'
```
**Fix:** Check INSTALLED_APPS in settings.py

#### Error 2: ImproperlyConfigured
```
django.core.exceptions.ImproperlyConfigured: SECRET_KEY
```
**Fix:** Set SECRET_KEY in Railway environment variables

#### Error 3: Static Files Error
```
ValueError: Missing staticfiles manifest entry
```
**Fix:** Run collectstatic command

#### Error 4: Database Error
```
django.db.utils.OperationalError: no such table
```
**Fix:** Run migrations

#### Error 5: ALLOWED_HOSTS Error
```
Invalid HTTP_HOST header: 'web-production-9d6bf.up.railway.app'
```
**Fix:** Add domain to ALLOWED_HOSTS

---

## 🔧 Common Fixes

### Fix 1: Set All Environment Variables

Run these commands in Railway CLI:
```bash
# Generate new SECRET_KEY
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Set variables (replace with your values)
railway variables set SECRET_KEY="your-generated-secret-key"
railway variables set DEBUG="False"
railway variables set ALLOWED_HOSTS="web-production-9d6bf.up.railway.app"
railway variables set CSRF_TRUSTED_ORIGINS="https://web-production-9d6bf.up.railway.app"
railway variables set RAZORPAY_KEY_ID="your_razorpay_key"
railway variables set RAZORPAY_KEY_SECRET="your_razorpay_secret"
```

### Fix 2: Run Migrations
```bash
railway run python manage.py migrate
```

### Fix 3: Collect Static Files
```bash
railway run python manage.py collectstatic --noinput
```

### Fix 4: Check Django Configuration
```bash
railway run python manage.py check --deploy
```

---

## 🚨 Emergency Fixes

### If Site Shows "Application Error"

**Step 1: Check if gunicorn is running**
```bash
railway logs | grep gunicorn
```

**Step 2: Verify Python version**
```bash
railway run python --version
```
Should show: Python 3.10.9

**Step 3: Test Django locally**
```bash
railway run python manage.py check
```

### If Getting 500 Internal Server Error

**Step 1: Enable DEBUG temporarily**
```bash
railway variables set DEBUG="True"
```

**Step 2: Visit site and see detailed error**

**Step 3: Fix the error**

**Step 4: Disable DEBUG**
```bash
railway variables set DEBUG="False"
```

### If Static Files Not Loading

**Option 1: Force collect**
```bash
railway run python manage.py collectstatic --noinput --clear
```

**Option 2: Check WhiteNoise**
Verify in settings.py:
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Must be here
    ...
]
```

---

## 📋 Deployment Checklist

### Before Deployment:
- [ ] All code committed to git
- [ ] requirements.txt updated
- [ ] Procfile exists
- [ ] railway.json exists
- [ ] runtime.txt exists
- [ ] settings.py uses environment variables

### After Deployment:
- [ ] Environment variables set in Railway
- [ ] Migrations run
- [ ] Static files collected
- [ ] Superuser created
- [ ] Sample data added (optional)

---

## 🔍 Specific Error Solutions

### Error: "No module named 'delivery'"

**Cause:** Django can't find your app

**Fix:**
1. Check INSTALLED_APPS in settings.py:
```python
INSTALLED_APPS = [
    ...
    'delivery.apps.DeliveryConfig',  # Should be here
]
```

2. Verify directory structure:
```
meal_mate/
├── delivery/
│   ├── __init__.py
│   ├── apps.py
│   └── ...
├── meal_mate/
│   ├── settings.py
│   └── ...
└── manage.py
```

### Error: "SECRET_KEY not set"

**Fix:**
```bash
# Generate key
python generate_secret_key.py

# Set in Railway
railway variables set SECRET_KEY="your-key-here"
```

### Error: "Invalid HTTP_HOST"

**Fix:**
```bash
railway variables set ALLOWED_HOSTS="web-production-9d6bf.up.railway.app"
```

### Error: "CSRF verification failed"

**Fix:**
```bash
railway variables set CSRF_TRUSTED_ORIGINS="https://web-production-9d6bf.up.railway.app"
```

### Error: "Static files not found"

**Fix:**
```bash
# Collect static files
railway run python manage.py collectstatic --noinput

# Verify STATIC_ROOT in settings.py
STATIC_ROOT = BASE_DIR / 'staticfiles'
```

### Error: "Database table doesn't exist"

**Fix:**
```bash
# Run migrations
railway run python manage.py migrate

# If that fails, try:
railway run python manage.py migrate --run-syncdb
```

---

## 🧪 Testing Commands

### Test if Django works:
```bash
railway run python manage.py check
```

### Test if database works:
```bash
railway run python manage.py showmigrations
```

### Test if static files work:
```bash
railway run python manage.py findstatic delivery/css/style.css
```

### Test if gunicorn works:
```bash
railway run gunicorn meal_mate.wsgi:application --bind 0.0.0.0:8000
```

---

## 📊 Monitoring

### Check Deployment Status:
```bash
railway status
```

### Check Service Health:
```bash
railway service
```

### View All Variables:
```bash
railway variables
```

---

## 🆘 Get Help

### 1. Share Your Logs
```bash
# Save logs to file
railway logs --lines 500 > railway_logs.txt
```

### 2. Check Railway Status
Visit: https://railway.statuspage.io/

### 3. Railway Discord
Join: https://discord.gg/railway

---

## ✅ Verification Steps

After fixing, verify:

1. **Logs show no errors:**
```bash
railway logs | grep -i error
```

2. **Site loads:**
Visit: https://web-production-9d6bf.up.railway.app/

3. **Static files work:**
Check if CSS is applied

4. **Database works:**
Try to sign up/sign in

5. **All features work:**
Test cart, checkout, etc.

---

## 🎯 Quick Diagnosis

Run this command to get a quick overview:
```bash
echo "=== Railway Status ===" && \
railway status && \
echo "\n=== Environment Variables ===" && \
railway variables && \
echo "\n=== Recent Logs ===" && \
railway logs --lines 50
```

---

## 📝 Report Template

If you need help, provide:

```
**Issue:** [Describe the problem]

**URL:** https://web-production-9d6bf.up.railway.app/

**Error Message:** [Copy from logs]

**Environment Variables Set:**
- SECRET_KEY: ✅ / ❌
- DEBUG: ✅ / ❌
- ALLOWED_HOSTS: ✅ / ❌
- CSRF_TRUSTED_ORIGINS: ✅ / ❌

**Commands Run:**
- migrate: ✅ / ❌
- collectstatic: ✅ / ❌

**Logs:** [Paste relevant logs]
```

---

**Need immediate help? Run these commands and share the output:**

```bash
railway logs --lines 100
railway variables
railway status
```
