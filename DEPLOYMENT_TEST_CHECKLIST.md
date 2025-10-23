# Railway Deployment Testing Checklist
**URL:** https://web-production-9d6bf.up.railway.app/

## 🔍 Pre-Testing Setup

### 1. Verify Environment Variables in Railway
Go to Railway Dashboard → Your Project → Variables

Required variables:
- [ ] `SECRET_KEY` - Set to a secure generated key
- [ ] `DEBUG` - Set to `False`
- [ ] `ALLOWED_HOSTS` - Set to `web-production-9d6bf.up.railway.app`
- [ ] `CSRF_TRUSTED_ORIGINS` - Set to `https://web-production-9d6bf.up.railway.app`
- [ ] `RAZORPAY_KEY_ID` - Your Razorpay key
- [ ] `RAZORPAY_KEY_SECRET` - Your Razorpay secret

### 2. Check Deployment Logs
```
Railway Dashboard → Deployments → View Logs
```
Look for:
- ✅ "Migrations completed"
- ✅ "Static files collected"
- ✅ "Server started"
- ❌ No error messages

---

## 📋 Test Cases

### Test 1: Homepage Access ✅
**URL:** https://web-production-9d6bf.up.railway.app/

**Steps:**
1. Open the URL in browser
2. Check if homepage loads

**Expected Result:**
- ✅ Page loads without errors
- ✅ Meal Mate logo visible
- ✅ Navigation bar present
- ✅ CSS styles applied correctly
- ✅ No 404 or 500 errors

**If Failed:**
- Check ALLOWED_HOSTS in Railway variables
- Check static files: `railway run python manage.py collectstatic --noinput`
- Check logs for errors

---

### Test 2: Static Files (CSS/Images) ✅
**URL:** https://web-production-9d6bf.up.railway.app/static/delivery/css/style.css

**Steps:**
1. Open the static file URL
2. Check if CSS loads

**Expected Result:**
- ✅ CSS file loads
- ✅ Styles are applied on pages
- ✅ Images display correctly

**If Failed:**
```bash
# Run in Railway terminal
railway run python manage.py collectstatic --noinput
```

---

### Test 3: Sign Up Page ✅
**URL:** https://web-production-9d6bf.up.railway.app/signup/

**Steps:**
1. Navigate to signup page
2. Fill in the form:
   - Username: `testuser`
   - Password: `testpass123`
   - Email: `test@example.com`
   - Mobile: `1234567890`
   - Address: `Test Address`
3. Click "Create Account"

**Expected Result:**
- ✅ Form loads correctly
- ✅ No CSRF token errors
- ✅ Account created successfully
- ✅ Redirected to signin page
- ✅ Success message displayed

**If Failed:**
- Check CSRF_TRUSTED_ORIGINS in Railway
- Clear browser cookies
- Try in incognito mode

---

### Test 4: Sign In ✅
**URL:** https://web-production-9d6bf.up.railway.app/signin/

**Steps:**
1. Navigate to signin page
2. Enter credentials:
   - Username: `testuser`
   - Password: `testpass123`
3. Click "Sign In"

**Expected Result:**
- ✅ Form loads correctly
- ✅ No CSRF token errors
- ✅ Login successful
- ✅ Redirected to customer home
- ✅ Username displayed in navbar

**If Failed:**
- Verify user was created in Test 3
- Check CSRF settings
- Check session configuration

---

### Test 5: Admin Access ✅
**URL:** https://web-production-9d6bf.up.railway.app/admin/

**Steps:**
1. Navigate to admin page
2. Try to login

**Expected Result:**
- ✅ Admin login page loads
- ✅ Styled correctly

**Note:** You need to create a superuser first:
```bash
railway run python manage.py createsuperuser
```

---

### Test 6: Restaurant Listing ✅
**URL:** https://web-production-9d6bf.up.railway.app/customer/{username}/home/

**Steps:**
1. Sign in as a customer
2. View restaurant list

**Expected Result:**
- ✅ Restaurants displayed (if any exist)
- ✅ Restaurant cards styled correctly
- ✅ Images load properly
- ✅ Can click on restaurants

**If No Restaurants:**
- Add via admin panel
- Or run: `railway run python create_sample_data.py`

---

### Test 7: Restaurant Menu ✅
**URL:** https://web-production-9d6bf.up.railway.app/restaurants/{id}/menu/customer/{username}/

**Steps:**
1. Click on a restaurant
2. View menu items

**Expected Result:**
- ✅ Menu items displayed
- ✅ Prices visible
- ✅ "Add to Cart" buttons work
- ✅ Veg/Non-veg badges show

---

### Test 8: Add to Cart ✅

**Steps:**
1. On restaurant menu page
2. Click "Add to Cart" on an item
3. Check cart badge in navbar

**Expected Result:**
- ✅ Item added to cart
- ✅ Success message displayed
- ✅ Cart badge updates with count
- ✅ No errors

---

### Test 9: View Cart ✅
**URL:** https://web-production-9d6bf.up.railway.app/cart/{username}/

**Steps:**
1. Click on cart icon in navbar
2. View cart contents

**Expected Result:**
- ✅ Cart items displayed
- ✅ Quantities shown correctly
- ✅ Prices calculated correctly
- ✅ Total amount displayed
- ✅ Update quantity works
- ✅ Remove item works

---

### Test 10: Checkout Page ✅
**URL:** https://web-production-9d6bf.up.railway.app/checkout/{username}/

**Steps:**
1. Go to cart
2. Click "Proceed to Checkout"
3. View checkout page

**Expected Result:**
- ✅ Order summary displayed
- ✅ Items and prices correct
- ✅ Payment button visible
- ✅ Razorpay integration ready
- ✅ Page styled correctly

---

### Test 11: Order Placement ✅

**Steps:**
1. On checkout page
2. Click "Pay" button
3. Complete payment (test mode)

**Expected Result:**
- ✅ Razorpay modal opens
- ✅ Test payment works
- ✅ Order confirmed
- ✅ Redirected to order confirmation
- ✅ Cart cleared

---

### Test 12: Order Confirmation ✅
**URL:** https://web-production-9d6bf.up.railway.app/orders/{username}/

**Steps:**
1. After placing order
2. View order confirmation page

**Expected Result:**
- ✅ Order details displayed
- ✅ Order items listed
- ✅ Total amount shown
- ✅ Delivery address shown
- ✅ Success message displayed

---

### Test 13: Mobile Responsiveness 📱

**Steps:**
1. Open site on mobile device or use DevTools
2. Test all pages

**Expected Result:**
- ✅ All pages responsive
- ✅ Navigation works on mobile
- ✅ Forms usable on mobile
- ✅ Buttons clickable
- ✅ Text readable

---

### Test 14: Cross-Browser Testing 🌐

**Browsers to Test:**
- [ ] Chrome
- [ ] Firefox
- [ ] Safari
- [ ] Edge

**Expected Result:**
- ✅ Works on all browsers
- ✅ Styles consistent
- ✅ No JavaScript errors

---

### Test 15: Security Tests 🔒

**Tests:**
1. Try accessing admin without login
2. Try accessing other user's cart
3. Try SQL injection in forms
4. Check HTTPS is enforced

**Expected Result:**
- ✅ Unauthorized access blocked
- ✅ HTTPS redirect works
- ✅ CSRF protection active
- ✅ XSS protection enabled

---

## 🐛 Common Issues & Fixes

### Issue 1: 500 Internal Server Error
**Fix:**
```bash
# Check logs
railway logs

# Common causes:
# - Missing environment variables
# - Database not migrated
# - Static files not collected
```

### Issue 2: Static Files Not Loading
**Fix:**
```bash
railway run python manage.py collectstatic --noinput
```

### Issue 3: CSRF Token Errors
**Fix:**
- Add to Railway variables:
```
CSRF_TRUSTED_ORIGINS=https://web-production-9d6bf.up.railway.app
```

### Issue 4: Database Empty
**Fix:**
```bash
# Create superuser
railway run python manage.py createsuperuser

# Add sample data
railway run python create_sample_data.py
```

### Issue 5: Page Not Found (404)
**Fix:**
- Check URL patterns in urls.py
- Verify ALLOWED_HOSTS includes your domain

---

## 📊 Performance Tests

### Load Time Test
- [ ] Homepage loads in < 3 seconds
- [ ] Menu page loads in < 3 seconds
- [ ] Cart page loads in < 2 seconds

### Database Test
- [ ] Can create 100+ restaurants
- [ ] Can handle 1000+ menu items
- [ ] Cart operations are fast

---

## ✅ Final Checklist

### Functionality
- [ ] All pages load without errors
- [ ] User registration works
- [ ] User login works
- [ ] Restaurant browsing works
- [ ] Add to cart works
- [ ] Cart management works
- [ ] Checkout process works
- [ ] Order placement works

### Design
- [ ] All CSS styles applied
- [ ] Images load correctly
- [ ] Responsive on mobile
- [ ] Consistent across browsers
- [ ] Burgundy/gold color scheme

### Security
- [ ] HTTPS enabled
- [ ] CSRF protection active
- [ ] Secure cookies in production
- [ ] No sensitive data exposed
- [ ] Admin panel protected

### Performance
- [ ] Pages load quickly
- [ ] No console errors
- [ ] Database queries optimized
- [ ] Static files cached

---

## 🚀 Post-Deployment Tasks

### 1. Create Admin Account
```bash
railway run python manage.py createsuperuser
```

### 2. Add Sample Data
```bash
railway run python create_sample_data.py
```

### 3. Monitor Logs
```bash
railway logs --follow
```

### 4. Set Up Custom Domain (Optional)
- Railway Dashboard → Settings → Domains
- Add your custom domain
- Update ALLOWED_HOSTS and CSRF_TRUSTED_ORIGINS

---

## 📞 Support

### Check Logs:
```bash
railway logs
```

### Run Commands:
```bash
railway run python manage.py <command>
```

### Restart App:
- Railway Dashboard → Redeploy

---

## 🎯 Success Criteria

Your deployment is successful if:
- ✅ All 15 test cases pass
- ✅ No critical errors in logs
- ✅ Users can sign up and sign in
- ✅ Users can browse and order
- ✅ Payment integration works
- ✅ Site is responsive and fast
- ✅ Security measures are active

---

## 📝 Test Results Template

```
Date: ___________
Tester: ___________

Test Results:
- Homepage: ✅ / ❌
- Sign Up: ✅ / ❌
- Sign In: ✅ / ❌
- Restaurant List: ✅ / ❌
- Menu View: ✅ / ❌
- Add to Cart: ✅ / ❌
- Cart View: ✅ / ❌
- Checkout: ✅ / ❌
- Order Placement: ✅ / ❌
- Mobile Responsive: ✅ / ❌

Issues Found:
1. ___________
2. ___________

Overall Status: ✅ PASS / ❌ FAIL
```

---

**Good luck with your deployment testing!** 🎉
