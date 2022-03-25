from .models import User
from django.shortcuts import render, redirect, HttpResponseRedirect
from re import M
from django.contrib import messages
import bcrypt

# make new hashed password
def MAKE_PASSWORD(password):
    password = password.encode()
    hash = bcrypt.hashpw(password, bcrypt.gensalt())
    return hash.decode()


# match password to hashed one
def CHECK_PASSWORD(password, hash):
    return bcrypt.checkpw(password.encode(), hash.encode())


# check if user is already logged in or not
def IsLoggedIn(request):
    if request.session.has_key("username"):
        try:
            user = User.objects.get(username=request.session["username"])
            return user
        except:
            return None
    else:
        return None

def get_role(request):
    if request.session.has_key("username"):
        try:
            user = User.objects.get(username=request.session["username"])
            return user.roles
        except:
            return None
    else:
        return None

def role_based_redirection(request):
    role = get_role(request)
    if role == "patient":
        return "/user/patient_dashboard"
    elif role == "hcadmin":
        return "/user/hcadmin_dashboard"
    elif role == "doctor":
        return "/user/doctor_dashboard"
    elif role == "accounts":
        return "/user/accounts_dashboard"
    else:
        messages.error(request, "Role not valid!")
        return "/user/logout"