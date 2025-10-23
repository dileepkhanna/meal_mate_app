# CSRF Token "Security token expired" Fix ✅

## Problem
Getting "Security token expired. Please try again." message when clicking Sign In or Sign Up buttons.

## Root Cause
CSRF (Cross-Site Request Forgery) token issues can occur due to:
1. Expired or missing CSRF cookies
2. Browser cache issues
3. Cookie settings conflicts
4. Session expiration

## ✅ Fixes Applied

### 1. Updated Templates
**Files:** `delivery/templates/delivery/signin.html` & `signup.html`

**Changes:**
- Added JavaScript CSRF token validation
- Auto-refresh token if missing
- Better error handling
- Added autocomplete attributes for better browser compatibility

### 2. Improved CSRF Failure Handler
**File:** `delivery/views.py`

**Changes:**
- Better error messages
- Redirects to correct page (signin or signup)
- More user-friendly feedback

### 3. Enhanced CSRF Settings
**File:** `meal_mate/settings.py`

**New Settings:**
```python
CSRF_COOKIE_AGE = 31449600  # 1 year
CSRF_USE_SESSIONS = False  # Use cookies
CSRF_COOKIE_NAME = 'csrftoken'
CSRF_COOKIE_HTTPONLY = False  # Allow JavaScript access
CSRF_COOKIE_SAMESITE = 'Lax'
```

## 🔧 How to Test

### 1. Clear Browser Data
```
1. Open browser settings
2. Clear cookies and cache
3. Close and reopen browser
```

### 2. Test Sign In
```
1. Go to http://localhost:8000/signin/
2. Enter credentials
3. Click "Sign In"
4. Should work without CSRF error
```

### 3. Test Sign Up
```
1. Go to http://localhost:8000/signup/
2. Fill in the form
3. Click "Create Account"
4. Should work without CSRF error
```

## 🐛 If Issue Persists

### Solution 1: Clear Django Sessions
```bash
python manage.py clearsessions
```

### Solution 2: Delete Session Files
```bash
# Delete db.sqlite3 sessions (development only!)
python manage.py flush
```

### Solution 3: Check Browser Console
1. Open browser DevTools (F12)
2. Go to Console tab
3. Look for CSRF-related errors
4. Check if csrftoken cookie exists in Application → Cookies

### Solution 4: Try Incognito/Private Mode
- Open browser in incognito/private mode
- Test signin/signup
- If it works, clear your browser cache

### Solution 5: Check Cookie Settings
Make sure your browser allows cookies:
1. Browser Settings → Privacy
2. Enable cookies
3. Allow third-party cookies (for localhost)

## 📋 Verification Checklist

- [ ] Browser cookies are enabled
- [ ] Browser cache is cleared
- [ ] CSRF token appears in form (inspect element)
- [ ] csrftoken cookie exists (check DevTools)
- [ ] No JavaScript errors in console
- [ ] Django server is running
- [ ] Using correct URL (http://localhost:8000)

## 🔍 Debug Mode

### Check if CSRF Token Exists
Open browser console and run:
```javascript
// Check cookie
document.cookie.split(';').find(c => c.includes('csrftoken'))

// Check form token
document.querySelector('input[name="csrfmiddlewaretoken"]').value
```

Both should return values. If not, refresh the page.

## 🚀 For Production (Railway)

### Additional Settings Needed:
```python
# In Railway environment variables:
CSRF_TRUSTED_ORIGINS=https://your-app.up.railway.app
CSRF_COOKIE_SECURE=True
SESSION_COOKIE_SECURE=True
```

## ✅ Expected Behavior Now

### Sign In Page:
1. Load page → CSRF token generated
2. Fill form → Token validated
3. Submit → Success (no CSRF error)

### Sign Up Page:
1. Load page → CSRF token generated
2. Fill form → Token validated
3. Submit → Account created (no CSRF error)

### Error Handling:
- If token expires → User-friendly message
- If token missing → Auto-refresh page
- If validation fails → Clear error message

## 📝 Technical Details

### CSRF Token Flow:
```
1. User visits signin/signup page
2. Django generates CSRF token
3. Token stored in cookie (csrftoken)
4. Token embedded in form (csrfmiddlewaretoken)
5. User submits form
6. Django validates: cookie token == form token
7. If match → Process request
8. If no match → CSRF failure
```

### JavaScript Enhancement:
- Checks token before submission
- Syncs cookie and form tokens
- Alerts user if token missing
- Auto-refreshes if needed

## 🎯 Success Indicators

✅ No "Security token expired" message
✅ Forms submit successfully
✅ Users can sign in/sign up
✅ No CSRF errors in logs
✅ Cookies are set properly

## 📞 Still Having Issues?

### Check Django Logs:
```bash
# Run server with verbose output
python manage.py runserver --verbosity 3
```

### Check CSRF Middleware:
Ensure this is in `settings.py` MIDDLEWARE:
```python
'django.middleware.csrf.CsrfViewMiddleware',
```

### Verify Views:
Both signin and signup views call:
```python
from django.middleware.csrf import get_token
get_token(request)  # Ensures fresh token
```

---

## Summary

The CSRF token issue has been fixed with:
1. ✅ Enhanced JavaScript validation
2. ✅ Better error handling
3. ✅ Improved CSRF settings
4. ✅ User-friendly error messages

**The signin and signup forms should now work without CSRF errors!** 🎉
