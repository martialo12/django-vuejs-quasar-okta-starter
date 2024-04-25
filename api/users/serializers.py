from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "name")
        extra_kwargs = {
            "email": {"validators": []},
        }


class LogoutSerializer(serializers.Serializer):
    message = serializers.CharField(help_text="Logout success message")


class OidcCallbackSerializer(serializers.Serializer):
    state = serializers.CharField(required=True, allow_blank=False)
    code = serializers.CharField(required=True, allow_blank=False)
