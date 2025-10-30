#!/usr/bin/env python
"""
Interactive Email Configuration Helper
"""

print("\n" + "="*70)
print("📧 EMAIL CONFIGURATION HELPER")
print("="*70)

print("\n📝 This will help you configure email for password reset.")
print("   You'll need a Gmail account with App Password.")

print("\n" + "="*70)
print("STEP 1: Do you have a Gmail App Password?")
print("="*70)

print("\nIf NO:")
print("  1. Go to: https://myaccount.google.com/security")
print("  2. Enable 2-Step Verification")
print("  3. Go to App passwords")
print("  4. Generate password for 'Mail' → 'Other (Meal Mate)'")
print("  5. Copy the 16-character password")

print("\nIf YES:")
print("  Continue below...")

input("\nPress Enter when you have your App Password ready...")

print("\n" + "="*70)
print("STEP 2: Enter Your Email Credentials")
print("="*70)

email = input("\nEnter your Gmail address: ").strip()
password = input("Enter your App Password (16 chars): ").strip().replace(' ', '')

if not email or not password:
    print("\n❌ Email and password are required!")
    exit(1)

print("\n" + "="*70)
print("STEP 3: Choose Configuration Method")
print("="*70)

print("\n1. Environment Variables (.env file) - RECOMMENDED")
print("   ✅ Secure - credentials not in code")
print("   ✅ Easy to change")
print("   ✅ Won't be committed to Git")

print("\n2. Direct in settings.py - QUICK TEST")
print("   ⚠️  Less secure")
print("   ⚠️  Need to be careful with Git")

choice = input("\nChoose method (1 or 2): ").strip()

if choice == "1":
    # Create .env file
    env_content = f"""# Email Configuration for Meal Mate
EMAIL_HOST_USER={email}
EMAIL_HOST_PASSWORD={password}
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("\n✅ Created .env file with your credentials")
    
    # Check if python-decouple is installed
    try:
        import decouple
        print("✅ python-decouple is installed")
    except ImportError:
        print("\n⚠️  python-decouple not installed")
        print("   Run: pip install python-decouple")
    
    # Add to .gitignore
    gitignore_content = "\n# Environment variables\n.env\n"
    try:
        with open('.gitignore', 'a') as f:
            f.write(gitignore_content)
        print("✅ Added .env to .gitignore")
    except:
        print("⚠️  Could not update .gitignore")
    
    print("\n📝 Next steps:")
    print("   1. Install: pip install python-decouple")
    print("   2. Restart Django server")
    print("   3. Test: python test_email.py")

elif choice == "2":
    print("\n📝 Add these lines to meal_mate/settings.py:")
    print("-" * 70)
    print(f"EMAIL_HOST_USER = '{email}'")
    print(f"EMAIL_HOST_PASSWORD = '{password}'")
    print("-" * 70)
    print("\n⚠️  Remember: Don't commit this file to Git!")
    print("   Add settings.py to .gitignore or remove credentials before committing")

else:
    print("\n❌ Invalid choice")
    exit(1)

print("\n" + "="*70)
print("✅ CONFIGURATION COMPLETE!")
print("="*70)

print("\n🧪 Test your configuration:")
print("   python test_email.py")

print("\n🔑 Test forgot password:")
print("   1. Go to: http://127.0.0.1:8000/signin/")
print("   2. Click 'Forgot Password?'")
print("   3. Enter your email")
print("   4. Check your inbox!")

print("\n" + "="*70)
