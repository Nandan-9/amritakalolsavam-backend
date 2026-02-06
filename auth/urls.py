from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views.user_login import user_login

urlpatterns = [
    path("login/",user_login, name="user_login"),
    path("token/refresh/", TokenRefreshView.as_view()),
]
