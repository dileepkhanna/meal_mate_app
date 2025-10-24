# Backend Not Working on Railway - Complete Fix Guide

## 🔍 Step 1: Run Diagnosis

Run this command and share the output:

```bash
# Windows
diagnose_railway.bat

# Mac/Linux
bash diagnose_railway.sh
```

Or run these commands one by one:

```bash
railway logs --lines 200
railway variables
railway status
```

---

## 🚨 Common Issues & Fixes

### Issue 1: Environment Variables Not Set

**Check:**
```bash
railway variables
```

**Should show:**
```
SECRET_KEY=...
DEBUG=False
ALLOWED_HOSTS=web-production-9d6bf.up.railway.app
CSRF_TRUSTED_ORIGINS=https://web-production-9d6bf.up.railway.app
RAZORPAY_KEY_ID=...
RAZORPAY_KEY_SECRET=...
```

**Fix if missing:**
Go to Railway Dashboard → Variables → Add each one

---

### Issue 2: Migrations Not Run

**Check:**
```bash
railway run python manage.py showmigrations
```

**Fix:**
```bash
railway run python manage.py migrate
```

---

### Issue 3: Static Files Not Collected

**Check logs for:**
```
ValueError: Missing staticfiles manifest
```

**Fix:**
```bash
railway run python manage.py collectstatic --noinput --clear
```

---

### Issue 4: Wrong Python Version

**Check:**
```bash
railway run python --version
```

**Should show:** Python 3.10.x

**Fix:** Verify `runtime.txt` contains:
```
python-3.10.9
```

---

### Issue 5: Gunicorn Not Starting

**Check logs for:**
```
Error: No module named 'gunicorn'
```

**Fix:** Verify `requirements.txt` has:
```
gunicorn==21.2.0
```

---

### Issue 6: Database Not Initialized

**Check:**
```bash
railway run python manage.py dbshell
```

**Fix:**
```bash
railway run python manage.py migrate --run-syncdb
```

---

## 🔧 Nuclear Option: Complete Reset

If nothing works, do a complete reset:

### Step 1: Clear Everything
```bash
# In Railway Dashboard
# Delete all environment variables
# Delete the service
# Create new service
```

### Step 2: Set Variables Fresh
```bash
# Generate new SECRET_KEY
python generate_secret_key.py

# In Railway Dashboard → Variables, add:
SECRET_KEY=(new generated key)
DEBUG=False
ALLOWED_HOSTS=web-production-9d6bf.up.railway.app
CSRF_TRUSTED_ORIGINS=https://web-production-9d6bf.up.railway.app
RAZORPAY_KEY_ID=(your key)
RAZORPAY_KEY_SECRET=(your secret)
```

### Step 3: Deploy Fresh
```bash
# Push to GitHub
git add .
git commit -m "Fresh deployment"
git push origin main

# Railway will auto-deploy
```

### Step 4: Run Setup Commands
```bash
railway run python manage.py migrate
railway run python manage.py collectstatic --noinput
railway run python manage.py createsuperuser
```

---

## 📊 Debugging Checklist

Run through this checklist:

### Local Environment
- [ ] `python manage.py check` works locally
- [ ] `python manage.py runserver` works locally
- [ ] All tests pass locally
- [ ] Static files load locally

### Railway Configuration
- [ ] `Procfile` exists and is correct
- [ ] `railway.json` exists
- [ ] `runtime.txt` exists with Python 3.10.9
- [ ] `requirements.txt` has all dependencies

### Railway Environment
- [ ] All 6 environment variables are set
- [ ] Variables have correct values (no typos)
- [ ] `CSRF_TRUSTED_ORIGINS` includes `https://`
- [ ] `ALLOWED_HOSTS` does NOT include `https://`

### Railway Deployment
- [ ] Latest deployment shows "Success"
- [ ] Logs show "Starting gunicorn"
- [ ] Logs show "Listening at: http://..."
- [ ] No ERROR messages in logs

### Database
- [ ] Migrations have run
- [ ] Tables exist
- [ ] Can create superuser

### Static Files
- [ ] `collectstatic` has run
- [ ] CSS files are accessible
- [ ] Images load correctly

---

## 🎯 Specific Error Solutions

### Error: "Application Error"

**Cause:** Gunicorn failed to start

**Check logs:**
```bash
railway logs | grep -i error
```

**Common causes:**
1. Missing environment variables
2. Syntax error in code
3. Import error
4. Database connection failed

**Fix:**
1. Check all variables are set
2. Run `python manage.py check` locally
3. Check logs for specific error
4. Fix the error and redeploy

---

### Error: "502 Bad Gateway"

**Cause:** Server not responding

**Fix:**
```bash
# Check if service is running
railway status

# Restart service
# Railway Dashboard → Redeploy
```

---

### Error: "500 Internal Server Error"

**Cause:** Django error

**Fix:**
```bash
# Temporarily enable DEBUG
railway variables
# Add: DEBUG=True

# Visit site to see detailed error
# Fix the error
# Set DEBUG=False again
```

---

### Error: "Static files not loading"

**Cause:** collectstatic not run or WhiteNoise issue

**Fix:**
```bash
# Collect static files
railway run python manage.py collectstatic --noinput --clear

# Verify WhiteNoise in settings.py
# MIDDLEWARE should have:
# 'whitenoise.middleware.WhiteNoiseMiddleware',
```

---

## 📞 Get Help

If you're still stuck, provide this information:

### 1. Railway Logs
```bash
railway logs --lines 200 > logs.txt
```

### 2. Environment Variables
```bash
railway variables > variables.txt
```

### 3. Deployment Status
```bash
railway status > status.txt
```

### 4. Django Check
```bash
railway run python manage.py check > check.txt
```

### 5. Error Message
Copy the exact error message you see

---

## 🎬 Video Tutorial Steps

### Step 1: Open Railway Dashboard
1. Go to https://railway.app/dashboard
2. Click on your project
3. Look at the deployment status

### Step 2: Check Logs
1. Click "Deployments"
2. Click latest deployment
3. Click "View Logs"
4. Look for ERROR messages (in red)

### Step 3: Check Variables
1. Click "Variables" tab
2. Verify all 6 variables are set
3. Check for typos

### Step 4: Run Commands
1. Open terminal
2. Run: `railway logs`
3. Look for errors
4. Fix errors one by one

---

## ✅ Success Indicators

Your backend is working when:

1. **Logs show:**
   ```
   [INFO] Starting gunicorn
   [INFO] Listening at: http://0.0.0.0:XXXX
   [INFO] Booting worker
   ```

2. **Site loads:**
   - Homepage displays
   - CSS is applied
   - No errors

3. **Forms work:**
   - Sign up works
   - Sign in works
   - No CSRF errors

4. **Features work:**
   - Can browse restaurants
   - Can add to cart
   - Can checkout

---

## 🚀 Quick Commands Reference

```bash
# View logs
railway logs

# View more logs
railway logs --lines 500

# Follow logs in real-time
railway logs --follow

# Check status
railway status

# Check variables
railway variables

# Run Django command
railway run python manage.py <command>

# Run migrations
railway run python manage.py migrate

# Collect static files
railway run python manage.py collectstatic --noinput

# Create superuser
railway run python manage.py createsuperuser

# Django check
railway run python manage.py check

# Django check for deployment
railway run python manage.py check --deploy
```

---

**Run the diagnosis script and share the output so I can help you fix the specific issue!** 🔍
