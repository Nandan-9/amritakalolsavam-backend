from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")

        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except Exception:
                pass  # token already invalid / expired

        response = Response(
            {"detail": "Logged out successfully"},
            status=status.HTTP_200_OK
        )

        # IMPORTANT: must match login cookie settings EXACTLY
        response.delete_cookie(
            key="refresh_token",
            domain=".amrita.edu.in",
            samesite="Lax",
        )

        return response