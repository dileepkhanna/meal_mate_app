# Railway Quick Command Reference

## 🚀 Essential Commands for Your Deployment

### Check Your Deployment Status
```bash
# View logs
railway logs

# Follow logs in real-time
railway logs --follow

# View last 100 lines
railway logs --lines 100
```

### Database Management
```bash
# Run migrations
railway run python manage.py migrate

# Create superuser (admin account)
railway run python manage.py createsuperuser

# Clear sessions
railway run python manage.py clearsessions

# Check database
railway run python manage.py dbshell
```

### Static Files
```bash
# Collect static files
railway run python manage.py collectstatic --noinput

# Force collect (overwrite)
railway run python manage.py collectstatic --noinput --clear
```

### Testing & Debugging
```bash
# Check for issues
railway run python manage.py check

# Check deployment settings
railway run python manage.py check --deploy

# Run Django shell
railway run python manage.py shell

# Test database connection
railway run python manage.py showmigrations
```

### Add Sample Data
```bash
# Run your sample data script
railway run python create_sample_data.py

# Or create manually via Django shell
railway run python manage.py shell
>>> from delivery.models import Restaurant, MenuItem
>>> # Create restaurants and items
```

### Environment Variables
```bash
# List all variables
railway variables

# Set a variable
railway variables set KEY=value

# Example: Set SECRET_KEY
railway variables set SECRET_KEY="your-new-secret-key"

# Set multiple variables
railway variables set DEBUG=False ALLOWED_HOSTS=web-production-9d6bf.up.railway.app
```

### Deployment
```bash
# Deploy current code
railway up

# Redeploy (from Railway dashboard or)
railway redeploy

# Link to project
railway link
```

## 🔧 Troubleshooting Commands

### If Site Shows 500 Error:
```bash
# Check logs for errors
railway logs --lines 200

# Verify migrations
railway run python manage.py showmigrations

# Run migrations if needed
railway run python manage.py migrate
```

### If Static Files Not Loading:
```bash
# Collect static files
railway run python manage.py collectstatic --noinput

# Check static files location
railway run python manage.py findstatic delivery/css/style.css
```

### If CSRF Errors:
```bash
# Set CSRF trusted origins
railway variables set CSRF_TRUSTED_ORIGINS=https://web-production-9d6bf.up.railway.app

# Clear sessions
railway run python manage.py clearsessions
```

### If Database Issues:
```bash
# Check migrations
railway run python manage.py showmigrations

# Make migrations (if needed)
railway run python manage.py makemigrations

# Apply migrations
railway run python manage.py migrate
```

## 📊 Monitoring

### Check App Status:
```bash
# View deployment status
railway status

# View service info
railway service
```

### View Environment:
```bash
# List all environment variables
railway variables

# Check specific variable
railway variables get SECRET_KEY
```

## 🎯 Quick Setup After Deployment

### 1. Set Environment Variables:
```bash
railway variables set SECRET_KEY="$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')"
railway variables set DEBUG=False
railway variables set ALLOWED_HOSTS=web-production-9d6bf.up.railway.app
railway variables set CSRF_TRUSTED_ORIGINS=https://web-production-9d6bf.up.railway.app
```

### 2. Run Migrations:
```bash
railway run python manage.py migrate
```

### 3. Collect Static Files:
```bash
railway run python manage.py collectstatic --noinput
```

### 4. Create Admin User:
```bash
railway run python manage.py createsuperuser
```

### 5. Add Sample Data:
```bash
railway run python create_sample_data.py
```

## 🔍 Testing Your Deployment

### Test Homepage:
```bash
curl https://web-production-9d6bf.up.railway.app/
```

### Test Admin:
```bash
curl https://web-production-9d6bf.up.railway.app/admin/
```

### Test API Endpoint:
```bash
curl https://web-production-9d6bf.up.railway.app/signin/
```

## 📝 Common Workflows

### Update Code and Redeploy:
```bash
# 1. Make changes locally
# 2. Commit to git
git add .
git commit -m "Your changes"
git push origin main

# 3. Railway auto-deploys
# Or manually:
railway up
```

### Check Deployment Logs:
```bash
railway logs --follow
```

### Rollback to Previous Version:
```bash
# Via Railway Dashboard:
# Deployments → Select previous deployment → Redeploy
```

## 🚨 Emergency Commands

### If Site is Down:
```bash
# 1. Check logs
railway logs --lines 500

# 2. Check status
railway status

# 3. Restart (redeploy)
railway redeploy
```

### If Database Corrupted:
```bash
# Reset migrations (DANGER: loses data!)
railway run python manage.py migrate --fake-initial

# Or start fresh
railway run python manage.py flush
```

### If Need to Reset Everything:
```bash
# Clear database
railway run python manage.py flush

# Run migrations
railway run python manage.py migrate

# Create superuser
railway run python manage.py createsuperuser

# Add data
railway run python create_sample_data.py
```

## 📚 Useful Links

- **Your App:** https://web-production-9d6bf.up.railway.app/
- **Railway Dashboard:** https://railway.app/dashboard
- **Railway Docs:** https://docs.railway.app/
- **Django Docs:** https://docs.djangoproject.com/

## 💡 Pro Tips

1. **Always check logs first:**
   ```bash
   railway logs
   ```

2. **Test locally before deploying:**
   ```bash
   python manage.py check --deploy
   ```

3. **Keep environment variables secure:**
   - Never commit them to git
   - Use Railway dashboard to manage them

4. **Monitor your app:**
   ```bash
   railway logs --follow
   ```

5. **Backup your database regularly:**
   - Use Railway's backup features
   - Or export data periodically

---

**Quick Reference Card:**
```bash
# Most Used Commands
railway logs                    # View logs
railway run python manage.py    # Run Django commands
railway variables               # Manage env vars
railway up                      # Deploy
railway status                  # Check status
```

Save this file for quick reference! 📌
