from django.db import transaction,IntegrityError
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
        roll_numbers = request.data.get("participants", [])

        if not can_user_register(leader,event) :
            return  Response({"error": "User not able to make more registrations"}, status=400)
        
        # ---- validation ----
        if reg_type == "group":
            if event.participation_mode != Event.GROUP:
                return Response({"error": "Not a group event"}, status=400)

            if not roll_numbers:
                return Response({"error": "Participants required"}, status=400)

            participants = []
            for uid in roll_numbers:
                user = get_user_by_id(uid)
                if not user:
                    return Response({"error": f"User {uid} not found"}, status=404)
                participants.append(user)

        try:
            with transaction.atomic():
                registration = EventRegistration.objects.create(
                    event=event,
                    registered_by=leader,
                    chest_number=self.generate_chest_number(),
                )

                if reg_type == "group":
                    GroupParticipants.objects.bulk_create([
                        GroupParticipants(
                            registration=registration,
                            user=p
                        )
                        for p in participants
                    ])
        except IntegrityError:
            return Response(
                {"error": "Already registered"},
                status=409
            )

        return Response({"id": registration.id}, status=201)


    def generate_chest_number(self):
        last = EventRegistration.objects.order_by("-id").first()
        return (last.id + 1) if last else 1001
