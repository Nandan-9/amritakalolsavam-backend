from django.urls import path
from .views.home_view import check_status_api,get_csrf
from .views.user_register import user_register
from .views.user_auth import user_login


urlpatterns = [
    path("healthcheck/", check_status_api, name="check_status_api"),
    path("register/", user_register, name="user_register"),
    path("login/", user_login, name="user_login"),
    path("csrf/", get_csrf, name="get_csrf"),


]
