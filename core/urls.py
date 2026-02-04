from django.urls import path
from .views.home_view import check_status_api
from .views.user_register import user_register

urlpatterns = [
    path("healthcheck/", check_status_api, name="check_status_api"),
    path("register/", user_register, name="user_register"),
]
