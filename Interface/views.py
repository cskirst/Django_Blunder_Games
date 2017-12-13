from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
import datetime
from django.utils import timezone
from Interface import Interface
from .models import User, HuntCommand, Game


def index(request):
    return render(request, 'index.html', {"message":""})

def validate(request):

    message = "XXX"
    try:
        u = User.objects.get(name=request.POST["User"])
    except User.DoesNotExist:
        message = "No user named " + request.POST["User"]
    else:
        if u.password != request.POST["password"]:
            message = "Invalid password"
    if message == "XXX":
        context = {"User": request.POST["User"], "Games": Game.objects.all()}
        if u.name == 'admin':
            return render(request,"terminal.html",context)
        else:
            return render(request, 'user.html', context)
    else:
        return render(request,"index.html",{"message":message})


def terminal(request):
    i = Interface.Interface()
    u = User.objects.get(name=request.POST["User"])
    c = HuntCommand(text=request.POST["command"],user=u,timestamp=timezone.now())
    c.save()
    output = i.process(request.POST["command"],request.POST["User"])
    context = {"User":request.POST["User"],"output":output}
    return render(request, "terminal.html", context)

def users(request):
    return render(request, "user.html")