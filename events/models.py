from django.db import models


class Event(models.Model):
    ON_STAGE = "ON"
    OFF_STAGE = "OFF"
    SOLO = "SOLO"
    GROUP = "GROUP"
    STAGE_CHOICES = [
        (ON_STAGE, "On Stage"),
        (OFF_STAGE, "Off Stage"),
    ]
    MODE_CHOICES = [
        (SOLO, "Solo"),
        (GROUP, "Group"),
    ]
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    event_date = models.DateField(null=True, blank=True)
    event_time = models.TimeField(null=True, blank=True)
    venue = models.CharField(max_length=255, blank=True, default="")
    stage_type = models.CharField(
        max_length=3,
        choices=STAGE_CHOICES,
        default=OFF_STAGE
    )
    participation_mode = models.CharField(
        max_length=5,
        choices=MODE_CHOICES,
        default=SOLO
    )
    min_participants = models.PositiveIntegerField(default=1)
    max_participants = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
