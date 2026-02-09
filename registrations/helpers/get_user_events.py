

from ..models import EventRegistration


def get_user_events(user):

    registration = EventRegistration.objects.all().values(
        "event",
        "chest_number"

    )
    if not registration:
        return None
    return list(registration)