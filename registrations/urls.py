from django.urls import path
from .views import get_all_events

urlpatterns = [
    path("all/", get_all_events, name="get_all_events"),

]
