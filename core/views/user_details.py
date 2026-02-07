from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

class UserDetails(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "name": user.username,
            "email": user.email,
            "roll_number": user.roll_number,
            "house": user.house,
        },        status=200
)
