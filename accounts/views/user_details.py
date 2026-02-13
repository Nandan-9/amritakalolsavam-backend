from django.db.models import Count, F
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from ..permisions import IsRegistration
from core.models import User


class ViewUsersDetails(APIView):
    permission_classes = [IsAuthenticated, IsRegistration]

    def get(self, request):

        users = (
            User.objects
            .annotate(
                registered_count=Count("group_registrations", distinct=True),
                participant_count=Count("group_participants", distinct=True),
            )
            .annotate(
                        total_events=Count("group_registrations__event",distinct=True) + Count("group_participants__registration__event",distinct=True
        )
            )
            .values(
                "id",
                "username",
                "email",
                "roll_number",
                "house",
                "registered_count",
                "participant_count",
                "total_events"
            )
        )

        return Response(users)