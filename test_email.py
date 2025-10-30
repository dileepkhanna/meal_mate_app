#!/usr/bin/env python
"""
Test Email Configuration
"""
import sys
import os
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meal_mate.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

print("\n" + "="*70)
print("📧 EMAIL CONFIGURATION TEST")
print("="*70)

# Check configuration
print("\n📋 Current Email Settings:")
print("-" * 70)
print(f"Backend: {settings.EMAIL_BACKEND}")
print(f"Host: {settings.EMAIL_HOST}")
print(f"Port: {settings.EMAIL_PORT}")
print(f"Use TLS: {settings.EMAIL_USE_TLS}")
print(f"From Email: {settings.DEFAULT_FROM_EMAIL}")

if settings.EMAIL_HOST_USER:
    print(f"Host User: {settings.EMAIL_HOST_USER}")
    print(f"Password: {'*' * len(settings.EMAIL_HOST_PASSWORD) if settings.EMAIL_HOST_PASSWORD else 'NOT SET'}")
else:
    print("⚠️  Email credentials not configured!")
    print("\n💡 To send real emails:")
    print("   1. See SETUP_EMAIL.md for instructions")
    print("   2. Configure Gmail App Password")
    print("   3. Update settings.py or create .env file")

# Check if using console backend
if 'console' in settings.EMAIL_BACKEND.lower():
    print("\n⚠️  Currently using CONSOLE backend")
    print("   Emails will print to terminal, not send to users")
    print("\n💡 To send real emails:")
    print("   Change EMAIL_BACKEND to 'django.core.mail.backends.smtp.EmailBackend'")
    print("   in meal_mate/settings.py")

# Test email sending
print("\n" + "="*70)
print("📤 Sending Test Email...")
print("="*70)

test_email = input("\nEnter email address to test (or press Enter to skip): ").strip()

if test_email:
    try:
        send_mail(
            subject='Test Email from Meal Mate',
            message='This is a test email to verify your email configuration is working correctly.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[test_email],
            fail_silently=False,
        )
        
        if 'console' in settings.EMAIL_BACKEND.lower():
            print("\n✅ Email printed to console above")
            print("   (Not sent to actual email - console mode)")
        else:
            print(f"\n✅ Test email sent successfully to {test_email}!")
            print("   Check your inbox (and spam folder)")
            
    except Exception as e:
        print(f"\n❌ Error sending email: {e}")
        print("\n💡 Common issues:")
        print("   1. Wrong email/password")
        print("   2. Need to use App Password (not regular password)")
        print("   3. 2-Step Verification not enabled")
        print("   4. Internet connection issue")
        print("\n   See SETUP_EMAIL.md for detailed setup instructions")
else:
    print("\n⏭️  Skipped email test")

print("\n" + "="*70)
print("📊 SUMMARY")
print("="*70)

if 'console' in settings.EMAIL_BACKEND.lower():
    print("Status: ⚠️  Console Mode (Testing)")
    print("Action: Configure real email to send to users")
    print("Guide: See SETUP_EMAIL.md")
elif settings.EMAIL_HOST_USER and settings.EMAIL_HOST_PASSWORD:
    print("Status: ✅ SMTP Configured")
    print("Action: Test forgot password feature")
else:
    print("Status: ❌ Not Configured")
    print("Action: Add email credentials")
    print("Guide: See SETUP_EMAIL.md")

print("="*70)
