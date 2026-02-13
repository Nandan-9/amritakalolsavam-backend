from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.COOKIES.get("refresh_token")

            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()  # requires blacklist app enabled

        except Exception:
            pass  # even if invalid, we still clear cookie

        response = Response(
            {"detail": "Logged out successfully"},
            status=status.HTTP_200_OK
        )

        # Delete refresh cookie
        response.delete_cookie(
            key="refresh_token",
            domain=".amrita.edu.in",
        )

        return response