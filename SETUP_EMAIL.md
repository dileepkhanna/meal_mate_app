# 📧 Setup Real Email for Password Reset

## Current Status
- ⚠️ Emails are printing to console (testing mode)
- ❌ Not sending to user's actual email

## Solution: Configure Gmail SMTP

---

## 🚀 Quick Setup (5 minutes)

### Step 1: Get Gmail App Password

1. **Go to your Google Account**: https://myaccount.google.com/
2. **Enable 2-Step Verification**:
   - Go to Security → 2-Step Verification
   - Follow the steps to enable it
3. **Generate App Password**:
   - Go to Security → 2-Step Verification → App passwords
   - Select "Mail" and "Other (Custom name)"
   - Enter "Meal Mate" as the name
   - Click "Generate"
   - **Copy the 16-character password** (like: abcd efgh ijkl mnop)

### Step 2: Create Environment File

Create a file named `.env` in your project root:

```bash
# .env file
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-16-char-app-password
```

**Example:**
```bash
EMAIL_HOST_USER=john.doe@gmail.com
EMAIL_HOST_PASSWORD=abcdefghijklmnop
```

### Step 3: Install python-decouple

```bash
pip install python-decouple
```

### Step 4: Update settings.py

I'll do this for you automatically, or you can manually add:

```python
from decouple import config

EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
```

### Step 5: Test It!

```bash
python test_email.py
```

---

## 🎯 Alternative: Manual Configuration (Quick Test)

If you want to test quickly without environment variables:

### Update `meal_mate/settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'  # Your Gmail
EMAIL_HOST_PASSWORD = 'your-app-password'  # Your 16-char app password
DEFAULT_FROM_EMAIL = 'your-email@gmail.com'
```

**⚠️ Warning**: Don't commit this file to Git with your real password!

---

## 📧 Other Email Services

### Option 2: SendGrid (Free 100 emails/day)

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = 'your-sendgrid-api-key'
DEFAULT_FROM_EMAIL = 'your-verified-email@domain.com'
```

### Option 3: Mailgun (Free 5,000 emails/month)

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.mailgun.org'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'postmaster@your-domain.mailgun.org'
EMAIL_HOST_PASSWORD = 'your-mailgun-password'
DEFAULT_FROM_EMAIL = 'noreply@your-domain.com'
```

---

## 🧪 Testing

### Test Email Sending:

```bash
python test_email.py
```

This will:
1. Send a test email to your configured address
2. Verify SMTP connection
3. Show any errors

### Test Forgot Password:

1. Go to: http://127.0.0.1:8000/signin/
2. Click "Forgot Password?"
3. Enter your email
4. Check your email inbox!

---

## 🐛 Troubleshooting

### Error: "Username and Password not accepted"
- ✅ Make sure you're using an **App Password**, not your regular Gmail password
- ✅ Enable 2-Step Verification first
- ✅ Generate a new App Password

### Error: "SMTPAuthenticationError"
- ✅ Check your email and password are correct
- ✅ Make sure there are no extra spaces
- ✅ Try generating a new App Password

### Email Not Received
- ✅ Check spam folder
- ✅ Verify email address is correct
- ✅ Check Gmail "Less secure app access" (if using old method)
- ✅ Use App Password instead

### Error: "Connection refused"
- ✅ Check your internet connection
- ✅ Verify EMAIL_PORT is 587
- ✅ Make sure EMAIL_USE_TLS is True

---

## 🔒 Security Best Practices

### ✅ DO:
- Use environment variables for credentials
- Use App Passwords (not regular password)
- Add `.env` to `.gitignore`
- Use different passwords for different apps

### ❌ DON'T:
- Commit passwords to Git
- Share your App Password
- Use your regular Gmail password
- Hardcode credentials in code

---

## 📝 Quick Reference

### Gmail App Password Setup:
1. Google Account → Security
2. Enable 2-Step Verification
3. App passwords → Generate
4. Copy 16-character password
5. Add to `.env` file

### Environment Variables:
```bash
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=abcdefghijklmnop
```

### Test Command:
```bash
python test_email.py
```

---

## ✅ Checklist

- [ ] Gmail 2-Step Verification enabled
- [ ] App Password generated
- [ ] `.env` file created
- [ ] Email credentials added
- [ ] `python-decouple` installed
- [ ] Test email sent successfully
- [ ] Forgot password tested

---

*Once configured, users will receive real emails with password reset links!*
