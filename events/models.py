from django.db import models


class Event(models.Model):
    SOLO = "solo"
    GROUP = "group"

    PARTICIPATION_MODE_CHOICES = [
        (SOLO, "Solo"),
        (GROUP, "Group"),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    event_date = models.DateField()
    event_time = models.TimeField()
    venue = models.CharField(max_length=255)
    participation_mode = models.CharField(
        max_length=10,
        choices=PARTICIPATION_MODE_CHOICES,
        default=SOLO,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.event_date})"
