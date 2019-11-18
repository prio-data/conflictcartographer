
from django.shortcuts import render, redirect

from django.contrib.auth import login,authenticate
from django.contrib.auth.forms import UserCreationForm 

from django.http import JsonResponse, HttpResponse

from django.views.decorators.csrf import csrf_exempt

from core import authentication, util

import json

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request,user)
            return(redirect("/"))
    else:
        form = UserCreationForm()
    return render(request,"registration/signup.html",{"form":form})
    
@csrf_exempt
def bulkAdd(request):
    auth = authentication.authenticateRequest(request)

    if auth and request.user.is_staff:
        # Do things
        valid = request.method =="POST"
        valid &= "data" in request.POST.keys()

        if valid:
            data = json.loads(request.POST["data"])
            result = util.bulkCreateUsers(data)
            if result:
                return HttpResponse(result, status=200)
            else:
                return HttpResponse(json.dumps(data),status = 400)
        else:
            return HttpResponse(status = 400)

    else:
        # Bounce
        return HttpResponse(status = 403)
