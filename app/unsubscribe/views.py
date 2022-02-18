
import logging
import base64
import binascii
import asyncio
from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.http.response import JsonResponse
from django.forms.models import model_to_dict
from django.shortcuts import redirect
from django.contrib.auth.models import User

from cc_backend_lib.clients import users_client
from cc_backend_lib import models

logger = logging.getLogger(__name__)
client = users_client.UsersClient(settings.API_URL, "users")

def unsubscribe_me(request: HttpRequest) -> HttpResponse:
    try:
        assert (key := request.GET.get("key")) is not None
        email = base64.b16decode(key.encode()).decode()
        assert (user := User.objects.filter(email = email).first()) is not None
        user_id = user.id 
    except (AssertionError, binascii.Error) as err:
        if request.user.is_authenticated:
            user_id = request.user.id
        else:
            return redirect("/") 

    result = asyncio.run(client.set_email_subscription_status(user_id, True))
    return result.either(lambda e: Response(str(e), status = 500), lambda r: JsonResponse(r.dict()))
