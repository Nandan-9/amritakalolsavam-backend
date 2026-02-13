from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from ..permisions import IsRegistration
from registrations.models import EventRegistration
from core.models import User

class ViewAllRegistrations(APIView):
    permission_classes = [IsAuthenticated, IsRegistration]

    def get(self, request):

        registrations = (
            EventRegistration.objects
            .select_related("event", "registered_by")
            .prefetch_related("participants__user")
            .all()
        )

        
        data = []

        for reg in registrations:
            participants = [
                {
                    "id": p.user.id,
                    "roll_number": p.user.roll_number,
                    "name": p.user.get_full_name(),
                    "house": p.user.house,
                }
                for p in reg.participants.all()
            ]

            data.append({
                "registration_id": reg.id,
                "event_id": reg.event.id,
                "event_name": reg.event.name,
                "participation_mode": reg.event.participation_mode,
                "chest_number": reg.chest_number,
                "registered_by": {
                    "id": reg.registered_by.id,
                    "roll_number": reg.registered_by.roll_number,
                    "name": reg.registered_by.username,
                },
                "participants": participants
            })

        return Response({

            "total_registrations": registrations.count(),
            "results": data
        })
