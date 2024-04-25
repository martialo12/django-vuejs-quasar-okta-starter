"""
URL mappings for the user API.
"""

from django.urls import path
from . import views

app_name = "user"


urlpatterns = [
    path("okta/login/", views.LoginView.as_view(), name="login"),
    path(
        "okta/callback/", views.OktaOAuth2CallbackView.as_view(), name="oauth2_callback"
    ),
    path("okta/logout/", views.LogoutView.as_view(), name="logout"),
    path("me/", views.UserInfoView.as_view(), name="me"),
]
