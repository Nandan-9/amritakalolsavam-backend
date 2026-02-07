from django.contrib import admin
from .models import EventRegistration,GroupParticipantsInline


@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "event",
        "registered_by",
        "chest_number",
        "reg_time",
        "participant_count",
    )

    list_filter = (
        "event",
        "event__stage_type",
        "event__participation_mode",
    )

    search_fields = (
        "registered_by__username",
        "registered_by__email",
        "chest_number",
        "event__name",
    )

    readonly_fields = (
        "reg_time",
        "chest_number",
    )

    inlines = [GroupParticipantsInline]

    autocomplete_fields = ["registered_by", "event"]

    def participant_count(self, obj):
        return obj.participants.count()

    participant_count.short_description = "Participants"
