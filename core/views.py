
from django.shortcuts import render, redirect

from django.contrib.auth import login,authenticate
from django.contrib.auth.forms import UserCreationForm 

from django.http import JsonResponse, HttpResponse

from django.views.decorators.csrf import csrf_exempt

from core import authentication, util
from core.models import Invitation

import json

def referralRedirect(request,refkey):
    try:
        invitation = Invitation.objects.get(refkey = refkey)
    except Invitation.DoesNotExist:
        return HttpResponse(status = 404)
    else: 
        request.session["invitation"] = refkey
        return redirect("referralSignup")

def referralSignup(request):
    refkey = request.session.get("invitation",False)

    if not refkey:
        return HttpResponse(status = 403)

    invitation = Invitation.objects.get(refkey = refkey)
    invitation.opened = True
    invitation.save()

    if invitation.registered:
        return redirect("/")

    elif request.method == "POST":
        form = UserCreationForm(request.POST)
        form.fields["username"].initial = invitation.email

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")

            user = authenticate(username = username, password = raw_password)
            user.email = invitation.email
            user.projects.set(invitation.projects.all())
            invitation.user = user

            invitation.save()
            user.save()

            login(request,user)

            invitation.registered = True
            invitation.save()
            return redirect("/") 

    else: 
        form = UserCreationForm()
        form.fields["username"].initial = invitation.email
    # And then
    return render(request, "registration/signup.html",
        {"form":form, "uname":invitation.email})

#def signup(request):
#    if request.method == "POST":
#        form = UserCreationForm(request.POST)
#        if form.is_valid():
#            form.save()
#            username = form.cleaned_data.get("username")
#            raw_password = form.cleaned_data.get("password1")
#            user = authenticate(username=username, password=raw_password)
#            login(request,user)
#            return(redirect("/"))
#    else:
#        form = UserCreationForm()
#    return render(request,"registration/signup.html",{"form":form})
    
#@csrf_exempt
#def bulkAdd(request):
    #auth = authentication.authenticateRequest(request)
#
    #if auth and request.user.is_staff:
        ## Do things
        #valid = request.method =="POST"
        #valid &= "data" in request.POST.keys()
#
        #if valid:
            #data = json.loads(request.POST["data"])
            #result = util.bulkCreateUsers(data)
            #if result:
                #return HttpResponse(result, status=200)
            #else:
                #return HttpResponse(json.dumps(data),status = 400)
        #else:
            #return HttpResponse(status = 400)
#
    #else:
        ## Bounce
        #return HttpResponse(status = 403)
