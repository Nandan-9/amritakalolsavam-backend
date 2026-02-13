from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views.user_login import user_login
from .azure.login import azure_login
from .azure.callback import azure_callback

urlpatterns = [
    path("login/",user_login, name="user_login"),
    path("token/refresh/", TokenRefreshView.as_view()),
    path("azure/login/",azure_login, name="azure_login"),
    path("azure/callback/",azure_callback, name="azure_callback")
]
