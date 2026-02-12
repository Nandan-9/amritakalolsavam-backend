from django.db import transaction, IntegrityError
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from ..models import EventRegistration, GroupParticipants
from events.models import Event
from ..validater import can_user_register
from core.helper.get_user_by_id import get_user_by_id
from students.helpers.get_students import validate_same_house
from ..helpers.get_chestnumber import generate_chest_number


class EventRegistrationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        leader = request.user
        reg_type = request.data.get("type", "solo")
        roll_numbers = request.data.get("participants", [])

        # 🔹 Leader limit check
        if not can_user_register(leader, event):
            return Response(
                {"error": "User not able to make more registrations"},
                status=400
            )

        participants = []

        # =========================
        # GROUP REGISTRATION LOGIC
        # =========================
        if reg_type == "group":

            if event.participation_mode != Event.GROUP:
                return Response(
                    {"error": "Not a group event"},
                    status=400
                )

            if not roll_numbers:
                return Response(
                    {"error": "Participants required"},
                    status=400
                )

            count = len(roll_numbers)

            if not (event.min_participants <= count <= event.max_participants):
                return Response(
                    {
                        "error": f"Participants must be between "
                                 f"{event.min_participants} and {event.max_participants}"
                    },
                    status=400
                )

            # Fetch and validate participants
            for uid in roll_numbers:
                uid = uid.strip()
                user = get_user_by_id(uid)

                if not user:
                    return Response(
                        {"error": f"User {uid} not found"},
                        status=404
                    )

                if not can_user_register(user, event):
                    return Response(
                        {"error": f"User {uid} not able to make more registrations"},
                        status=400
                    )

                participants.append(user)

            # 🔹 Prevent duplicate users inside same request
            participant_ids = [u.id for u in participants]
            if len(participant_ids) != len(set(participant_ids)):
                return Response(
                    {"error": "Duplicate participants in request"},
                    status=400
                )

            all_users = participants

            # 🔹 Same house validation
            if not validate_same_house(all_users):
                return Response(
                    {"error": "All participants must belong to the same house"},
                    status=400
                )

        else:
            # SOLO registration
            all_users = [leader]

        # =========================
        # ATOMIC REGISTRATION BLOCK
        # =========================
        try:
            with transaction.atomic():

                # 🔒 Lock existing participant rows for this event
                existing = GroupParticipants.objects.select_for_update().filter(
                    registration__event=event,
                    user__in=all_users
                ).values_list("user_id", flat=True)

                if existing.exists():
                    return Response(
                        {"error": "One or more users already registered in this event"},
                        status=409
                    )

                # Generate chest number safely
                chest_number = generate_chest_number(event)

                registration = EventRegistration.objects.create(
                    event=event,
                    registered_by=leader,
                    chest_number=chest_number,
                )

                # Store ALL users including leader
                GroupParticipants.objects.bulk_create([
                    GroupParticipants(
                        registration=registration,
                        user=user
                    )
                    for user in all_users
                ])

        except IntegrityError:
            return Response(
                {"error": "Already registered"},
                status=409
            )

        return Response(
            {"id": registration.id},
            status=201
        )
