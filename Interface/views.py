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
        u = User.objects.get(name=request.GET["User"]) #POST
    except User.DoesNotExist:
        message = "No user named " + request.GET["User"]
    else:
        if u.password != request.GET["password"]:
            message = "Invalid password"
    if message == "XXX":
        context = {"User": request.GET["User"], "Games": Game.objects.all()}
        if u.name == 'admin':
            return render(request,"terminal.html",context)
        else:
            return render(request, 'user.html', context)
    else:
        return render(request,"index.html",{"message":message})


def terminal(request):
    i = Interface.Interface()
    u = User.objects.get(name=(request.POST.get("User", "admin"))) #u = request.GET.get("User", None)
    #c = HuntCommand(text=request.POST["command"],user=u,timestamp=timezone.now())
    #c.save()
    #output = i.process(request.POST["command"],request.POST["User"])
    username = request.GET.get('User',None)
    #print("THE FIRST ELEMENT IS: " + request.GET.get('1'))
    prefix = request.GET.get('prefix',None)
    j=1
    strin = prefix.split()
    '''
    strin = prefix + " "
    print(strin)
    while request.GET.get(str(j)) != None:
        strin += request.GET.get(str(j)) + " "
        j += 1
    '''
    print(strin)
    while request.GET.get(str(j)) != None:
        strin.append(request.GET.get(str(j)))
        j += 1
    print(strin)
    i.process(strin, u)
    context = {"User":u}    #request.POST.get("User", "admin")
    return render(request, "terminal.html", context)

def users(request):
    return render(request, "user.html")