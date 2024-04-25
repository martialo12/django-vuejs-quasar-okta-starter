import logging

from django.contrib.auth import get_user_model, authenticate, login, logout
from rest_framework.exceptions import APIException, AuthenticationFailed, ParseError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer, LogoutSerializer, OidcCallbackSerializer
from .providers import Provider, ProviderError


log = logging.getLogger(__name__)

User = get_user_model()


class LoginView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            provider = Provider()
            url, state = provider.get_authorization_url()
        except ProviderError as e:
            log.error(e)
            raise APIException(detail=str(e))
        request.session["state"] = state
        return Response({"url": url})


class OktaOAuth2CallbackView(APIView):
    permission_classes = [AllowAny]
    serializer_class = OidcCallbackSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            raise ParseError(detail="Missing authorization code and/or state")

        state = serializer.validated_data["state"]
        code = serializer.validated_data["code"]

        if state != request.session.get("state"):
            raise AuthenticationFailed(detail="State value does not match")

        try:
            provider = Provider(state=state)
            id_token = provider.get_id_token(code)
        except ProviderError as e:
            raise AuthenticationFailed(detail=str(e))

        user = authenticate(
            request,
            id_token=id_token,
            client_id=provider.client_id,
            jwks_uri=provider.jwks_uri,
        )
        if not user:
            raise AuthenticationFailed(detail="Invalid access token")

        login(request, user)

        return Response(
            {
                "message": "User successfully logged in",
                "user": {"email": user.email, "name": user.name},
            }
        )


class UserInfoView(APIView):
    serializer_class = UserSerializer

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class LogoutView(APIView):
    serializer_class = LogoutSerializer

    def get(self, request):
        logout(request)
        return Response({"message": "Logout successful"})
