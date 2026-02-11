from django.urls import path
from .views import get_all_events
from  registrations.views.register_event import EventRegistrationView
from .google_sheets.sheet_sync import sync_events_from_sheet

urlpatterns = [
    path("all/", get_all_events, name="get_all_events"),
    path("<int:event_id>/registrations/",EventRegistrationView.as_view(),name="event-registrations"),
    path("update/", sync_events_from_sheet, name="sync_events_from_sheet"),


]
