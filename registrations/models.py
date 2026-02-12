from django.db import models

# Create your models here.
from django.contrib import admin
from events.models import Event
from core.models import User




class EventRegistration(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="group_registrations"
    )
    registered_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="group_registrations"
    )
    reg_time = models.DateTimeField(auto_now_add=True)
    chest_number = models.CharField(max_length=10)


    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["event", "chest_number"],
                name="unique_event_chest_number"
            ),
            models.UniqueConstraint(
                fields=["event", "registered_by"],
                name="unique_user_event_registration"
            )
        ]


class GroupParticipants(models.Model):
    registration = models.ForeignKey(
        EventRegistration,
        on_delete=models.CASCADE,
        related_name="participants"
    )
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="group_participants"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["registration", "user"],
                name="unique_user_in_registration"
            )
        ]


USER_EVENT_LIMITS = {
    ("ON", "SOLO"): 4,
    ("ON", "GROUP"): 3,
    ("OFF", "SOLO"): 4,
}
class GroupParticipantsInline(admin.TabularInline):
    model = GroupParticipants
    extra = 0
    autocomplete_fields = ["user"]
