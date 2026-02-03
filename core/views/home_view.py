import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt














@csrf_exempt
def check_status_api(request):
    return JsonResponse(
    {
        "Message":"Ellam ok anu moneeee"
    },
    status=200
    )