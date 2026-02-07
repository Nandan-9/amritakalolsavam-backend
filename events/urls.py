from django.urls import path
from .views import get_all_events
from  registrations.views.register_event import EventRegistrationView

urlpatterns = [
    path("all/", get_all_events, name="get_all_events"),
    path("<int:event_id>/registrations/",EventRegistrationView.as_view(),name="event-registrations"),

]
