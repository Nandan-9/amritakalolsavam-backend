import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import ensure_csrf_cookie


@csrf_exempt
def check_status_api(request):
    return JsonResponse(
    {
        "Message":"Ellam ok anu moneeee"
    },
    status=200
    )

@ensure_csrf_cookie
def get_csrf(request):
    return JsonResponse({"message": "CSRF cookie set"})
