import csv
import io
from django.shortcuts import render,redirect
from django.http import HttpRequest,HttpResponse

from adminext.services import updateInvitations

# Create your views here.

def handleExcelFile(request: HttpRequest)->HttpResponse:
    if request.method == "GET":
        return HttpResponse("You got")
    elif request.method == "POST":
        try:
            datafile = request.FILES["datafile"]
        except KeyError:
            return redirect("/admin/")

        lines = io.StringIO(datafile.read().decode())
        reader = csv.DictReader(lines)

        resp = updateInvitations(reader)
        return render(request,"adminext/index.html",{"resp": resp})
    else:
        return HttpResponse(status_code=405)
