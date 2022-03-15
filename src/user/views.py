from django.forms import PasswordInput
from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import Transaction, User, Form
from django.contrib.auth import logout, login, authenticate
from .utils import (
    MAKE_PASSWORD,
    CHECK_PASSWORD,
    IsLoggedIn,
)

# Create your views here.
from django.http import HttpResponse


def login(request):
    return render(request, "signin.html")
    # return HttpResponse("Hello, world.")

def patientsignup(request):
    return render(request, "signup.html")

def registerPatient(request):
    if request.method == "POST":
        user = IsLoggedIn(request)
        if user is None:
            name = request.POST.get("name")
            username = request.POST.get("username")
            roll = request.POST.get("roll")
            email = request.POST.get("email")
            password = MAKE_PASSWORD(request.POST.get("password"))
            if User.objects.filter(username=username).exists():
                return render(request, "signup.html")
            else:
                user = User(roles = "patient")
                user.name = name
                user.username = username
                user.roll = roll
                user.email = email
                user.password = password
                user.save()
                return render(request, "signin.html")
        else:
            return HttpResponse("current login:: Welcome patient,")



def loginUser(request):
    if request.method == "POST":
        user = IsLoggedIn(request)
        if user is None:  # user is not already login
            username = request.POST.get("username")
            password = request.POST.get("password")
            if User.objects.filter(username=username).exists():
                user = User.objects.get(username=username)
                if CHECK_PASSWORD(password, user.password):
                    request.session["username"] = username
                    request.session.modified = True
                    # based on roles render pages
                    if user.roles == "patient":
                        return HttpResponse("current login:: Welcome patient,")
                    elif user.roles == "hcadmin":
                        return HttpResponse("current login:: Welcome hcadmin,")
                    elif user.roles == "doctor":
                        return HttpResponse("current login:: Welcome doctor,")
                    elif user.roles == "accounts":
                        return HttpResponse("current login:: Welcome accounts office,")
                    else:
                        return HttpResponse("current login:: Welcome none,")
                else:
                    print("wrong_pwd")
                    return render(
                        request,
                        "login.html",
                        context={
                            "wrong_pwd": 99,
                        },
                    )  # redirect to login(wrong_password)
            else:
                print("not_in_db")
                return render(
                    request,
                    "login.html",
                    context={
                        "not_in_db": 99,
                    },
                )  # not in database
        else:
            if user.roles == "patient":
                return HttpResponse("current loggedin:: Welcome patient,")
            elif user.roles == "hcadmin":
                return HttpResponse("already loggedin:: Welcome hcadmin,")
            elif user.roles == "doctor":
                return HttpResponse("already loggedin:: Welcome doctor,")
            elif user.roles == "accounts":
                return HttpResponse("already loggedin:: Welcome accounts office,")
            else:
                return HttpResponse("current login:: Welcome none,")


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
        user = IsLoggedIn(request)
        if IsLoggedIn(request) is not None:
            form= Form()
            form.user = user
            # form.userid=user.username
            form.name=request.POST.get("name")
            form.department=request.POST.get("department")
            form.designation=request.POST.get("designation")
            # if form.is_valid():
            #     form_application=form.save(commit=False)
            form.save()
            transaction = Transaction(status = "Form submitted", form = form, user = user, feedback = "")
            # user feedback
            transaction.save()
            return HttpResponse(
                "form submitted"+str(form))
                # return redirect('form_detail', pk=form.pk)
        else:
            return HttpResponse(
                "Please login to submit a form"
                )