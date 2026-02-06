from django.urls import path
from .views.home_view import check_status_api,get_csrf
from .views.user_register import user_register
from .views.user_details import UserDetails
from .views.email_otp_auth import send_otp




urlpatterns = [
    path("healthcheck/", check_status_api, name="check_status_api"),
    path("register/", user_register, name="user_register"),
    path("send-otp/", send_otp, name="send_otp"),
    path("details/", UserDetails.as_view(), name="user_details"),
    path("csrf/", get_csrf, name="get_csrf"),


]
