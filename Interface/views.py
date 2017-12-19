from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
import datetime
from django.utils import timezone
from django.db import IntegrityError
from Interface import Interface
from .models import User, HuntCommand, Game, Landmarks


def index(request):
    return render(request, 'index.html', {"message":""})

def sess(request):
    request.session['User'] = request.POST["User"]
    request.session['password'] = request.POST["password"]
    request.session.modified = True
    return validate(request)

def validate(request):
    message = "XXX"
    try:
        u = User.objects.get(name=request.session.get('User')) #POST

    except User.DoesNotExist:
        message = "No user named " + request.session.get('User')
        return render(request, "index.html", {"message": message})
    else:
        if u.password != request.session.get("password"):
            message = "Invalid password"
    try:
       l = Landmarks.objects.filter(game=u.game)#.order_by('position')
       l = l.values()
       curL = Landmarks.objects.get(game=u.game,position=u.currentLandmark)
    except Landmarks.DoesNotExist:
        #message = "No landmarks"
        curL = None
    if message == "XXX":
        context = {"User": request.session.get('User'), "Games": Game.objects.all(), "curUser": u, "landList":l, "currentLm":curL}
        if u.name == 'admin':
            return render(request,"terminal.html",context)
        else:
            return render(request, 'user.html', context)
    else:
        return render(request,"index.html",{"message":message})


def terminal(request):
    i = Interface.Interface()
    u = User.objects.get(name='admin')
    #u = User.objects.get(name=(request.POST.get("User", 'admin'))) !!!!!!!!!!!!!!Don't supply with default value 'admin', needs rework
    strin = request.POST.get('prefix').split()
    j=1
    while request.POST.get(str(j)) != None:
        strin.append(request.POST.get(str(j)))
        j += 1
    print(strin)
    try:
        i.process(strin, u)
    except IntegrityError:
        pass
    context = {"User": u, "Games": Game.objects.all()}
    return render(request, "terminal.html", context)


#WIP
def user(request):
    i = Interface.Interface()
    #passw = request.session['password']
    u = User.objects.get(name=request.session.get('User'))#username)   request.POST.get("User")
    user = request.session.get('User')
    try:
        l = Landmarks.objects.filter(game=u.game)#.order_by('position')
        l = l.values()
        curL = Landmarks.objects.get(game=u.game,position=u.currentLandmark)
    except Landmarks.DoesNotExist:
        l=[]
        curL = None
    #u = User.objects.get(name=(request.GET.get("User")))
    prefix = request.POST.get('prefix')
    j = 1
    strin = prefix.split()
    while request.POST.get(str(j)) != None:
        strin.append(request.POST.get(str(j)))
        j += 1
    i.process(strin, u)
    #context = {"User": u}
    context = {"User": User, "Games": Game.objects.all(), "curUser": u, "landList": l, "currentLm": curL}
    return render(request, "user.html", context)