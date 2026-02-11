from django.urls import path
from .views.home_view import check_status_api
from .views.user_register import user_register
from .views.user_details import UserDetails



urlpatterns = [
    path("port/", check_status_api, name="check_status_api"),
    path("students/register/", user_register, name="user_register"),
    path("details/", UserDetails.as_view(), name="user_details"),


]
