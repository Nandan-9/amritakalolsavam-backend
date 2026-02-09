import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError, transaction
from django.views.decorators.http import require_POST
from django.contrib.auth import login
from ..models import User
from students.helpers.get_students import get_student_meta
@csrf_exempt
@require_POST
def user_register(request):
    try:
        data = json.loads(request.body)

        student = get_student_meta(data['roll_number'])
        if not student:
            return JsonResponse({
                "error" : "User not found"
            },status=404)

        with transaction.atomic():
            user = User.objects.create_user(
                username=student['name'],
                email=data['email'],
                password=data['password'],
                roll_number=data['roll_number'],
                house=student["house"]
            )

            login(request, user)

        return JsonResponse(
            {"message": "User registered and logged in"},
            status=201
        )

    except KeyError as e:
        return JsonResponse(
            {"error": f"Missing field: {str(e)}"},
            status=400
        )

    except IntegrityError:
        return JsonResponse(
            {"error": "Username or roll number already exists"},
            status=409
        )

    except json.JSONDecodeError:
        return JsonResponse(
            {"error": "Invalid JSON"},
            status=400
        )

    except Exception:
        return JsonResponse(
            {"error": "Something went wrong"},
            status=500
        )