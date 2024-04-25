from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from unittest.mock import patch

from ..providers import ProviderError

User = get_user_model()

OKTA_OAUTH2_CALLBACK_URL = reverse("users:oauth2_callback")
LOGIN_URL = reverse("users:login")
LOGOUT_URL = reverse("users:logout")
ME_URL = reverse("users:me")


class LoginViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    @patch("users.views.Provider")
    def test_on_provider_error(self, provider_mock):
        provider_instance = provider_mock.return_value
        provider_instance.get_authorization_url.side_effect = ProviderError(
            "some provider error"
        )
        response = self.client.get(LOGIN_URL)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.data.get("detail"), "some provider error")

    @patch("users.views.Provider")
    def test_get_authorization_url(self, provider_mock):
        provider_instance = provider_mock.return_value
        url = "https://some_login_url.com"
        state = "some_random_state"
        provider_instance.get_authorization_url.return_value = (url, state)
        response = self.client.get(LOGIN_URL)
        self.assertEqual(self.client.session.get("state"), "some_random_state")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("url"), "https://some_login_url.com")


class OidcCallbackViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def _set_state_session(self, value):
        session = self.client.session
        session["state"] = value
        session.save()

    def test_post_with_missing_required_data(self):
        response = self.client.post(OKTA_OAUTH2_CALLBACK_URL, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data.get("detail"), "Missing authorization code and/or state"
        )

    def test_state_session_not_matching_posted_state(self):
        self._set_state_session("some_state_value")
        response = self.client.post(
            OKTA_OAUTH2_CALLBACK_URL, {"code": "some_code", "state": "some_other_value"}
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data.get("detail"), "State value does not match")

    @patch("users.views.Provider")
    def test_provider_error_when_requesting_token(self, provider_mock):
        provider_instance = provider_mock.return_value
        provider_instance.get_id_token.side_effect = ProviderError(
            "some provider error"
        )
        self._set_state_session("some_state_value")
        response = self.client.post(
            OKTA_OAUTH2_CALLBACK_URL, {"code": "some_code", "state": "some_state_value"}
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data.get("detail"), "some provider error")

    @patch("users.views.Provider")
    @patch("users.backends.OidcAuthentication.authenticate", return_value=None)
    def test_failing_to_authenticate(self, _, __):
        self._set_state_session("some_state_value")
        response = self.client.post(
            OKTA_OAUTH2_CALLBACK_URL, {"code": "some_code", "state": "some_state_value"}
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data.get("detail"), "Invalid access token")

    @patch("users.views.Provider")
    @patch("users.backends.OidcAuthentication.authenticate", return_value=None)
    def test_successfull_authentication(self, auth_mock, _):
        user = User.objects.create(email="someone@kering.com", name="some_name")
        auth_mock.return_value = user
        self._set_state_session("some_state_value")
        response = self.client.post(
            OKTA_OAUTH2_CALLBACK_URL, {"code": "some_code", "state": "some_state_value"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data.get("user"),
            {
                "email": user.email,
                "name": user.name,
            },
        )


class LogoutViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_logout_view(self):
        """Test the logout view successfully logs out a user."""
        user = User.objects.create_user(email="test@example.com", name="Test User")
        self.client.force_login(user)
        response = self.client.get(LOGOUT_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("message"), "Logout successful")


class UserInfoViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_user_info_view_unauthorized(self):
        """Test unauthorized access to the user info view."""
        response = self.client.get(ME_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_info_view_success(self):
        """Test successful access to the user info view for logged-in user."""
        user = User.objects.create_user(email="test@example.com", name="Test User")
        self.client.force_authenticate(user=user)
        response = self.client.get(ME_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], user.email)
        self.assertEqual(response.data["name"], user.name)
