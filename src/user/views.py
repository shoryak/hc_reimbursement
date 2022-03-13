from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def login(request):
    return render(request, "login.html")
    # return HttpResponse("Hello, world.")


def loginUser(request):
    return HttpResponse("Hello, world.")
