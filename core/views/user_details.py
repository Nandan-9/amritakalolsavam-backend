from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


@login_required(login_url=None)
def user_details(request):
    user = request.user

    return JsonResponse(
        {
            "name": user.username,
            "email": user.email,
            "roll_number": user.roll_number,
            "house": user.house,
        },
        status=200
    )