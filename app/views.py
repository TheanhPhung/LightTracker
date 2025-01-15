from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    user = request.user
    
    return render(request, "app/index.html", {"user": user})
