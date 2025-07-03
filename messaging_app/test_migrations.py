#!/usr/bin/env python
"""
Test script to verify that migrations work correctly
"""
import os
import sys
import django
from django.conf import settings
from django.core.management import execute_from_command_line

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'messaging_app.test_settings')
    try:
        django.setup()
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    # Test migrate command
    print("Testing migrate command...")
    try:
        execute_from_command_line(['manage.py', 'migrate', '--dry-run', '--verbosity=2'])
        print("✓ Migrations look good")
    except Exception as e:
        print(f"✗ Migration error: {e}")
        sys.exit(1)
    
    # Test showmigrations command
    print("\nShowing migration status...")
    try:
        execute_from_command_line(['manage.py', 'showmigrations'])
        print("✓ Migration status checked")
    except Exception as e:
        print(f"✗ Show migrations error: {e}")
        sys.exit(1)
