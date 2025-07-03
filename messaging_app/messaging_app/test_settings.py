"""
Test settings for GitHub Actions CI/CD
"""
import os

# Override database settings for testing
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME', 'test_messaging_app'),
        'USER': os.environ.get('DB_USER', 'test_user'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'test_password'),
        'HOST': os.environ.get('DB_HOST', '127.0.0.1'),
        'PORT': os.environ.get('DB_PORT', '3306'),
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
        'TEST': {
            'CHARSET': 'utf8mb4',
            'COLLATION': 'utf8mb4_unicode_ci',
        }
    }
}

# Use in-memory cache for testing
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# Allow migrations for CI to ensure database is properly set up
# We need Django's built-in migrations to create core tables
# MIGRATION_MODULES = DisableMigrations()  # Disabled for CI

# Test-specific settings
SECRET_KEY = 'test-secret-key-for-github-actions'
DEBUG = True
ALLOWED_HOSTS = ['*']

# Disable logging during tests
LOGGING_CONFIG = None

# Speed up password hashing for tests
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]
