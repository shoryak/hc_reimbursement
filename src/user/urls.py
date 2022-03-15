from django.urls import path

from . import views

urlpatterns = [
    path("", views.login, name="login"),
    path("loginUser", views.loginUser, name="loginUser"),
    path("logout", views.logout, name="logout"),
    path("form", views.form, name="form"),
    path("formsubmit",views.submitForm,name="formsubmit"),
]
