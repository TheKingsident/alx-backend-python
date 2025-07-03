from django.conf import settings
from django.test import TestCase


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


class DatabaseTestCase(TestCase):
    """Test that database operations work"""

    def test_database_connection(self):
        """Test that we can connect to the database"""
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            self.assertEqual(result[0], 1)

    def test_custom_user_model(self):
        """Test that our custom user model works"""
        from chats.models import User

        # Create a test user
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

        # Test that the user was created properly
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('testpass123'))
        self.assertIsNotNone(user.user_id)

        # Test that we can retrieve the user
        retrieved_user = User.objects.get(username='testuser')
        self.assertEqual(retrieved_user.user_id, user.user_id)
