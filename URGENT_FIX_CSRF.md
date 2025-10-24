# 🚨 URGENT FIX - CSRF Trusted Origins Error

## The Error You're Seeing:
```
Forbidden (Origin checking failed - https://web-production-9d6bf.up.railway.app 
does not match any trusted origins.)
```

## ✅ Quick Fix (2 Minutes)

### Method 1: Via Railway Dashboard (EASIEST)

1. **Go to Railway Dashboard:**
   - Visit: https://railway.app/dashboard
   - Click on your project

2. **Click on "Variables" tab**

3. **Add New Variable:**
   - Click "+ New Variable" button
   - Variable Name: `CSRF_TRUSTED_ORIGINS`
   - Variable Value: `https://web-production-9d6bf.up.railway.app`
   - Click "Add"

4. **Railway will automatically redeploy**
   - Wait 1-2 minutes for redeployment

5. **Test Again:**
   - Go to: https://web-production-9d6bf.up.railway.app/signup/
   - Try to sign up
   - Should work now! ✅

---

### Method 2: Via Railway CLI

```bash
# Open Railway shell
railway shell

# Set the variable
export CSRF_TRUSTED_ORIGINS="https://web-production-9d6bf.up.railway.app"

# Exit
exit
```

Then redeploy from dashboard.

---

### Method 3: Update via Railway Project Settings

1. Go to your Railway project
2. Click on your service
3. Go to "Settings" tab
4. Scroll to "Environment Variables"
5. Add:
   ```
   CSRF_TRUSTED_ORIGINS=https://web-production-9d6bf.up.railway.app
   ```

---

## 🔍 Verify It's Set

After adding the variable:

1. **Check variables:**
   ```bash
   railway variables
   ```
   
   Should show:
   ```
   CSRF_TRUSTED_ORIGINS=https://web-production-9d6bf.up.railway.app
   ```

2. **Check logs:**
   ```bash
   railway logs
   ```
   
   Should show successful restart

3. **Test the site:**
   - Visit: https://web-production-9d6bf.up.railway.app/signup/
   - Fill the form
   - Click "Create Account"
   - Should work! ✅

---

## 📋 All Required Environment Variables

Make sure ALL of these are set in Railway:

| Variable | Value |
|----------|-------|
| `SECRET_KEY` | (your generated secret key) |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `web-production-9d6bf.up.railway.app` |
| `CSRF_TRUSTED_ORIGINS` | `https://web-production-9d6bf.up.railway.app` |
| `RAZORPAY_KEY_ID` | (your Razorpay key) |
| `RAZORPAY_KEY_SECRET` | (your Razorpay secret) |

**Note:** `CSRF_TRUSTED_ORIGINS` must include `https://` prefix!

---

## 🎯 Step-by-Step Visual Guide

### Step 1: Railway Dashboard
![Railway Dashboard](https://railway.app/dashboard)

### Step 2: Select Your Project
Click on: `meal-mate` or your project name

### Step 3: Variables Tab
Click on: `Variables` (in the left sidebar or top menu)

### Step 4: Add Variable
```
Name:  CSRF_TRUSTED_ORIGINS
Value: https://web-production-9d6bf.up.railway.app
```

### Step 5: Save
Click "Add" or "Save"

### Step 6: Wait for Redeploy
Railway will automatically redeploy (1-2 minutes)

### Step 7: Test
Visit your site and try signup/signin

---

## ✅ Success Indicators

After fixing, you should see:

1. **No more "Forbidden" errors** ✅
2. **Sign up works** ✅
3. **Sign in works** ✅
4. **Forms submit successfully** ✅

---

## 🐛 If Still Not Working

### Check 1: Verify the URL is Correct
Make sure you used:
```
https://web-production-9d6bf.up.railway.app
```

NOT:
```
http://web-production-9d6bf.up.railway.app  ❌ (missing 's' in https)
web-production-9d6bf.up.railway.app         ❌ (missing https://)
```

### Check 2: Check for Typos
The variable name must be EXACTLY:
```
CSRF_TRUSTED_ORIGINS
```

NOT:
```
CSRF_TRUSTED_ORIGIN   ❌ (missing 'S')
csrf_trusted_origins  ❌ (lowercase)
```

### Check 3: Restart Deployment
If you added the variable but it's still not working:

1. Go to Railway Dashboard
2. Click "Deployments"
3. Click "Redeploy" on the latest deployment

---

## 🎉 After It Works

Once signup/signin works, test these:

1. **Sign Up:**
   - Create a new account ✅

2. **Sign In:**
   - Login with your account ✅

3. **Browse Restaurants:**
   - View restaurant list ✅

4. **Add to Cart:**
   - Add items to cart ✅

5. **Checkout:**
   - Complete checkout process ✅

---

## 📞 Quick Help

If you're still stuck, run this and share the output:

```bash
# Check if variable is set
railway variables | grep CSRF

# Check logs for errors
railway logs --lines 50 | grep -i csrf

# Check deployment status
railway status
```

---

## 💡 Why This Happened

Django's CSRF protection checks if the request origin matches trusted origins. In production (Railway), you must explicitly add your domain to `CSRF_TRUSTED_ORIGINS`.

Your `settings.py` already has the code to read this variable:
```python
CSRF_TRUSTED_ORIGINS = os.environ.get('CSRF_TRUSTED_ORIGINS', '').split(',')
```

You just need to set it in Railway! 🚀

---

**This should fix your issue in 2 minutes!** ✅
