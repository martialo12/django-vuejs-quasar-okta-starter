from django.test import TestCase
from django.contrib.auth import get_user_model


def create_user(email="user@example.com", **extra_fields):
    """Create and return a new user."""
    return get_user_model().objects.create_user(email, **extra_fields)


class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        email = "test@example.com"
        user = create_user(email=email)

        self.assertEqual(user.email, email)

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_emails = [
            ["test1@EXAMPLE.com", "test1@example.com"],
            ["Test2@Example.com", "Test2@example.com"],
            ["TEST3@EXAMPLE.com", "TEST3@example.com"],
            ["test4@example.COM", "test4@example.com"],
        ]
        for email, expected in sample_emails:
            user = create_user(email=email)
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError."""
        with self.assertRaises(ValueError):
            create_user(email="")

    def test_create_superuser(self):
        """Test creating a superuser."""
        user = get_user_model().objects.create_superuser(email="test@example.com")

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
