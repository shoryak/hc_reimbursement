from django.shortcuts import render, redirect
from .models import User, Form
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
                    if user.roles=="patient":
                        return HttpResponse(
                        "current login:: Welcome patient,"
                        )
                    elif user.roles=="hcadmin":
                        return HttpResponse(
                        "current login:: Welcome hcadmin,"
                        )
                    elif user.roles=="doctor":
                        return HttpResponse(
                        "current login:: Welcome doctor,"
                        )
                    elif user.roles=="accounts":
                        return HttpResponse(
                        "current login:: Welcome accounts office,"
                        )
                    else:
                        return HttpResponse(
                        "current login:: Welcome none,"
                        )               
                    return HttpResponse(
                        "current login:: Welcome," + user.username + user.roll
                    )
                else:
                    return render(request, "login.html")  # redirect to login
            else:
                return render(request, "login.html")  # not in database
        else:
            """ return HttpResponse(
                "already logged in:: Welcome," + user.username + user.roll
            )  # already logged in """
            if user.roles=="patient":
                return HttpResponse(
                        "current loggedin:: Welcome patient,"
                )
            elif user.roles=="hcadmin":
                return HttpResponse(
                        "already loggedin:: Welcome hcadmin,"
                )
            elif user.roles=="doctor":
                return HttpResponse(
                        "already loggedin:: Welcome doctor,"
                )
            elif user.roles=="accounts":
                return HttpResponse(
                        "already loggedin:: Welcome accounts office,"
                )
            else:
                return HttpResponse(
                        "current login:: Welcome none,"
                )  


def logout(request):
    if request.method == "GET":
        if IsLoggedIn(request) is not None:
            del request.session["username"]
            return render(request, "login.html")
        else:
            return render(request, "login.html")


def form(request):
    return render(request,'form.html')
    
def submitForm(request):
    if request.method=="POST":
        # user = IsLoggedIn(request)
        # if IsLoggedIn(user) is not None:
            form= Form()
            form.userid=request.POST.get("name")
            # form.userid=user.username
            form.name=request.POST.get("name")
            form.department=request.POST.get("department")
            form.designation=request.POST.get("designation")
            # if form.is_valid():
            #     form_application=form.save(commit=False)
            form.save()
            return HttpResponse(
                "form submitted"+str(form))
                # return redirect('form_detail', pk=form.pk)
        # else:
        #     return HttpResponse(
        #         "Please login to submit a form"
        #     )