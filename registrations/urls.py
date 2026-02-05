from django.urls import path
from .views import create_registrations

urlpatterns = [
    path("register/", create_registrations, name="create_registrations"),

]
