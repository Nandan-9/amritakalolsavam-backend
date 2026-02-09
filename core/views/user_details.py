from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from registrations.helpers.get_user_events import get_user_events
class UserDetails(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        registrations  = get_user_events(user)
        return Response({
            "name": user.username,
            "email": user.email,
            "roll_number": user.roll_number,
            "house": user.house,
            "registrations" : registrations
        },        status=200
)
