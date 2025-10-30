#!/usr/bin/env python
"""
Live OTP test - Actually request and display OTP
"""
import requests
from bs4 import BeautifulSoup
import time

BASE_URL = "http://127.0.0.1:8000"

def get_csrf_token(session, url):
    """Extract CSRF token from a page"""
    response = session.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})
    if csrf_token:
        return csrf_token.get('value')
    return None

print("\n" + "="*60)
print("🔥 LIVE OTP TEST - Requesting Real OTP")
print("="*60)

session = requests.Session()

# Step 1: Get signin page
print("\n1️⃣  Loading signin page...")
csrf_token = get_csrf_token(session, f"{BASE_URL}/signin/")
if csrf_token:
    print(f"   ✅ CSRF token obtained")
else:
    print("   ❌ Failed to get CSRF token")
    exit(1)

# Step 2: Request OTP
print("\n2️⃣  Requesting OTP for phone: 9876543210")
data = {
    'csrfmiddlewaretoken': csrf_token,
    'identifier': '9876543210'
}

response = session.post(
    f"{BASE_URL}/otp/request/",
    data=data,
    headers={'Referer': f"{BASE_URL}/signin/"},
    allow_redirects=False
)

print(f"   Response status: {response.status_code}")
if response.status_code == 302:
    redirect_url = response.headers.get('Location', '')
    print(f"   ✅ Redirected to: {redirect_url}")
    
    if 'verify' in redirect_url:
        print("\n3️⃣  ✅ OTP REQUEST SUCCESSFUL!")
        print("\n" + "="*60)
        print("📧 CHECK THE SERVER CONSOLE OUTPUT ABOVE")
        print("="*60)
        print("Look for an email output that contains:")
        print("  - Subject: Your Meal Mate Login OTP")
        print("  - A 6-digit OTP code")
        print("\nThe OTP should be printed in the Django server console")
        print("(the terminal where 'python manage.py runserver' is running)")
        print("="*60)
    else:
        print(f"   ⚠️  Unexpected redirect: {redirect_url}")
else:
    print(f"   ❌ Unexpected response: {response.status_code}")
    print(f"   Response text: {response.text[:200]}")

print("\n" + "="*60)
print("🎯 NEXT STEPS FOR MANUAL TESTING:")
print("="*60)
print("1. Check the Django server terminal for the OTP email output")
print("2. Copy the 6-digit OTP code")
print("3. Open: http://127.0.0.1:8000/otp/verify/")
print("4. Enter the OTP code")
print("5. Click 'Verify OTP'")
print("6. You should be logged in as 'testuser'!")
print("="*60)
