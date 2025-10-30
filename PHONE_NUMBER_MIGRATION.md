# Phone Number as Unique Field - Migration Guide

## Changes Made

### 1. Model Changes
- Made `mobile` field unique in Customer model
- Added validation for 10-digit phone numbers

### 2. Signin Changes
- Replaced username input with phone number input
- Added 10-digit validation
- Updated login handler to authenticate by phone number

### 3. Signup Changes
- Added duplicate phone number check
- Phone number is now required and unique

### 4. OTP Changes
- OTP can now be requested using phone number, email, or username
- Auto-detects if input is phone (10 digits), email (@), or username

## Migration Steps

### Step 1: Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 2: Handle Existing Data (If Any)

If you have existing users without phone numbers or with duplicate phone numbers:

**Option A: Update via Django Shell**
```bash
python manage.py shell
```

```python
from delivery.models import Customer

# Find users without phone numbers
users_without_phone = Customer.objects.filter(mobile='')
print(f"Users without phone: {users_without_phone.count()}")

# Assign temporary unique phone numbers
for i, user in enumerate(users_without_phone):
    user.mobile = f"9999{str(i).zfill(6)}"  # Creates: 9999000001, 9999000002, etc.
    user.save()
    print(f"Updated {user.username} with phone: {user.mobile}")

# Check for duplicate phone numbers
from django.db.models import Count
duplicates = Customer.objects.values('mobile').annotate(count=Count('mobile')).filter(count__gt=1)
print(f"Duplicate phones: {duplicates}")
```

**Option B: Fresh Database**
If you're in development and can reset:
```bash
# Delete database
del db.sqlite3

# Delete migrations
del delivery/migrations/0*.py

# Recreate everything
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### Step 3: Test the Changes

1. **Test Signup:**
   - Try signing up with a phone number
   - Verify duplicate phone numbers are rejected

2. **Test Signin:**
   - Login using phone number and password
   - Verify authentication works

3. **Test OTP:**
   - Request OTP using phone number
   - Request OTP using email
   - Request OTP using username
   - Verify all methods work

## Important Notes

### Phone Number Format
- Must be exactly 10 digits
- No spaces, dashes, or special characters
- Example: `9876543210`

### Validation Rules
- Signin: Requires 10-digit phone number
- Signup: Phone number must be unique
- OTP: Accepts phone (10 digits), email (@), or username

### User Experience
- Clear error messages for invalid phone numbers
- Helpful placeholder text
- Pattern validation (HTML5)
- Small hint text below input

## Troubleshooting

### Error: "UNIQUE constraint failed"
**Cause:** Trying to create user with existing phone number
**Solution:** Check if phone number already exists in database

### Error: "mobile cannot be null"
**Cause:** Existing users without phone numbers
**Solution:** Run Option A from Step 2 above

### Error: "Invalid phone number"
**Cause:** Phone number not exactly 10 digits
**Solution:** Ensure phone number is 10 digits, no spaces

## Rollback (If Needed)

If you need to revert changes:

1. Remove `unique=True` from mobile field in models.py
2. Change signin back to username
3. Run migrations again

## Future Enhancements

- SMS OTP using phone number
- Phone number verification during signup
- International phone number support (+91, etc.)
- Phone number formatting (display as: 98765-43210)
