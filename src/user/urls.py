from django.urls import path

from . import views

urlpatterns = [
    path("", views.login, name="login"),
    path("signup", views.patientsignup, name="signup"),
    path("register", views.registerPatient, name="registerPatient"),
    path("loginUser", views.loginUser, name="loginUser"),
    path("logout", views.logout, name="logout"),
    path("patient_dashboard", views.patient_dashboard_display, name="patient_dashboard_display"),
    path("doctor_dashboard", views.doctor_dashboard_display, name="doctor_dashboard_display"),
    path("hcadmin_dashboard", views.hcadmin_dashboard_display, name="hcadmin_dashboard_display"),
    path("accounts_dashboard", views.accounts_dashboard_display, name="accounts_dashboard_display"),
    path("form", views.form, name="form"),
    path("formsubmit",views.submitForm,name="formsubmit"),
    path("hcadmin_dashboard/acceptFormByHC", views.acceptFormByHC, name="acceptFormByHC"),
    path("hcadmin_dashboard/rejectFormByHC", views.rejectFormByHC, name="rejectFormByHC"),
    path("doctor_dashboard/acceptByDoctor", views.acceptByDoctor, name="acceptByDoctor"),
    path("doctor_dashboard/rejectByDoctor", views.rejectByDoctor, name="rejectByDoctor"),
    path("accounts_dashboard/acceptByAccounts", views.acceptByAccounts, name="acceptByAccounts"),
    path("accounts_dashboard/rejectByAccounts", views.rejectByAccounts, name="rejectByAccounts"),
]
