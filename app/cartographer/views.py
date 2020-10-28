from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import redirect
from  django.conf import settings
#from .models import DrawnShape
import json

# Create your views here.

def cartographer(request):
    if request.user.is_authenticated:
        if request.method == "GET":

            #shapes = DrawnShape.objects.all()

            context = {#"data": serializers.serialize("json",shapes),
                    "sessionInfo": {"username":request.user.username,
                                    "isdebug":settings.DEBUG,
                                    "uk":request.user.pk}} 
            return render(request,"cartographer/index.html",context)
        elif request.method == "POST":
            #DrawnShape.objects.all().delete()
            data = request.body.decode()
            print(f"Recieved: {data} from {request.user}")
            shapes = serializers.deserialize("json",data)
            for shape in shapes: 
                shape.save()

            return HttpResponse("You posted!!")
    else:
        return redirect("accounts/login")
