from django.test import TestCase
import pytest

# Create your tests here.

class BasicTestCase(TestCase):
    """Basic test to verify test setup is working"""
    
    def test_basic_assertion(self):
        """Test that basic assertions work"""
        self.assertTrue(True)
        self.assertEqual(1 + 1, 2)
        
    def test_django_setup(self):
        """Test that Django is properly configured"""
        from django.conf import settings
        self.assertTrue(hasattr(settings, 'INSTALLED_APPS'))

@pytest.mark.django_db
def test_pytest_django_setup():
    """Test that pytest-django is working"""
    assert True
