import base64
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

def consent(request: HttpRequest) -> HttpResponse:
    return render(request, "consent/consent.html")

def submit_consent(request: HttpRequest) -> HttpResponse:
    came_from = request.GET.get("from")
    redirect_to = base64.b16decode(came_from).decode() if came_from else "/"
    response = redirect(redirect_to)
    response.set_cookie("privacy-consent", "true")
    return response
