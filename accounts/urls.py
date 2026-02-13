from django.urls import path
from .registrations.registration_user import registrations_login
from .views.registrations_view import ViewAllRegistrations
from .views.user_details import ViewUsersDetails

urlpatterns = [
    path("login/registrations", registrations_login, name="registrations_login"),
    path("view/all/registrations", ViewAllRegistrations.as_view(), name="registrations_all"),
    path("user/details/", ViewUsersDetails.as_view(), name="user_details"),
]
