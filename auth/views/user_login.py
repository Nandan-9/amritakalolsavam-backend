

import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login, authenticate
from core.models import User


@csrf_exempt
@require_POST
def user_login(request):

    try:
        data = json.loads(request.body)
        

        if not data['email'] or not data['password']:
            return JsonResponse({
                "error" : "Email and password required"
            },status=400)
        
        user_obj = User.objects.get(email=data['email'])
        if not user_obj :
            return JsonResponse(
                {"error": "Invalid credentials"},
                status=401
            )
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
        return JsonResponse(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": {
                    "user_id": user.id,
                    "roll_number": user.roll_number,
                    "email": user.email,
                    "house": user.house,
                }
            },
            status=200
        )
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
