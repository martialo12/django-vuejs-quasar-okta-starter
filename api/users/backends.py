import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from django.http import HttpRequest
import jwt

from .models import User as AppUser

log = logging.getLogger(__name__)

User = get_user_model()


def decode_token(id_token: str, client_id: str, jwks_uri: str) -> dict | None:
    """
    Decode a jwt token.

    Returns:
        dict | None: The decoded JWT token or None if decoding failed.
    """
    client = jwt.PyJWKClient(jwks_uri)
    signing_key = client.get_signing_key_from_jwt(id_token)
    header_data = jwt.get_unverified_header(id_token)
    try:
        return jwt.decode(
            id_token,
            signing_key.key,
            algorithms=[header_data.get("alg")],
            audience=client_id,
            options={"verify_exp": True},
        )
    except (jwt.ExpiredSignatureError, jwt.PyJWTError, Exception) as e:
        log.error(e)
    return None


class OidcAuthentication(BaseBackend):
    """Authenticates against OKTA identity provider."""

    def authenticate(
        self, _: HttpRequest, id_token: str, client_id: str, jwks_uri: str
    ) -> AppUser | None:
        """
        Authenticate a user from the provided JWT token.

        Args:
            id_token (str): The token retreived from the authorization server.
            client_id (str): The id of the authorization server.
            jwks_uri (str): The URL of the authorization server's JSON Web Key Set document.

        Returns:
            user: User instance or None on decoding failure.
        """
        user_infos = decode_token(id_token, client_id, jwks_uri)
        if user_infos:
            email = user_infos.get("email")
            name = user_infos.get("name")
            return self._update_or_create_user(email, name)
        return None

    def get_user(self, user_id: int) -> AppUser | None:
        """
        GET the User object from the provided databse id.

        Args:
            user_id (int): The id of the user.

        Returns:
            user: User instance or None.
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def _update_or_create_user(self, email: str, name: str) -> AppUser:
        """
        Create or update a user instance.

        Args:
            email (str): The id of the user.
            name (str): The id of the user.

        Returns:
            user: User instance.
        """
        user, created = User.objects.update_or_create(
            defaults={"name": name},
            create_defaults={
                "email": email,
                "name": name,
                "is_active": True,
                "is_staff": True,
            },
        )
        if created:
            log.info(f"User {email} successfully created.")
        return user
