from django.urls import path

from . import views

urlpatterns = [
    path("", views.login, name="login"),
    path("signup", views.patientsignup, name="signup"),
    path("register", views.registerPatient, name="registerPatient"),
    path("loginUser", views.loginUser, name="loginUser"),
    path("logout", views.logout, name="logout"),
    path("patient_dashboard", views.patient, name="patient"),
    path("form", views.form, name="form"),
    path("formsubmit",views.submitForm,name="formsubmit"),
]
