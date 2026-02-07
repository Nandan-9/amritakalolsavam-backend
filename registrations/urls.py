from django.urls import path
from .views.home_view import EventRegistration

urlpatterns = [
    path("", EventRegistration.as_view(), name="create_registrations"),

]