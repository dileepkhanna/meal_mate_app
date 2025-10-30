# 📧 Quick Email Setup (5 Minutes)

## Current Problem
- ⚠️ Emails only print to console
- ❌ Not sending to user's actual email

## Quick Solution

### Option 1: Automated Setup (Easiest)

```bash
python configure_email.py
```

Follow the prompts to configure email automatically!

---

### Option 2: Manual Setup (5 minutes)

#### Step 1: Get Gmail App Password

1. Go to: https://myaccount.google.com/security
2. Enable **2-Step Verification**
3. Go to **App passwords**
4. Select **Mail** → **Other (Custom name)**
5. Enter "Meal Mate"
6. Click **Generate**
7. **Copy the 16-character password**

#### Step 2: Update settings.py

Open `meal_mate/settings.py` and find this section:

```python
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
```

Replace with:

```python
EMAIL_HOST_USER = 'your-email@gmail.com'  # Your Gmail
EMAIL_HOST_PASSWORD = 'abcdefghijklmnop'  # Your 16-char app password
```

#### Step 3: Test It

```bash
python test_email.py
```

Enter your email when prompted, and check your inbox!

---

## ✅ That's It!

Now when users click "Forgot Password?", they'll receive real emails!

---

## 🧪 Test Forgot Password

1. Go to: http://127.0.0.1:8000/signin/
2. Click "Forgot Password?"
3. Enter email address
4. Check email inbox
5. Click reset link
6. Set new password!

---

## 🔒 Security Note

**Don't commit your password to Git!**

Better approach:
1. Create `.env` file:
   ```
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   ```

2. Install python-decouple:
   ```bash
   pip install python-decouple
   ```

3. Update settings.py:
   ```python
   from decouple import config
   
   EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
   EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
   ```

4. Add `.env` to `.gitignore`

---

## 📞 Need Help?

See detailed guide: `SETUP_EMAIL.md`

Or run: `python configure_email.py`
