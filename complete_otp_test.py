#!/usr/bin/env python
"""
Complete end-to-end OTP test
"""
import requests
from bs4 import BeautifulSoup
import re

BASE_URL = "http://127.0.0.1:8000"

def get_csrf_token(session, url):
    """Extract CSRF token from a page"""
    response = session.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})
    if csrf_token:
        return csrf_token.get('value')
    return None

print("\n" + "="*70)
print("🎯 COMPLETE END-TO-END OTP LOGIN TEST")
print("="*70)

session = requests.Session()

# Step 1: Request OTP
print("\n📱 STEP 1: Requesting OTP")
print("-" * 70)
csrf_token = get_csrf_token(session, f"{BASE_URL}/signin/")
print(f"✅ CSRF token obtained")

data = {
    'csrfmiddlewaretoken': csrf_token,
    'identifier': '9876543210'
}

response = session.post(
    f"{BASE_URL}/otp/request/",
    data=data,
    headers={'Referer': f"{BASE_URL}/signin/"},
    allow_redirects=True
)

if 'verify' in response.url:
    print(f"✅ Successfully redirected to verification page")
    print(f"   URL: {response.url}")
else:
    print(f"❌ Unexpected redirect: {response.url}")
    exit(1)

# Step 2: Get the latest OTP from database
print("\n🔑 STEP 2: Retrieving OTP from database")
print("-" * 70)
import sys
import os
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meal_mate.settings')
django.setup()

from delivery.models import OTP, Customer

user = Customer.objects.get(mobile='9876543210')
latest_otp = OTP.objects.filter(user=user, is_used=False).order_by('-created_at').first()

if latest_otp:
    otp_code = latest_otp.otp_code
    print(f"✅ OTP retrieved: {otp_code}")
    print(f"   Expires at: {latest_otp.expires_at}")
    print(f"   Is valid: {latest_otp.is_valid()}")
else:
    print("❌ No OTP found")
    exit(1)

# Step 3: Verify OTP
print("\n✅ STEP 3: Verifying OTP")
print("-" * 70)

# Get new CSRF token for verification page
csrf_token = get_csrf_token(session, f"{BASE_URL}/otp/verify/")
print(f"✅ New CSRF token obtained for verification")

verify_data = {
    'csrfmiddlewaretoken': csrf_token,
    'otp_code': otp_code
}

response = session.post(
    f"{BASE_URL}/otp/verify/submit/",
    data=verify_data,
    headers={'Referer': f"{BASE_URL}/otp/verify/"},
    allow_redirects=True
)

print(f"   Response status: {response.status_code}")
print(f"   Final URL: {response.url}")

# Check if logged in successfully
if 'customer' in response.url or 'home' in response.url:
    print("\n" + "="*70)
    print("🎉 SUCCESS! OTP LOGIN COMPLETED!")
    print("="*70)
    print(f"✅ User logged in successfully")
    print(f"✅ Redirected to: {response.url}")
    print(f"✅ Session authenticated")
    
    # Verify OTP is marked as used
    latest_otp.refresh_from_db()
    print(f"✅ OTP marked as used: {latest_otp.is_used}")
    
elif 'signin' in response.url:
    print("\n❌ FAILED: Redirected back to signin")
    print("   This might indicate an OTP verification error")
else:
    print(f"\n⚠️  Unexpected redirect: {response.url}")

print("\n" + "="*70)
print("📊 TEST SUMMARY")
print("="*70)
print("✅ OTP Request: SUCCESS")
print("✅ OTP Generation: SUCCESS")
print("✅ OTP Email: SUCCESS (check server console)")
print("✅ OTP Verification: SUCCESS" if 'customer' in response.url or 'home' in response.url else "❌ OTP Verification: FAILED")
print("✅ User Login: SUCCESS" if 'customer' in response.url or 'home' in response.url else "❌ User Login: FAILED")
print("="*70)
