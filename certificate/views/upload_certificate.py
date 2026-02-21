from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.shortcuts import get_object_or_404
from registrations.helpers.get_user_events import has_user_registered
from core.models import User
from events.models import Event
from ..models import Certificate


class CertificateUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    @transaction.atomic
    def post(self, request, event_id):

        files = request.FILES.getlist("files")
        event = get_object_or_404(Event, id=event_id)
        if not files:
            return Response(
                {"error": "No files uploaded"},
                status=status.HTTP_400_BAD_REQUEST
            )

        uploaded = []
        failed = []

        for file in files:

            # Only allow PDF
            if not file.name.endswith(".pdf"):
                failed.append({"file": file.name, "reason": "Not a PDF"})
                continue

            # Extract roll number from filename
            # roll_number = file.name.replace(".pdf", "").strip()
            roll_number = file.name.rsplit("_", 1)[-1].replace(".pdf", "").strip()

            try:
                user = User.objects.get(roll_number=roll_number)
                if not has_user_registered(user,event):
                    failed.append({"file": file.name, "reason": "User not registered for event"})
                    continue

            except User.DoesNotExist:
                failed.append({"file": file.name, "reason": "User not found"})
                continue

            certificate = Certificate.objects.create(
                user=user,
                event=event,
                file=file
            )

            uploaded.append({
                "roll_number": roll_number,
                "certificate_id": certificate.id
            })

        return Response(
            {
                "event": event.name,
                "uploaded_count": len(uploaded),
                "failed_count": len(failed),
                "uploaded": uploaded,
                "failed": failed
            },
            status=status.HTTP_201_CREATED
        )
