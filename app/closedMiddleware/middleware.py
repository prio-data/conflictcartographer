
from django.conf import settings
from django.shortcuts import redirect
from django.http import HttpResponse

def check_active(get_response):
    def middleware(request):
        try:
            if not request.path == "/closed/" and not settings.ACTIVE:
                    return redirect("closed")
            return get_response(request)
        except Exception as e:
            return HttpResponse(str(e))
    return middleware
