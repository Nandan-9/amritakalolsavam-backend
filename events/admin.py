# events/admin.py
from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("id","name", "event_date", "event_time", "venue", "participation_mode")
    list_filter = ("event_date", "participation_mode")
    search_fields = ("name", "venue")
