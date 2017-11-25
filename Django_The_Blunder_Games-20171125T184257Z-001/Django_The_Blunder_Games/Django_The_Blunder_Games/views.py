from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
import datetime
from django.utils import timezone
from Interface import Interface
from .models import HuntUser, HuntCommand


def index(request):
    return render(request, 'index.html', {"message":""})

def validate(request):

    message = "XXX"
    try:
        u = HuntUser.objects.get(name=request.POST["huntUser"])
    except HuntUser.DoesNotExist:
        message = "No user named " + request.POST["huntUser"]
    else:
        if u.password != request.POST["password"]:
            message = "Invalid password"
    if message == "XXX":
        context = {"huntUser": request.POST["huntUser"]}
        return render(request,"terminal.html",context)
    else:
        return render(request,"index.html",{"message":message})


def terminal(request):
    i = Interface.Interface()
    u = HuntUser.objects.get(name=request.POST["huntUser"])
    c = HuntCommand(text=request.POST["command"],user=u,timestamp=timezone.now())
    c.save()
    output = i.process(request.POST["command"])
    context = {"huntUser":request.POST["huntUser"],"output":output}
    return render(request, "terminal.html", context)

