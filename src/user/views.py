from audioop import add
from django.utils import timezone
from django.forms import PasswordInput
from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import (
    User,
    Form,
    Transaction,
    Patient,
    Doctor,
    HCAdmin,
    Medicine,
    FormMedicine,
    Accounts,
    FormTest,
    Test,
)
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
        elif user.roles == "hcadmin":
            return HttpResponseRedirect("/user/hcadmin_dashboard")
        elif user.roles == "doctor":
            return HttpResponseRedirect("/user/doctor_dashboard")
        elif user.roles == "accounts":
            return HttpResponseRedirect("/user/accounts_dashboard")
        else:
            messages.error(request, "Invalid user")
            return HttpResponseRedirect("/user")


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
                messages.error(request, "Username already in use!")
                return HttpResponseRedirect("/user/signup")
            else:
                user = User(roles="patient")
                user.name = name
                user.username = username
                user.roll = roll
                user.email = email
                user.password = password
                user.designation = designation
                user.save()
                patient = Patient(user=user, department=department)
                patient.save()

                messages.success(request, "User account created successfully!")
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
                        return HttpResponseRedirect("/user/hcadmin_dashboard")
                    elif user.roles == "doctor":
                        return HttpResponseRedirect("/user/doctor_dashboard")
                    elif user.roles == "accounts":
                        return HttpResponseRedirect("/user/accounts_dashboard")
                    else:
                        messages.error(request, "Invalid user")
                        return HttpResponseRedirect("/user")
                else:
                    messages.error(request, "Wrong username or password!")
                    return HttpResponseRedirect(
                        "/user"
                    )  # redirect to login(wrong_password)
            else:
                messages.error(request, "User does not exist!")
                return HttpResponseRedirect(
                    "/user"
                )  # redirect to login(user_not_exists)
    else:
        if user.roles == "patient":
            return HttpResponseRedirect("/user/patient_dashboard")
        elif user.roles == "hcadmin":
            return HttpResponseRedirect("/user/hcadmin_dashboard")
        elif user.roles == "doctor":
            return HttpResponseRedirect("/user/doctor_dashboard")
        elif user.roles == "accounts":
            return HttpResponseRedirect("/user/accounts_dashboard")
        else:
            messages.error(request, "Invalid user")
            return HttpResponseRedirect("/user")


def logout(request):
    if request.method == "GET":
        if IsLoggedIn(request) is not None:
            del request.session["username"]
            return HttpResponseRedirect("/user")
        else:
            return HttpResponseRedirect("/user")


def patient(request):
    return render(
        request,
        "patient_dashboard.html",
        {
            "user": IsLoggedIn(request),
            "patient": Patient.objects.get(user=IsLoggedIn(request)),
        },
    )


def form(request):
    user = IsLoggedIn(request)
    if user is not None:
        return render(
            request,
            "form.html",
            {
                "user": IsLoggedIn(request),
                "patient": Patient.objects.get(user=IsLoggedIn(request)),
                "doctors": Doctor.objects.all(),
                "tests": Test.objects.all(),
                "medicines": Medicine.objects.all(),
            },
        )
    else:
        messages.warning(request, "Please login first to fill reimbursement form!")
        return HttpResponseRedirect("/user")


def submitForm(request):
    if request.method == "POST":
        user = IsLoggedIn(request)
        if IsLoggedIn(request) is not None:
            form = Form()
            form.patient = Patient.objects.get(user=IsLoggedIn(request));
            form.patient_name = request.POST.get("patient_name");
            form.relationship = request.POST.get("relationship");
            form.hc_medical_advisor = Doctor.objects.get(doctor_id=request.POST.get("hc_medical_advisor"));
            form.consultation_date = request.POST.get("con_date");
            form.referral_advisor = request.POST.get("specialist");
            form.consultation_fees = request.POST.get("con-charge");
            form.consultation_visits = request.POST.get("visits");
            form.created_date = timezone.now();
            # if form.is_valid():
            #     form_application=form.save(commit=False)
            form.save();
            no_med = int(request.POST.get("n_med"));
            no_test = int(request.POST.get("n_test"));
            for i in range(1,no_med+1):
                formmedicine = FormMedicine(form=form, medicine=Medicine.objects.get(medicine_id=request.POST.get("medicine-"+str(i))), quantity=request.POST.get("quantity-"+str(i)));
                formmedicine.save()
            for i in range(1,no_test+1):
                formtest = FormTest(form=form, test=Test.objects.get(test_id=request.POST.get("test-"+str(i))), cost=request.POST.get("charge-"+str(i)));
                formtest.save();
            transaction = Transaction(
                status="Form submitted", form=form, feedback="", created_date=timezone.now(), reimbursement_amount = request.POST.get("total")
            );
            # user feedback
            transaction.save();
            return HttpResponseRedirect("patient_dashboard")
            # return HttpResponse("form submitted" + str(form))
            # return redirect('form_detail', pk=form.pk)
        else:
            messages.warning(request, "Please login first to fill reimbursement form!")
            return HttpResponseRedirect("/user")


def doctor_dashboard_display(request):
    user = IsLoggedIn(request)
    data = {"doctor": None, "items": []}
    for d in Doctor.objects.all():
        if d.user == user:
            data["doctor"] = d
            break
    for t in Transaction.objects.all():
        if t.form.hc_medical_advisor == user:
            data["items"].append(
                {
                    "transaction": t,
                    "medicines": FormMedicine.objects.filter(form=t.form),
                    "tests": FormTest.objects.filter(form=t.form),
                }
            )

    return render(request, "doctor_dashboard.html", data)


# displaying dashboards
def patient_dashboard_display(request):
    user = IsLoggedIn(request)
    data = {"patient": None, "items": []}
    for p in Patient.objects.all():
        if p.user == user:
            data["patient"] = p
            break
    for t in Transaction.objects.all():
        if t.form.patient.user == user:
            data["items"].append(
                {
                    "transaction": t,
                    "medicines": FormMedicine.objects.filter(form=t.form),
                    "tests": FormTest.objects.filter(form=t.form),
                }
            )

    return render(request, "patient_dashboard.html", data)


def hcadmin_dashboard_display(request):
    user = IsLoggedIn(request)
    data = {"hcadmin": None, "items": []}
    for hc in HCAdmin.objects.all():
        if hc.user == user:
            data["hcadmin"] = hc
            break
    for t in Transaction.objects.all():
        data["items"].append(
            {
                "transaction": t,
                "medicines": FormMedicine.objects.filter(form=t.form),
                "tests": FormTest.objects.filter(form=t.form),
            }
        )

    return render(request, "hcadmin_dashboard.html", data)


def accounts_dashboard_display(request):
    user = IsLoggedIn(request)
    data = {"accounts": None, "items": []}
    for acc in Accounts.objects.all():
        if acc.user == user:
            data["accounts"] = acc
            break
    for t in Transaction.objects.all():
        data["items"].append(
            {
                "transaction": t,
                "medicines": FormMedicine.objects.filter(form=t.form),
                "tests": FormTest.objects.filter(form=t.form),
            }
        )
    return render(request, "accounts_dashboard.html", data)


def acceptForDoctorApproval(request):
    t_no = request.POST.get("t_no")
    if Transaction.objects.filter(transaction_id=t_no).exists():
        transaction = Transaction.objects.get(transaction_id=t_no)
        transaction.status = "Waiting Doctor approval"
        transaction.save()
        return HttpResponseRedirect("/user/hcadmin_dashboard")
    else:
        return HttpResponse("Something is wrong")


# accept, reject and view form logic
def viewRequest(request):
    pass


def acceptFormByHC(request):
    t_no = request.POST.get("t_no")
    if Transaction.objects.filter(transaction_id=t_no).exists():
        transaction = Transaction.objects.get(transaction_id=t_no)
        transaction.status = "Sent to Accounts"
        # update corresponding feedback
        transaction.account_sent_date = timezone.now()
        transaction.save()
        return HttpResponseRedirect("/user/hcadmin_dashboard")
    else:
        return HttpResponse("Something is wrong")


def rejectFormByHC(request):
    t_no = request.POST.get("t_no")
    if Transaction.objects.filter(transaction_id=t_no).exists():
        transaction = Transaction.objects.get(transaction_id=t_no)
        transaction.status = "Rejected by HC Admin"
        # update corresponding feedback
        transaction.save()
        return HttpResponseRedirect("/user/hcadmin_dashboard")
    else:
        return HttpResponseRedirect("/user/hcadmin_dashboard")


def acceptByDoctor(request):
    t_no = request.POST.get("t_no")
    if Transaction.objects.filter(transaction_id=t_no).exists():
        transaction = Transaction.objects.get(transaction_id=t_no)
        transaction.status = "Waiting HC Admin approval"
        # update corresponding feedback
        transaction.doctor_update_date = timezone.now()
        transaction.save()
        return HttpResponseRedirect("/user/doctor_dashboard")
    else:
        return HttpResponseRedirect("/user/doctor_dashboard")


def rejectByDoctor(request):
    t_no = request.POST.get("t_no")
    if Transaction.objects.filter(transaction_id=t_no).exists():
        transaction = Transaction.objects.get(transaction_id=t_no)
        transaction.status = "Rejected by Doctor"
        # update corresponding feedback
        transaction.save() 
        return HttpResponseRedirect("/user/doctor_dashboard")
    else:
        return HttpResponseRedirect("/user/doctor_dashboard")


def acceptByAccounts(request):
    t_no = request.POST.get("t_no")
    if Transaction.objects.filter(transaction_id=t_no).exists():
        transaction = Transaction.objects.get(transaction_id=t_no)
        transaction.status = "Approved by Accounts"
        # update corresponding feedback
        transaction.account_approve_date = timezone.now()
        transaction.save()
        return HttpResponseRedirect("/user/accounts_dashboard")
    else:
        return HttpResponseRedirect("/user/accounts_dashboard")


def rejectByAccounts(request):
    t_no = request.POST.get("t_no")
    if Transaction.objects.filter(transaction_id=t_no).exists():
        transaction = Transaction.objects.get(transaction_id=t_no)
        transaction.status = "Rejected by Accounts"
        # update corresponding feedback
        transaction.save()
        return HttpResponseRedirect("/user/accounts_dashboard")
    else:
        return HttpResponseRedirect("/user/accounts_dashboard")

# allowing hcadmin to register any user 
def adminsignup(request):
    user = IsLoggedIn(request)
    if user is None:
        return render(request, "signup.html")
    else:
        if user.roles == "hcadmin":
            data = {"hcadmin": None}
            for hc in HCAdmin.objects.all():
                if hc.user == user:
                    data["hcadmin"] = hc
                    break
            return render(request, "signup_admin.html", data)
        else:
            return HttpResponseRedirect("/user")

def register_any_user(request):
    user = IsLoggedIn(request)
    if user is not None:
        if request.method == "POST":
            name = request.POST.get("name")
            username = request.POST.get("username")
            roll = request.POST.get("roll")
            email = request.POST.get("email")
            designation = request.POST.get("designation")
            department = request.POST.get("department")
            password = MAKE_PASSWORD(request.POST.get("password"))
            role = request.POST.get("role")
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already in use!")
                return HttpResponseRedirect("/user/hcadmin_dashboard/signup_admin")
            elif User.objects.filter(roll=roll).exists():
                messages.error(request, "Roll Number already in use!")
                return HttpResponseRedirect("/user/hcadmin_dashboard/signup_admin")
            else:
                user = User()
                user.name = name
                user.username = username
                user.roll = roll
                user.email = email
                user.password = password
                user.designation = designation
                user.roles = role
                user.save()
                if(role == "patient"):
                    patient = Patient(user=user, department=department)
                    patient.save()
                elif(role == "doctor"):
                    doctor = Doctor(user=user)
                    doctor.save()
                elif(role == "hcadmin"):
                    hcadmin = HCAdmin(user=user)
                    hcadmin.save()
                elif(role == "accounts"):  
                    accounts = Accounts(user=user)
                    accounts.save()
                else:
                    messages.error(request, "Invalid User!")
                    return HttpResponseRedirect("/user/hcadmin_dashboard/signup_admin")

                messages.success(request, "User account created successfully!")
                return HttpResponseRedirect("/user/hcadmin_dashboard/signup_admin")
    else:
        return HttpResponseRedirect("/user")

def patient_profile(request):
    user = IsLoggedIn(request)
    if user is None:
        return HttpResponseRedirect("/user")
    else:
        data = {"patient": None}
        for p in Patient.objects.all():
            if p.user == user:
                data["patient"] = p
                break
        return render(request, "patient_profile.html", data)

def update_patient_profile(request):
    user = IsLoggedIn(request)
    if user is None:
        return HttpResponseRedirect("/user")
    else:
        if(user.roles != "patient"):
            return HttpResponseRedirect("/user")
        else:
            username = user.username
            contact = request.POST.get("contact")
            address = request.POST.get("address")
            bank_name = request.POST.get("bank_name")
            bank_IFSC = request.POST.get("bank_IFSC")
            bank_AC = request.POST.get("bank_AC")
            
            # return HttpResponse(str(username) + " " + str(contact))
            userp = User.objects.get(username=username)
            userp.contact = contact
            userp.address = address
            userp.save()

            patient = Patient.objects.get(user=user) 
            patient.bank_name=bank_name
            patient.bank_IFSC=bank_IFSC
            patient.bank_AC=bank_AC
            patient.save()
            return HttpResponseRedirect("/user/patient_dashboard/patient_profile")


# displaying dashboards
# def patient_dashboard_display(request):
#     user = IsLoggedIn(request)
#     data = {"patient": None, "items": []}
#     for p in Patient.objects.all():
#         if p.user == user:
#             data["patient"] = p
#             break
#     for t in Transaction.objects.all():
#         if t.form.patient.user == user:
#             data["items"].append(
#                 {
#                     "transaction": t,
#                     "medicines": FormMedicine.objects.filter(form=t.form),
#                     "tests": FormTest.objects.filter(form=t.form),
#                 }
#             )

#     return render(request, "patient_dashboard.html", data)


# def patientsignup(request):
#     user = IsLoggedIn(request)
#     if user is None:
#         return render(request, "signup.html")
#     else:
#         if user.roles == "patient":
#             return HttpResponseRedirect("/user/patient_dashboard")


# def registerPatient(request):
#     user = IsLoggedIn(request)
#     if user is None:
#         if request.method == "POST":
#             name = request.POST.get("name")
#             username = request.POST.get("username")
#             roll = request.POST.get("roll")
#             email = request.POST.get("email")
#             designation = request.POST.get("designation")
#             department = request.POST.get("department")
#             password = MAKE_PASSWORD(request.POST.get("password"))
#             if User.objects.filter(username=username).exists():
#                 messages.error(request, "Username already in use!")
#                 return HttpResponseRedirect("/user/signup")
#             else:
#                 user = User(roles="patient")
#                 user.name = name
#                 user.username = username
#                 user.roll = roll
#                 user.email = email
#                 user.password = password
#                 user.designation = designation
#                 user.save()
#                 patient = Patient(user=user, department=department)
#                 patient.save()

#                 messages.success(request, "User account created successfully!")
#                 return HttpResponseRedirect("/user")
#     else:
#         return HttpResponseRedirect("/user/patient_dashboard")



def viewProfile(request):
    pass
