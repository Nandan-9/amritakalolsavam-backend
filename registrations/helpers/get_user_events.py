from ..models import EventRegistration, GroupParticipants


def get_user_events(user):

    # Registrations where user is leader
    leader_regs = EventRegistration.objects.filter(
        registered_by=user
    )

    # Registrations where user is participant
    participant_regs = EventRegistration.objects.filter(
        participants__user=user
    )

    # Merge both (remove duplicates if user is both leader & participant)
    
    all_regs = (leader_regs | participant_regs).distinct()

    return list(
        all_regs.values(
            "event__id",
            "event__name",
            "event__venue",
            "event__event_date",
            "event__participation_mode",
            "chest_number",
            "registered_by__username",
        )
    )

def has_user_registered(user,event):
    leader_regs = EventRegistration.objects.filter(
        registered_by=user,
        event=event
    )

    # Registrations where user is participant
    participant_regs = EventRegistration.objects.filter(
        participants__user=user,
        event=event

    )

    # Merge both (remove duplicates if user is both leader & participant)
    
    all_regs = (leader_regs | participant_regs).distinct()

    if not all_regs :
        return False
    else :
        return True