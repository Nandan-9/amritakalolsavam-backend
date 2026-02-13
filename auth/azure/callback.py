from django.http import JsonResponse
from django.db import transaction
from django.shortcuts import redirect
from django.conf import settings
from msal import ConfidentialClientApplication
from rest_framework_simplejwt.tokens import RefreshToken
from core.models import User
from students.helpers.get_students import get_student_meta


def azure_callback(request):
    code = request.GET.get("code")

    if not code:
        return JsonResponse({"error": "No authorization code"}, status=400)

    app = ConfidentialClientApplication(
        settings.AZURE_CLIENT_ID,
        authority=settings.AZURE_AUTHORITY,
        client_credential=settings.AZURE_CLIENT_SECRET,
    )

    result = app.acquire_token_by_authorization_code(
        code,
        scopes=["User.Read"],
        redirect_uri=settings.AZURE_REDIRECT_URI,
    )

    # Ensure authentication succeeded
    if "id_token_claims" not in result:
        return JsonResponse({"error": "Authentication failed"}, status=400)

    claims = result["id_token_claims"]

    # 🔒 Tenant restriction
    if claims.get("tid") != settings.AZURE_TENANT_ID:
        return JsonResponse({"error": "Unauthorized tenant"}, status=403)

    email = claims.get("preferred_username") or claims.get("email")

    if not email:
        return JsonResponse({"error": "Email not found in token"}, status=400)

    # 🔒 Restrict domain
    if not email.endswith("@am.students.amrita.edu"):
        return JsonResponse({"error": "Unauthorized email domain"}, status=403)

    # Extract roll number
    roll_number = email.split("@")[0]

    # Validate student internally
    student = get_student_meta(roll_number)

    if not student:
        return JsonResponse(
            {"error": "Student not found in system"},
            status=404
        )

    # Create or update user
    with transaction.atomic():
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "username": student["name"],
                "roll_number": roll_number,
                "house": student["house"],
            }
        )

        if created:
            user.set_unusable_password()
            user.save()
        else:
            # Sync house in case it changed
            if user.house != student["house"]:
                user.house = student["house"]
                user.save()

    # Issue JWT tokens
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    # Redirect to frontend with access token
    response = redirect(
        f"{settings.FRONTEND_URL}/auth/success?token={access_token}"
    )

    # Store refresh token securely
    response.set_cookie(
        key="refresh_token",
        value=str(refresh),
        httponly=True,
        secure=True,
        samesite="Lax",
        domain=".amrita.edu.in"  # adjust if needed
    )

    return response