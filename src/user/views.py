from django.shortcuts import render, redirect
from .models import User
from django.contrib.auth import logout, login, authenticate
from .utils import (
    MAKE_PASSWORD,
    CHECK_PASSWORD,
    IsLoggedIn,
)

# Create your views here.
from django.http import HttpResponse


def login(request):
    return render(request, "login.html")
    # return HttpResponse("Hello, world.")


def loginUser(request):
    if request.method == "POST":
        user = IsLoggedIn(request)
        if user is None:  # user is not already login
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = User.objects.get(username=username)
            if user is not None:
                if CHECK_PASSWORD(password, user.password):
                    request.session["username"] = username
                    request.session.modified = True
                    # based on roles render pages
                    return HttpResponse(
                        "current login:: Welcome," + user.username + user.roll
                    )
                else:
                    return render(request, "login.html")  # redirect to login
            else:
                return render(request, "login.html")  # not in database
        else:
            return HttpResponse(
                "already logged in:: Welcome," + user.username + user.roll
            )  # already logged in


def logout(request):
    if request.method == "GET":
        if IsLoggedIn(request) is not None:
            del request.session["username"]
            return render(request, "login.html")
        else:
            return render(request, "login.html")
