from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views.user_login import user_login
from .azure.login import azure_login
from .azure.callback import azure_callback
from .azure.logout import LogoutView
from .token.refresh_token import CookieTokenRefreshView
urlpatterns = [
    # path("login/",user_login, name="user_login"),
    path("token/refresh/", CookieTokenRefreshView.as_view()),
    path("azure/login/",azure_login, name="azure_login"),
    path("azure/callback/",azure_callback, name="azure_callback"),
    path("logout/",LogoutView.as_view(), name="logout")
]
