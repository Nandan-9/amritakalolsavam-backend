from django.db import transaction
from django.db.models import Max
from ..models import EventRegistration


def generate_chest_number(event):
    prefix = event.prefix.upper()

    last_registration = (
        EventRegistration.objects
        .select_for_update()
        .filter(event=event)
        .order_by("-id")
        .first()
    )

    if not last_registration:
        return f"{prefix}100"

    last_number = int(last_registration.chest_number.replace(prefix, ""))
    new_number = last_number + 1

    return f"{prefix}{new_number}"
