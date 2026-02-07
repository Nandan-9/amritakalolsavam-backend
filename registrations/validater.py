


from django.db import transaction
from django.db.models import Count
from .models import USER_EVENT_LIMITS,EventRegistration
def can_user_register(user, event):
    key = (event.stage_type, event.participation_mode)
    limit = USER_EVENT_LIMITS.get(key)

    if limit is None:
        return True

    count = (
        EventRegistration.objects
        .select_for_update()
        .filter(
            user=user,
            event__stage_type=event.stage_type,
            event__participation_mode=event.participation_mode
        )
        .count()
    )

    return count < limit
