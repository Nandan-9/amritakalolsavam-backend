import gspread
from google.oauth2.service_account import Credentials
from django.http import JsonResponse
from ..models import Event
import os
from dotenv import load_dotenv
load_dotenv()

def sync_events_from_sheet(request):
    try:
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets.readonly",
        ]

        cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "/app/cred.json")

        creds = Credentials.from_service_account_file(
            cred_path,
            scopes=scopes
)
        client = gspread.authorize(creds)

        sheet = client.open_by_key(
            "1pb8BdXRjsEhJ_cF7qWXIg31uVfaE6JYPGLhF-rE3M88"
        ).sheet1

        rows = sheet.get_all_records()

        created_count = 0
        updated_count = 0

        for row in rows:
            obj, created = Event.objects.update_or_create(
                id=row.get("Event_Id"),
                defaults={
                    "name": row.get("Event_Name", "").strip(),
                    "description": row.get("Description", "") or "",
                    "event_date": row.get("event_date") or None,
                    "prefix" : row.get("prefix") or "",
                    "event_time": row.get("event_time") or None,
                    "venue": row.get("venue", "") or "",
                    "stage_type": row.get("stage_type", "OFF_STAGE"),
                    "participation_mode": row.get("participation_mode", "SOLO"),
                    "min_participants": row.get("min_participants") or 1,
                    "max_participants": row.get("max_participants") or 1,
                }
            )

            if created:
                created_count += 1
            else:
                updated_count += 1

        return JsonResponse({
            "status": "success",
            "total_rows_processed": len(rows),
            "created": created_count,
            "updated": updated_count
        })

    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e)
        }, status=500)
