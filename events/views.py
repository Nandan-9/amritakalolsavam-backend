import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError, transaction
from django.views.decorators.http import require_GET
from django.contrib.auth import login

from .models import Event



@require_GET
def get_all_events(request):
    events = Event.objects.all().values(
        "id",
        "name",
        "description",
        "event_date",
        "event_time",
        "venue",
        "participation_mode",
    )

    return JsonResponse(
        {
            "events": list(events),
        },
        safe=False,
    )