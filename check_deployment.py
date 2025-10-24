#!/usr/bin/env python
"""
Deployment Checker Script
Run this to verify your deployment configuration
"""

import os
import sys
from pathlib import Path

def check_file_exists(filepath, description):
    """Check if a file exists"""
    if Path(filepath).exists():
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description} MISSING: {filepath}")
        return False

def check_settings():
    """Check settings.py configuration"""
    print("\n" + "="*60)
    print("CHECKING SETTINGS.PY")
    print("="*60)
    
    try:
        # Set Django settings
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meal_mate.settings')
        
        # Import Django
        import django
        django.setup()
        
        from django.conf import settings
        
        # Check critical settings
        checks = {
            'SECRET_KEY': bool(settings.SECRET_KEY),
            'DEBUG': settings.DEBUG,
            'ALLOWED_HOSTS': bool(settings.ALLOWED_HOSTS),
            'STATIC_ROOT': bool(settings.STATIC_ROOT),
            'STATIC_URL': bool(settings.STATIC_URL),
            'DATABASES': bool(settings.DATABASES),
            'INSTALLED_APPS': 'delivery' in str(settings.INSTALLED_APPS),
            'MIDDLEWARE': 'whitenoise' in str(settings.MIDDLEWARE),
        }
        
        for key, value in checks.items():
            status = "✅" if value else "❌"
            print(f"{status} {key}: {value}")
        
        return all(checks.values())
    except Exception as e:
        print(f"❌ Error checking settings: {e}")
        return False

def check_deployment_files():
    """Check if all deployment files exist"""
    print("\n" + "="*60)
    print("CHECKING DEPLOYMENT FILES")
    print("="*60)
    
    files = {
        'Procfile': 'Procfile for Railway',
        'railway.json': 'Railway configuration',
        'runtime.txt': 'Python version specification',
        'requirements.txt': 'Python dependencies',
        'manage.py': 'Django management script',
        'meal_mate/wsgi.py': 'WSGI application',
        'meal_mate/settings.py': 'Django settings',
    }
    
    results = []
    for filepath, description in files.items():
        results.append(check_file_exists(filepath, description))
    
    return all(results)

def check_requirements():
    """Check if all required packages are in requirements.txt"""
    print("\n" + "="*60)
    print("CHECKING REQUIREMENTS.TXT")
    print("="*60)
    
    required_packages = [
        'Django',
        'gunicorn',
        'whitenoise',
        'razorpay',
    ]
    
    try:
        with open('requirements.txt', 'r') as f:
            content = f.read()
        
        results = []
        for package in required_packages:
            if package.lower() in content.lower():
                print(f"✅ {package} found")
                results.append(True)
            else:
                print(f"❌ {package} MISSING")
                results.append(False)
        
        return all(results)
    except FileNotFoundError:
        print("❌ requirements.txt not found")
        return False

def check_procfile():
    """Check Procfile configuration"""
    print("\n" + "="*60)
    print("CHECKING PROCFILE")
    print("="*60)
    
    try:
        with open('Procfile', 'r') as f:
            content = f.read()
        
        checks = {
            'gunicorn': 'gunicorn' in content,
            'wsgi': 'wsgi' in content,
            'meal_mate': 'meal_mate' in content,
        }
        
        for key, value in checks.items():
            status = "✅" if value else "❌"
            print(f"{status} {key} configured: {value}")
        
        print(f"\nProcfile content:\n{content}")
        
        return all(checks.values())
    except FileNotFoundError:
        print("❌ Procfile not found")
        return False

def check_static_files():
    """Check static files configuration"""
    print("\n" + "="*60)
    print("CHECKING STATIC FILES")
    print("="*60)
    
    static_dirs = [
        'delivery/static',
        'delivery/static/delivery',
        'delivery/static/delivery/css',
    ]
    
    results = []
    for directory in static_dirs:
        if Path(directory).exists():
            print(f"✅ {directory} exists")
            results.append(True)
        else:
            print(f"❌ {directory} MISSING")
            results.append(False)
    
    # Check if style.css exists
    if Path('delivery/static/delivery/css/style.css').exists():
        print(f"✅ style.css exists")
        results.append(True)
    else:
        print(f"❌ style.css MISSING")
        results.append(False)
    
    return all(results)

def print_environment_variables():
    """Print required environment variables"""
    print("\n" + "="*60)
    print("REQUIRED ENVIRONMENT VARIABLES FOR RAILWAY")
    print("="*60)
    
    variables = {
        'SECRET_KEY': 'Django secret key (generate new one)',
        'DEBUG': 'False',
        'ALLOWED_HOSTS': 'web-production-9d6bf.up.railway.app',
        'CSRF_TRUSTED_ORIGINS': 'https://web-production-9d6bf.up.railway.app',
        'RAZORPAY_KEY_ID': 'Your Razorpay key',
        'RAZORPAY_KEY_SECRET': 'Your Razorpay secret',
    }
    
    print("\nSet these in Railway Dashboard → Variables:")
    print("-" * 60)
    for key, value in variables.items():
        print(f"{key}={value}")

def print_deployment_commands():
    """Print deployment commands"""
    print("\n" + "="*60)
    print("DEPLOYMENT COMMANDS")
    print("="*60)
    
    commands = [
        "# After setting environment variables, run:",
        "railway run python manage.py migrate",
        "railway run python manage.py collectstatic --noinput",
        "railway run python manage.py createsuperuser",
        "",
        "# To view logs:",
        "railway logs",
        "",
        "# To check status:",
        "railway status",
    ]
    
    for cmd in commands:
        print(cmd)

def main():
    """Main function"""
    print("\n" + "="*60)
    print("RAILWAY DEPLOYMENT CHECKER")
    print("="*60)
    
    results = []
    
    # Run all checks
    results.append(check_deployment_files())
    results.append(check_requirements())
    results.append(check_procfile())
    results.append(check_static_files())
    results.append(check_settings())
    
    # Print environment variables
    print_environment_variables()
    
    # Print deployment commands
    print_deployment_commands()
    
    # Final result
    print("\n" + "="*60)
    print("FINAL RESULT")
    print("="*60)
    
    if all(results):
        print("✅ ALL CHECKS PASSED!")
        print("Your project is ready for deployment.")
        print("\nNext steps:")
        print("1. Set environment variables in Railway")
        print("2. Push to GitHub")
        print("3. Deploy on Railway")
        print("4. Run migration and collectstatic commands")
    else:
        print("❌ SOME CHECKS FAILED!")
        print("Please fix the issues above before deploying.")
        sys.exit(1)

if __name__ == "__main__":
    main()
