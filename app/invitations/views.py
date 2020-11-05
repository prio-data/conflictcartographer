import io
import csv
import json

import pydantic

from django.shortcuts import render, redirect

from django.contrib.auth import login,authenticate
from django.contrib.auth.forms import UserCreationForm 

from django.views.decorators.http import require_http_methods

from django.http import HttpResponse,HttpRequest,JsonResponse
from invitations.models import Invitation
from invitations.services import parseInviteFile,bulkCreateInvites

def referralRedirect(request,refkey):
    try:
        Invitation.objects.get(refkey = refkey)
    except Invitation.DoesNotExist:
        return HttpResponse(status = 404)
    else: 
        request.session["invitation"] = refkey
        return redirect("referralSignup")

def referralSignup(request):
    refkey = request.session.get("invitation",False)

    if not refkey:
        return HttpResponse(status = 403)

    try:
        invitation = Invitation.objects.get(refkey = refkey)
    except Invitation.DoesNotExist:
        return redirect("/")

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        form.fields["username"].initial = invitation.email
        if form.is_valid():
            form.save()

            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")

            user = authenticate(username = username, password = raw_password)
            profile = invitation.makeProfile(user)
            profile.save()

            user.email = invitation.email
            invitation.delete()
            user.save()

            login(request,user)
            return redirect("/") 
    else: 
        form = UserCreationForm()
        form.fields["username"].initial = invitation.email

    # And then
    return render(request, "registration/signup.html",
        {"form":form, "uname":invitation.email})

@require_http_methods(["POST"])
def handleExcelFile(request: HttpRequest)->HttpResponse:
    if not request.user.is_staff:
        return JsonResponse({"status":"error","messages":"permission denied"},status=403)
    try:
        datafile = request.FILES["datafile"]
    except KeyError:
        return JsonResponse({"status":"error","messages":"no file included"},status=400)

    lines = io.StringIO(datafile.read().decode())
    reader = csv.DictReader(lines)
    try:
        lines = parseInviteFile(reader)
    except pydantic.ValidationError as e:
        return JsonResponse({"status":"error","messages":str(e)})

    res = bulkCreateInvites(lines)
    res.update({"status":"success"})
    return JsonResponse(res)

def fileuploadMenu(request:HttpRequest)->HttpResponse:
    return render(request,"invitations/fileuploadMenu.html",{})
