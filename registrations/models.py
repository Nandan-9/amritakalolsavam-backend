from django.db import models

# Create your models here.

from ..events.models import Event
from ..core.models import User




class GroupRegistration(models.Model):
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
    team_name = models.CharField(max_length=100, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["event", "registered_by"],
                name="unique_user_event_registration"
            )
        ]

    def __str__(self):
        return f"{self.team_name} - {self.event}"




class ChessNumber(models.Model):
        event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="event_chess_number"
    )
    