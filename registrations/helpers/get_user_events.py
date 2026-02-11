

from ..models import EventRegistration


def get_user_events(user):

    registrations = EventRegistration.objects.filter(
        registered_by=user
    ).values(
        "event__id",
        "event__name",
        "event__venue",
        "chest_number",
    )

    return list(registrations)