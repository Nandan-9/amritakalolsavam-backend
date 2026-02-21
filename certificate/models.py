# models.py
import uuid
from django.db import models
from core.models import User
from registrations.models import EventRegistration
from slugify import slugify
from events.models import Event

def certificate_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    event_name = slugify(instance.event.name)
    roll_number = instance.user.roll_number
    unique = uuid.uuid4().hex[:8]

    return f"certificates/{event_name}/{roll_number}_{unique}.{ext}"



class Certificate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="certificates")
    event = models.ForeignKey(
    Event,
    on_delete=models.CASCADE,
    related_name="certificates",
    null=True,blank=True)
    file = models.FileField(upload_to=certificate_upload_path)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "event")
