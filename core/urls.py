from django.urls import path
from .views.home_view import check_status_api

urlpatterns = [
    path("healthcheck/", check_status_api, name="check_status_api"),
]
