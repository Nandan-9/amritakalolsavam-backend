from django.http import JsonResponse
from msal import ConfidentialClientApplication
from django.conf import settings

def azure_callback(request):
    code = request.GET.get("code")

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

    if "access_token" in result:
        # Create or login user here
        return JsonResponse({"message": "Login successful"})
    
    return JsonResponse(result)