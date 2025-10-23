# Railway.app Deployment Guide for Meal Mate

## Prerequisites
- Railway.app account
- GitHub repository with your code
- Railway CLI (optional)

## Step 1: Prepare Your Project

### Files Created/Updated:
- ✅ `railway.json` - Railway configuration
- ✅ `runtime.txt` - Python version specification
- ✅ `Procfile` - Process commands
- ✅ `requirements.txt` - Python dependencies
- ✅ `meal_mate/settings.py` - Updated with environment variables

## Step 2: Deploy to Railway

### Option A: Deploy via Railway Dashboard

1. **Go to Railway.app**
   - Visit https://railway.app
   - Sign in with GitHub

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your `meal-mate` repository

3. **Configure Environment Variables**
   
   Go to your project → Variables tab and add:

   ```
   SECRET_KEY=your-secret-key-here-generate-a-new-one
   DEBUG=False
   ALLOWED_HOSTS=your-app-name.up.railway.app
   CSRF_TRUSTED_ORIGINS=https://your-app-name.up.railway.app
   RAZORPAY_KEY_ID=your_razorpay_key_id
   RAZORPAY_KEY_SECRET=your_razorpay_secret
   ```

   **Generate a new SECRET_KEY:**
   ```python
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

4. **Deploy**
   - Railway will automatically detect Django and deploy
   - Wait for the build to complete
   - Your app will be available at: `https://your-app-name.up.railway.app`

### Option B: Deploy via Railway CLI

1. **Install Railway CLI**
   ```bash
   npm install -g @railway/cli
   ```

2. **Login to Railway**
   ```bash
   railway login
   ```

3. **Initialize Project**
   ```bash
   railway init
   ```

4. **Set Environment Variables**
   ```bash
   railway variables set SECRET_KEY="your-secret-key"
   railway variables set DEBUG="False"
   railway variables set ALLOWED_HOSTS="your-app-name.up.railway.app"
   railway variables set CSRF_TRUSTED_ORIGINS="https://your-app-name.up.railway.app"
   railway variables set RAZORPAY_KEY_ID="your_key"
   railway variables set RAZORPAY_KEY_SECRET="your_secret"
   ```

5. **Deploy**
   ```bash
   railway up
   ```

## Step 3: Post-Deployment

### Create Superuser (Admin Account)

1. **Via Railway Dashboard:**
   - Go to your project
   - Click on "Deployments" tab
   - Find the latest deployment
   - Click "View Logs"
   - In the top right, click "Shell" or "Terminal"
   - Run:
     ```bash
     python manage.py createsuperuser
     ```

2. **Via Railway CLI:**
   ```bash
   railway run python manage.py createsuperuser
   ```

### Add Sample Data

If you want to add restaurants and menu items:

```bash
railway run python create_sample_data.py
```

Or manually via Django admin:
- Go to `https://your-app-name.up.railway.app/admin`
- Login with superuser credentials
- Add restaurants and menu items

## Step 4: Verify Deployment

1. **Check Homepage**
   - Visit: `https://your-app-name.up.railway.app`
   - Should see the Meal Mate homepage

2. **Check Static Files**
   - CSS should be loaded properly
   - Images should display correctly

3. **Test Functionality**
   - Sign up for a new account
   - Browse restaurants
   - Add items to cart
   - Test checkout (with test Razorpay keys)

## Troubleshooting

### Issue: Static Files Not Loading

**Solution:**
```bash
railway run python manage.py collectstatic --noinput
```

### Issue: Database Not Migrated

**Solution:**
```bash
railway run python manage.py migrate
```

### Issue: 500 Internal Server Error

**Check Logs:**
```bash
railway logs
```

Common fixes:
1. Verify all environment variables are set
2. Check `ALLOWED_HOSTS` includes your Railway domain
3. Ensure `CSRF_TRUSTED_ORIGINS` is set correctly

### Issue: CSRF Verification Failed

**Solution:**
Add your Railway domain to environment variables:
```
CSRF_TRUSTED_ORIGINS=https://your-app-name.up.railway.app
```

## Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | Generate with command above |
| `DEBUG` | Debug mode | `False` for production |
| `ALLOWED_HOSTS` | Allowed domains | `your-app.up.railway.app` |
| `CSRF_TRUSTED_ORIGINS` | Trusted origins for CSRF | `https://your-app.up.railway.app` |
| `RAZORPAY_KEY_ID` | Razorpay API key | From Razorpay dashboard |
| `RAZORPAY_KEY_SECRET` | Razorpay secret | From Razorpay dashboard |

## Important Notes

1. **Database**: Railway uses SQLite by default. For production, consider upgrading to PostgreSQL:
   - Add PostgreSQL plugin in Railway dashboard
   - Update `DATABASES` in settings.py to use `DATABASE_URL` environment variable

2. **Media Files**: For user-uploaded files, consider using:
   - AWS S3
   - Cloudinary
   - Railway Volumes

3. **Custom Domain**: 
   - Go to Settings → Domains
   - Add your custom domain
   - Update `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS`

## Updating Your Deployment

### Push Changes:
```bash
git add .
git commit -m "Your commit message"
git push origin main
```

Railway will automatically redeploy when you push to your connected branch.

### Manual Redeploy:
- Go to Railway dashboard
- Click "Redeploy" button

## Support

If you encounter issues:
1. Check Railway logs: `railway logs`
2. Check Django logs in Railway dashboard
3. Verify all environment variables are set correctly
4. Ensure your domain is in `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS`

## Success! 🎉

Your Meal Mate application should now be live on Railway.app!

Visit: `https://your-app-name.up.railway.app`
