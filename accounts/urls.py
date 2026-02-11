from django.urls import path
from .registrations.registration_user import registrations_login
from .views.registrations_view import ViewAllRegistrations

urlpatterns = [
    path("login/registrations", registrations_login, name="registrations_login"),
    path("view/all/registrations", ViewAllRegistrations.as_view(), name="registrations_all"),


]
