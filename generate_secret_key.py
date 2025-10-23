#!/usr/bin/env python
"""
Generate a new Django SECRET_KEY
"""
from django.core.management.utils import get_random_secret_key

if __name__ == "__main__":
    secret_key = get_random_secret_key()
    print("\n" + "="*60)
    print("Your new Django SECRET_KEY:")
    print("="*60)
    print(secret_key)
    print("="*60)
    print("\nCopy this key and use it in your Railway environment variables")
    print("Variable name: SECRET_KEY")
    print("="*60 + "\n")
