# Fix Railway Deployment - Step by Step

## ✅ Your Local Setup is CORRECT!

All files are properly configured. The issue is likely with Railway environment variables or deployment commands.

## 🚀 Follow These Steps EXACTLY:

### Step 1: Set Environment Variables in Railway

1. Go to https://railway.app/dashboard
2. Click on your project
3. Click on "Variables" tab
4. Add these variables ONE BY ONE:

```bash
# Generate a new SECRET_KEY first
python generate_secret_key.py
# Copy the output
```

Then add these variables in Railway:

| Variable Name | Variable Value |
|---------------|----------------|
| `SECRET_KEY` | (paste the generated key) |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `web-production-9d6bf.up.railway.app` |
| `CSRF_TRUSTED_ORIGINS` | `https://web-production-9d6bf.up.railway.app` |
| `RAZORPAY_KEY_ID` | (your Razorpay test key) |
| `RAZORPAY_KEY_SECRET` | (your Razorpay secret) |

### Step 2: Install Railway CLI

```bash
npm install -g @railway/cli
```

### Step 3: Login and Link

```bash
# Login to Railway
railway login

# Link to your project
railway link
```

### Step 4: Run Deployment Commands

```bash
# 1. Run migrations
railway run python manage.py migrate

# 2. Collect static files
railway run python manage.py collectstatic --noinput

# 3. Create superuser (optional but recommended)
railway run python manage.py createsuperuser
```

### Step 5: Check Logs

```bash
railway logs
```

Look for:
- ✅ "Starting gunicorn"
- ✅ "Listening at: http://0.0.0.0:XXXX"
- ❌ Any ERROR messages

### Step 6: Test Your Site

Visit: https://web-production-9d6bf.up.railway.app/

Should see your homepage!

---

## 🐛 If Still Not Working

### Check 1: View Full Logs

```bash
railway logs --lines 500
```

Copy the ERROR messages and look for:

#### Common Error 1: "Invalid HTTP_HOST"
```
Invalid HTTP_HOST header: 'web-production-9d6bf.up.railway.app'
```

**Fix:**
```bash
railway variables set ALLOWED_HOSTS="web-production-9d6bf.up.railway.app"
```

#### Common Error 2: "No module named 'delivery'"
```
ModuleNotFoundError: No module named 'delivery'
```

**Fix:** This shouldn't happen, but if it does:
```bash
railway run python manage.py check
```

#### Common Error 3: "Static files not found"
```
ValueError: Missing staticfiles manifest entry
```

**Fix:**
```bash
railway run python manage.py collectstatic --noinput --clear
```

#### Common Error 4: "Database error"
```
django.db.utils.OperationalError: no such table
```

**Fix:**
```bash
railway run python manage.py migrate --run-syncdb
```

### Check 2: Verify Environment Variables

```bash
railway variables
```

Should show all 6 variables set.

### Check 3: Force Redeploy

In Railway Dashboard:
1. Go to Deployments
2. Click "Redeploy" on the latest deployment

---

## 📋 Quick Diagnosis Commands

Run these and share the output if you need help:

```bash
# Check status
railway status

# Check variables
railway variables

# Check logs
railway logs --lines 100

# Test Django
railway run python manage.py check --deploy
```

---

## 🎯 Expected Output

When everything works, `railway logs` should show:

```
[INFO] Starting gunicorn 21.2.0
[INFO] Listening at: http://0.0.0.0:8000
[INFO] Using worker: sync
[INFO] Booting worker with pid: 123
```

And your site should load at:
https://web-production-9d6bf.up.railway.app/

---

## 💡 Pro Tips

1. **Always check logs first:**
   ```bash
   railway logs
   ```

2. **If you see errors, fix them one by one**

3. **After fixing, redeploy:**
   - Railway Dashboard → Redeploy

4. **Test locally first:**
   ```bash
   python manage.py check --deploy
   ```

---

## 🆘 Still Stuck?

### Option 1: Share Your Logs

Run this and share the output:
```bash
railway logs --lines 200 > logs.txt
```

### Option 2: Check Railway Status

Visit: https://railway.statuspage.io/

### Option 3: Verify Your Setup

Run locally:
```bash
python check_deployment.py
```

---

## ✅ Success Checklist

- [ ] All environment variables set in Railway
- [ ] `railway run python manage.py migrate` completed
- [ ] `railway run python manage.py collectstatic --noinput` completed
- [ ] `railway logs` shows no errors
- [ ] Site loads at https://web-production-9d6bf.up.railway.app/
- [ ] CSS styles are applied
- [ ] Can sign up/sign in

---

## 🎉 Once It Works

1. Create superuser:
   ```bash
   railway run python manage.py createsuperuser
   ```

2. Add sample data:
   ```bash
   railway run python create_sample_data.py
   ```

3. Test all features:
   - Sign up
   - Sign in
   - Browse restaurants
   - Add to cart
   - Checkout

---

**Your configuration is correct. Just follow the steps above to deploy!** 🚀
