from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from registrations.helpers.get_user_events import get_user_events
from certificate.models import Certificate
from registrations.helpers.get_user_events import get_user_events

class UserDetails(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        registrations = get_user_events(user)

        # Fetch certificates of this user
        certificates = (
            Certificate.objects
            .filter(user=user)
            .select_related("event")
        )

        certificate_data = []

        for cert in certificates:
            certificate_data.append({
                "event_id": cert.event.id if cert.event else None,
                "event_name": cert.event.name if cert.event else None,
                "certificate_url": cert.file.url,
                "issued_at": cert.created_at
            })

        return Response({
            "name": user.username,
            "email": user.email,
            "roll_number": user.roll_number,
            "house": user.house,
            "registrations": registrations,
            "certificates": certificate_data
        }, status=200)