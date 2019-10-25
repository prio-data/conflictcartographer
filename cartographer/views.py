from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
import json

# Create your views here.

def cartographer(request):
    if request.method == "GET":
        context = {"data":[1,2,3,4,5]}
        return render(request,"cartographer.html",context)
    elif request.method == "POST":
        print(f"Recieved: {request.body.decode()}")
        return HttpResponse("You posted!!")
