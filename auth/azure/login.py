from msal import ConfidentialClientApplication
from django.shortcuts import redirect
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def azure_login(request):
    app = ConfidentialClientApplication(
        settings.AZURE_CLIENT_ID,
        authority=settings.AZURE_AUTHORITY,
        client_credential=settings.AZURE_CLIENT_SECRET,
    )

    auth_url = app.get_authorization_request_url(
        scopes=["User.Read"],
        redirect_uri=settings.AZURE_REDIRECT_URI,

    )

    return redirect(auth_url)