from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import login, logout


def index(request):
    user = request.user
    
    return render(request, "app/index.html", {"user": user})


def login_view(request):
    logout(request)
    return render(request, "app/login.html")


def register(request):
    logout(request)
    return render(request, "app/register.html")


def logout_view(request):
    logout(request)
    return HttpResponse("You've logged out!")
