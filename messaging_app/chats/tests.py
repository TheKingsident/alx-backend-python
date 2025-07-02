import pytest
from django.conf import settings

# Create your tests here.

def test_basic_assertion():
    """Test that basic assertions work"""
    assert True
    assert 1 + 1 == 2

def test_django_settings():
    """Test that Django settings are properly configured"""
    assert hasattr(settings, 'INSTALLED_APPS')
    assert 'chats' in settings.INSTALLED_APPS

def test_python_basics():
    """Test basic Python functionality"""
    test_list = [1, 2, 3]
    assert len(test_list) == 3
    assert max(test_list) == 3

def test_string_operations():
    """Test string operations"""
    test_string = "Hello World"
    assert test_string.lower() == "hello world"
    assert "World" in test_string
