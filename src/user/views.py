from django.forms import PasswordInput
from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import Transaction, User, Form, Patient, Doctor
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from .utils import (
    MAKE_PASSWORD,
    CHECK_PASSWORD,
    IsLoggedIn,
)

# Create your views here.
from django.http import HttpResponse


def login(request):
    user = IsLoggedIn(request)
    if user is None:
        return render(request, "signin.html")
    else:
        if user.roles == "patient":
            return HttpResponseRedirect("/user/patient_dashboard")
    # return HttpResponse("Hello, world.")

def patientsignup(request):
    user = IsLoggedIn(request)
    if user is None:
        return render(request, "signup.html")
    else:
        if user.roles == "patient":
            return HttpResponseRedirect("/user/patient_dashboard")

def registerPatient(request):
    user = IsLoggedIn(request)
    if user is None:
        if request.method == "POST":
            name = request.POST.get("name")
            username = request.POST.get("username")
            roll = request.POST.get("roll")
            email = request.POST.get("email")
            designation = request.POST.get("designation")
            department = request.POST.get("department")
            password = MAKE_PASSWORD(request.POST.get("password"))
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already in use!')
                return HttpResponseRedirect("/user/signup")
            else:
                user = User(roles = "patient")
                user.name = name
                user.username = username
                user.roll = roll
                user.email = email
                user.password = password
                user.designation = designation
                user.save()
                patient = Patient(user = user, department = department)
                patient.save()
                
                messages.success(request, 'User account created successfully!')
                return HttpResponseRedirect("/user")
    else:
        return HttpResponseRedirect("/user/patient_dashboard")



def loginUser(request):
    user = IsLoggedIn(request)
    if user is None:  # user is not already login
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")
            if User.objects.filter(username=username).exists():
                user = User.objects.get(username=username)
                if CHECK_PASSWORD(password, user.password):
                    request.session["username"] = username
                    request.session.modified = True
                    # based on roles render pages
                    if user.roles == "patient":
                        return HttpResponseRedirect("/user/patient_dashboard")
                    elif user.roles == "hcadmin":
                        return HttpResponse("current login:: Welcome hcadmin,")
                    elif user.roles == "doctor":
                        return HttpResponse("current login:: Welcome doctor,")
                    elif user.roles == "accounts":
                        return HttpResponse("current login:: Welcome accounts office,")
                    else:
                        return HttpResponse("current login:: Welcome none,")
                else:
                    messages.error(request, 'Wrong username or password!')
                    return HttpResponseRedirect("/user") # redirect to login(wrong_password)
            else:
                messages.error(request, 'User does not exist!')
                return HttpResponseRedirect("/user")  # redirect to login(user_not_exists)
    else:
        if user.roles == "patient":
            return redirect("/user/patient_dashboard")
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
            return HttpResponseRedirect("/user")
        else:
            return HttpResponseRedirect("/user")

def patient(request):
    return render(request, 'patient_dashboard.html', {'user': IsLoggedIn(request), 'patient': Patient.objects.get(user = IsLoggedIn(request))})


def form(request):
    user = IsLoggedIn(request)
    if user is not None:
        return render(request,'form.html', {'user': IsLoggedIn(request), 'patient': Patient.objects.get(user = IsLoggedIn(request)), 'doctors': Doctor.objects.all()})
    else:
        messages.warning(request, 'Please login first to fill reimbursement form!')
        return HttpResponseRedirect("/user")
    
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
            messages.warning(request, 'Please login first to fill reimbursement form!')
            return HttpResponseRedirect("/user")