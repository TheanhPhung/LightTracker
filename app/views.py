from django.http import HttpResponse
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from .models import *

ACT_LIST = ["ejaculation", "porn", "masturbation"]
BONUS = 10
PENALTY = -50

def index(request):
    if request.user.is_authenticated:
        user = request.user

        for index in range(3):
            if user.action_progress(index) >= 100:
                target_field_name = ACT_LIST[index] + "_target"
                target_value = getattr(user, target_field_name)
                update_field_name = ACT_LIST[index] + "_update"
                update_value = getattr(user, update_field_name)
                if update_value == False:
                    user.update_score(BONUS)
                    setattr(user, update_field_name, True)
                    user.save()
                    messages.success(request, f"CONGRATULATIONS!!! You have completed your \"{ACT_LIST[index]} progress\" with {target_value} days. Set a new goal!")

        score_progress = user.score / user.score_by_level(user.level) * 100

        return render(request, "app/index.html", {
            "user": user,
            "no_ejaculation": user.convert_time(0),
            "no_porn": user.convert_time(1),
            "no_masturbation": user.convert_time(2),
            "ejaculation_progress": user.action_progress(0),
            "porn_progress": user.action_progress(1),
            "masturbation_progress": user.action_progress(2),
            "score_progress": score_progress 
        })

    return redirect("login")


def login_view(request):
    logout(request)
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successfull!")
            return redirect("index")

        else:
            messages.error(request, "Username or password is not valid!")

    return render(request, "app/login.html")


def register(request):
    logout(request)
    if request.method == "POST":
        username = request.POST["username"]
        if User.objects.filter(username=username):
            messsages.error(request, "Username already exists!")
            return render(request, "app/register.html")

        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            messages.error(request, "Password does not match!")
            return render(request, "app/register.html")

        user = User.objects.create_user(username=username, password=password)
        user.ejaculation_time = timezone.now()
        user.porn_time = timezone.now()
        user.masturbation_time = timezone.now()
        user.save()
        login(request, user)
        return redirect("index")

    return render(request, "app/register.html")


@login_required
def logout_view(request):
    username = request.user.username
    logout(request)
    messages.warning(request, f"You have just logged out of {username}'s account!")
    return redirect("login") 


@login_required
def relapse(request, act_code):
    if request.method == "POST":
        user = request.user
        action_field = ACT_LIST[act_code] + "_time"

        setattr(user, action_field, timezone.now())
        user.update_score(PENALTY)
        user.save()

        messages.warning(request, f"Your \"non {ACT_LIST[act_code]}\" progress has been reset!")

        return redirect("index")


@login_required
def targets(request):
    user = request.user
    return render(request, "app/targets.html", {"user": user})


@login_required
def set_target(request, act_code):
    if request.method == "POST":
        user = request.user
        new_target = request.POST["new_target"]
        target_field_name = ACT_LIST[act_code] + "_target"
        setattr(user, target_field_name, int(new_target))

        if user.action_progress(act_code) >= 100:
            messages.error(request, f"Your new target must be make your progress smaller than 100%!")
            return redirect("targets")

        update_field_name = ACT_LIST[act_code] + "_update"
        setattr(user, update_field_name, False)
        user.save()

        messages.success(request, "Set a new target successfully. Stay focused on your goal!")
    
        return redirect("index")
