from django.db import transaction
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from ..models import EventRegistration, GroupParticipants
from events.models import Event
from ..validater import can_user_register
from core.helper.get_user_by_id import get_user_by_id


class EventRegistrationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        leader = request.user
        reg_type = request.data.get("type", "solo")
        user_ids = request.data.get("user_ids", [])

        if reg_type == "group" and event.participation_mode != Event.GROUP:
            return Response({"error": "This is not a group event"}, status=400)

        if reg_type == "solo" and event.participation_mode != Event.SOLO:
            return Response({"error": "This is not a solo event"}, status=400)

        if not can_user_register(leader, event):
            return Response(
                {"error": "Registration limit reached"},
                status=403
            )

        with transaction.atomic():
            registration = EventRegistration.objects.create(
                event=event,
                registered_by=leader,
                chest_number=self.generate_chest_number(),
            )

            if reg_type == "group":
                if not user_ids:
                    return Response(
                        {"error": "Group participants required"},
                        status=400
                    )

                for user_id in user_ids:
                    participant = get_user_by_id(user_id)
                    if not participant:
                        return Response(
                            {"error": f"User {user_id} not found"},
                            status=404
                        )
                    GroupParticipants.objects.create(
                        registration=registration,
                        user=participant
                    )
        return Response(
            {"id": registration.id},
            status=201
        )

    def generate_chest_number(self):
        last = EventRegistration.objects.order_by("-id").first()
        return (last.id + 1) if last else 1001
