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
                participant_count=Count("group_participants", distinct=True),
            )
            .values(
                "id",
                "username",
                "email",
                "roll_number",
                "house",
                "participant_count",
            )
        )

        return Response(users)