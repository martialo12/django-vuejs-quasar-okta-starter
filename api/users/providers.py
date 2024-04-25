import logging

from django.conf import settings
import requests
from requests_oauthlib import OAuth2Session


log = logging.getLogger(__name__)


class ProviderError(Exception):
    pass


class Provider:
    """Handler class for OIDC authentication flow."""

    def __init__(
        self,
        organization_url: str = settings.OKTA_ORG_URL,
        server_id: str = settings.OKTA_AUTHORIZATION_SERVER_ID,
        client_id: str = settings.OKTA_CLIENT_ID,
        client_secret: str = settings.OKTA_CLIENT_SECRET,
        redirect_uri: str = settings.SIGNIN_REDIRECT_URI,
        **kwargs,
    ) -> None:
        self.organization_url = organization_url
        self.server_id = server_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self._init_discovery()
        self._init_session(**kwargs)

    def _init_session(self, **kwargs) -> None:
        """Initiate an OAuth2 session with autorisation server."""
        self.session = OAuth2Session(
            client_id=self.client_id,
            scope=["profile", "email", "openid"],
            redirect_uri=self.redirect_uri,
            **kwargs,
        )

    def _init_discovery(self) -> None:
        """Retreive autorisation server metadata."""
        try:
            response = requests.get(self.discovery_endpoint)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise ProviderError(
                f"Failed to perform discovery on endpoint: {self.discovery_endpoint}"
            ) from e
        self.metadata = response.json()

    @property
    def discovery_endpoint(self) -> str:
        return "{}/oauth2/{}/.well-known/oauth-authorization-server".format(
            self.organization_url, self.server_id
        )

    @property
    def authorization_endpoint(self) -> str:
        return self.metadata.get("authorization_endpoint")

    @property
    def token_endpoint(self) -> str:
        return self.metadata.get("token_endpoint")

    @property
    def jwks_uri(self) -> str:
        return self.metadata.get("jwks_uri")

    def get_authorization_url(self) -> str:
        """
        Get Provider authorization url endpoint.

        Returns:
            str: The authorization endpoint of the provider
        """
        try:
            url, state = self.session.authorization_url(self.authorization_endpoint)
        except (OAuth2Session.OAuth2Error, requests.exceptions.RequestException) as e:
            raise ProviderError(
                f"Failed to initiate authentication: {self.token_endpoint}"
            ) from e
        return url, state

    def get_id_token(self, code: str) -> dict:
        """
        Exchange authorization code for access token.

        Returns:
            dict | None: The token obtained or None if exchange failed.
        """
        try:
            response = self.session.fetch_token(
                token_url=self.token_endpoint,
                client_secret=self.client_secret,
                code=code,
            )
        except (OAuth2Session.OAuth2Error, requests.exceptions.RequestException) as e:
            raise ProviderError(
                f"Failed to get token from endpoint: {self.token_endpoint}"
            ) from e
        return response.get("id_token")
