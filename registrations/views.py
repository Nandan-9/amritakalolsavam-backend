import json
from django.http import JsonResponse
from django.views.decorators.http import require_GET



@require_GET
def create_registrations(request):
    return JsonResponse({
        "message" : "registations working"
    },status=200)
