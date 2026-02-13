

import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login, authenticate
from core.models import User


@csrf_exempt
@require_POST
def registrations_login(request):

    try:
        data = json.loads(request.body)
        

        if not data['email'] or not data['password']:
            return JsonResponse({
                "error" : "Email and password required"
            },status=400)
        
        try:
            user_obj = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            return JsonResponse({"error": "Invalid credentials"}, status=401)
        
        user = authenticate(
            request,
            username=user_obj.username,
            password=data['password']
        )

        if user is None:
            return JsonResponse(
                {"error": "Invalid credentials"},
                status=401
            )
        refresh = RefreshToken.for_user(user)
        refresh["role"] = user.role
        return JsonResponse(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            },
            status=200
        )
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
