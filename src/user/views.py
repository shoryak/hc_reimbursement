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
    role_based_redirection,
)
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

# Create your views here.
from django.http import HttpResponse

# rendered on viewing the "/user" page
def login(request): 
    user = IsLoggedIn(request)
    if user is None:  # not logged in the system
        return render(request, "signin.html")
    else:  # already logged in
        url = role_based_redirection(request)
        return HttpResponseRedirect(url)


def patientsignup(request):
    user = IsLoggedIn(request)
    if user is None:
        return render(request, "signup.html")
    else:
        url = role_based_redirection(request)
        return HttpResponseRedirect(url)


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
            password1 = request.POST.get("password")
            password2 = request.POST.get("conf_password")
            if(password1 != password2):
                messages.error(request, "Password does not match!")
                return HttpResponseRedirect("/user/signup")   
            else:
                password = MAKE_PASSWORD(password1)
                if User.objects.filter(username=username).exists():
                    messages.error(request, "Username already in use!")
                    return HttpResponseRedirect("/user/signup")
                elif User.objects.filter(roll=roll).exists():
                    messages.error(request, "User with this roll already exits!")
                    return HttpResponseRedirect("/user/signup")
                elif User.objects.filter(email=email).exists():
                    messages.error(request, "User with this email already exits!")
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
            messages.error(request, "Please fill in the credentials to sign up!")
            return HttpResponseRedirect("/user/signup")
    else: # user is already logged in 
        url = role_based_redirection(request)
        return HttpResponseRedirect(url)

# rendered when logging in using the form on login page
def loginUser(request): 
    user = IsLoggedIn(request)
    if user is None:  # user is not already logged in 
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")
            if User.objects.filter(username=username).exists(): # username exists in the dB
                user = User.objects.get(username=username)
                if CHECK_PASSWORD(password, user.password): # entered password matches with the password stored in dB
                    request.session["username"] = username
                    request.session.modified = True
                    # rendering pages based on roles
                    url = role_based_redirection(request)
                    return HttpResponseRedirect(url)
                else:
                    messages.error(request, "Incorrect password!") # password does not matches : redirect to login page 
                    return HttpResponseRedirect("/user") 
            else: # user is not registered in the database : redirect to sign up page 
                messages.error(request, "User does not exist. Kindly register yourself! ")
                return HttpResponseRedirect("/user/signup")
        else:
            messages.error(request, "Please fill in the credentials first to login in!")
            return HttpResponseRedirect("/user")
    else: # user is already logged in : redirect to the login page
        url = role_based_redirection(request)
        return HttpResponseRedirect(url)


def logout(request):
    if IsLoggedIn(request) is not None:
        del request.session["username"]
    return HttpResponseRedirect("/user/")


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
    if user is None: # not already logged in 
        messages.error(request, "Please login first to fill reimbursement form!")
        return HttpResponseRedirect("/user/logout")
    elif user.roles != "patient": # already logged in but not as patient 
        url = role_based_redirection(request)
        return HttpResponseRedirect(url) 
    else:
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

def submitForm(request):
        user = IsLoggedIn(request)
        if user is None: # not already logged in 
            messages.error(request, "Please login first to submit the reimbursement form!")
            return HttpResponseRedirect("/user/logout")
        elif user.roles != "patient": # already logged in but not as patient 
            url = role_based_redirection(request)
            return HttpResponseRedirect(url)
        else: 
            if request.method == "POST":
                form = Form()
                form.patient = Patient.objects.get(user=IsLoggedIn(request))
                form.patient_name = request.POST.get("patient_name")
                form.relationship = request.POST.get("relationship")
                form.hc_medical_advisor = Doctor.objects.get(doctor_id=request.POST.get("hc_medical_advisor"));
                form.consultation_date = request.POST.get("con_date")
                form.referral_advisor = request.POST.get("specialist")
                form.consultation_fees = request.POST.get("con-charge")
                form.consultation_visits = request.POST.get("visits")
                form.created_date = timezone.now();
                form.file = request.FILES["file"]
                # if form.is_valid():
                #     form_application=form.save(commit=False)
                form.save();
                no_med = int(request.POST.get("n_med"));
                no_test = int(request.POST.get("n_test"));
                for i in range(1,no_med+1):
                    formmedicine = FormMedicine(form=form, medicine=Medicine.objects.get(medicine_id=request.POST.get("medicine-"+str(i))), quantity=request.POST.get("quantity-"+str(i)));
                    formmedicine.save()
                for i in range(1,no_test+1):
                    formtest = FormTest(form=form, test=Test.objects.get(test_id=request.POST.get("test-"+str(i))), cost=request.POST.get("charge-"+str(i)),lab=request.POST.get("lab-"+str(i)));
                    formtest.save()
                transaction = Transaction(
                    status="Form submitted", form=form, feedback="", created_date=timezone.now(), reimbursement_amount = request.POST.get("total")
                )
                # user feedback
                transaction.save(); 
                return HttpResponseRedirect("patient_dashboard")
                # return HttpResponse("form submitted" + str(form))
                # return redirect('form_detail', pk=form.pk)
            else:
                return HttpResponseRedirect("/user")

# displaying doctor's dashboard 
def doctor_dashboard_display(request):
    user = IsLoggedIn(request)
    if user is None: # not already logged in 
        messages.error(request, "Kindly login to view the page!")
        return HttpResponseRedirect("/user/logout")
    elif user.roles != "doctor": # already logged in but not as doctor 
        url = role_based_redirection(request)
        return HttpResponseRedirect(url)
    else: # get doctor data
        data = {"doctor": None, "items": []}
        for d in Doctor.objects.all():
            if d.user == user:
                data["doctor"] = d
                break
        for t in Transaction.objects.all():
            if t.form.hc_medical_advisor.user == user:
                data["items"].append(
                    {
                        "transaction": t,
                        "medicines": FormMedicine.objects.filter(form=t.form),
                        "tests": FormTest.objects.filter(form=t.form),
                    }
                )
        return render(request, "doctor_dashboard.html", data)


# displaying patient dashboards to patient 
def patient_dashboard_display(request):
    user = IsLoggedIn(request)
    if user is None: # not already logged in 
        messages.error(request, "Kindly login to view the page!")
        return HttpResponseRedirect("/user/logout")
    elif user.roles != "patient": # already logged in but not as patient 
        url = role_based_redirection(request)
        return HttpResponseRedirect(url)
    else: # get patient data 
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

# displaying hcadmin dashboard 
def hcadmin_dashboard_display(request):
    user = IsLoggedIn(request)
    if user is None: # not already logged in 
        messages.error(request, "Kindly login to view the page!")
        return HttpResponseRedirect("/user/logout")
    elif user.roles != "hcadmin": # already logged in but not as hcadmin 
        url = role_based_redirection(request)
        return HttpResponseRedirect(url)
    else: # get hcadmin data
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
    if user is None: # not already logged in 
        messages.error(request, "Kindly login to view the page!")
        return HttpResponseRedirect("/user/logout")
    elif user.roles != "accounts": # already logged in but not as accounts 
        url = role_based_redirection(request)
        return HttpResponseRedirect(url)
    else: # get accounts data
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
    user = IsLoggedIn(request)
    if user is None: # not already logged in 
        messages.error(request, "Kindly login to view the page!")
        return HttpResponseRedirect("/user/logout")
    elif user.roles != "hcadmin": # already logged in but not as hcadmin 
        url = role_based_redirection(request)
        return HttpResponseRedirect(url)
    else:
        if request.method == "POST":
            t_no = request.POST.get("t_no")
            feedback = request.POST.get("feedback")
            if Transaction.objects.filter(transaction_id=t_no).exists():
                transaction = Transaction.objects.get(transaction_id=t_no)
                transaction.status = "Waiting Doctor approval"
                transaction.feedback = feedback
                transaction.admin_update_date = timezone.now()
                transaction.save()
                return HttpResponseRedirect("/user/hcadmin_dashboard")
            else:
                messages.error(request, "Transaction ID does not exists!")
                return HttpResponseRedirect("/user")
        else:
            messages.error(request, "Kindly login to view the page!")
            return HttpResponseRedirect("/user")


def acceptFormByHC(request):
    user = IsLoggedIn(request)
    if user is None: # not already logged in 
        messages.error(request, "Kindly login to view the page!")
        return HttpResponseRedirect("/user/logout")
    elif user.roles != "hcadmin": # already logged in but not as hcadmin 
        url = role_based_redirection(request)
        return HttpResponseRedirect(url)
    else:
        if request.method == "POST":
            t_no = request.POST.get("t_no")
            feedback = request.POST.get("feedback")
            if Transaction.objects.filter(transaction_id=t_no).exists():
                transaction = Transaction.objects.get(transaction_id=t_no)
                transaction.status = "Sent to Accounts"
                transaction.feedback = feedback
                transaction.account_sent_date = timezone.now()
                transaction.save()
                return HttpResponseRedirect("/user/hcadmin_dashboard")
            else:
                messages.error(request, "Transaction ID does not exists!")
                return HttpResponseRedirect("/user")
        else:
            messages.error(request, "Kindly login to view the page!")
            return HttpResponseRedirect("/user")

def rejectFormByHC(request):
    user = IsLoggedIn(request)
    if user is None: # not already logged in 
        messages.error(request, "Kindly login to view the page!")
        return HttpResponseRedirect("/user/logout")
    elif user.roles != "hcadmin": # already logged in but not as hcadmin 
        url = role_based_redirection(request)
        return HttpResponseRedirect(url)
    else:
        if request.method == "POST":
            t_no = request.POST.get("t_no")
            feedback = request.POST.get("feedback")
            if Transaction.objects.filter(transaction_id=t_no).exists():
                transaction = Transaction.objects.get(transaction_id=t_no)
                if(transaction.status == "Waiting HC Admin approval"):
                    transaction.status = "Rejected by HC Admin after Doctor Verification"
                else:
                    transaction.status = "Rejected by HC Admin"
                transaction.feedback = feedback
                transaction.admin_update_date = timezone.now()
                transaction.save()
                return HttpResponseRedirect("/user/hcadmin_dashboard")
            else:
                messages.error(request, "Transaction ID does not exists!")
                return HttpResponseRedirect("/user")
        else:
            messages.error(request, "Kindly login to view the page!")
            return HttpResponseRedirect("/user")


def acceptByDoctor(request):
    user = IsLoggedIn(request)
    if user is None: # not already logged in 
        messages.error(request, "Kindly login to view the page!")
        return HttpResponseRedirect("/user/logout")
    elif user.roles != "doctor": # already logged in but not as doctor 
        url = role_based_redirection(request)
        return HttpResponseRedirect(url)
    else:
        if request.method == "POST":
            t_no = request.POST.get("t_no")
            feedback = request.POST.get("feedback")
            if Transaction.objects.filter(transaction_id=t_no).exists():
                transaction = Transaction.objects.get(transaction_id=t_no)
                transaction.status = "Waiting HC Admin approval"
                transaction.feedback = feedback
                transaction.doctor_update_date = timezone.now()
                transaction.save()
                return HttpResponseRedirect("/user/doctor_dashboard")
            else:
                messages.error(request, "Transaction ID does not exists!")
                return HttpResponseRedirect("/user")
        else:
            messages.error(request, "Kindly login to view the page!")
            return HttpResponseRedirect("/user")


def rejectByDoctor(request):
    user = IsLoggedIn(request)
    if user is None: # not already logged in 
        messages.error(request, "Kindly login to view the page!")
        return HttpResponseRedirect("/user/logout")
    elif user.roles != "doctor": # already logged in but not as doctor 
        url = role_based_redirection(request)
        return HttpResponseRedirect(url)
    else:
        if request.method == "POST":
            t_no = request.POST.get("t_no")
            feedback = request.POST.get("feedback")
            if Transaction.objects.filter(transaction_id=t_no).exists():
                transaction = Transaction.objects.get(transaction_id=t_no)
                transaction.status = "Rejected by Doctor"
                transaction.feedback = feedback
                transaction.doctor_update_date = timezone.now();
                transaction.save()
                return HttpResponseRedirect("/user/doctor_dashboard")
            else:
                messages.error(request, "Transaction ID does not exists!")
                return HttpResponseRedirect("/user")
        else:
            messages.error(request, "Kindly login to view the page!")
            return HttpResponseRedirect("/user")


def acceptByAccounts(request):
    user = IsLoggedIn(request)
    if user is None: # not already logged in 
        messages.error(request, "Kindly login to view the page!")
        return HttpResponseRedirect("/user/logout")
    elif user.roles != "accounts": # already logged in but not as doctor 
        url = role_based_redirection(request)
        return HttpResponseRedirect(url)
    else:
        if request.method == "POST":
            t_no = request.POST.get("t_no")
            feedback = request.POST.get("feedback")
            if Transaction.objects.filter(transaction_id=t_no).exists():
                transaction = Transaction.objects.get(transaction_id=t_no)
                transaction.status = "Approved by Accounts"
                transaction.feedback = feedback
                transaction.account_approve_date = timezone.now()
                transaction.save()
                return HttpResponseRedirect("/user/accounts_dashboard")
            else:
                messages.error(request, "Transaction ID does not exists!")
                return HttpResponseRedirect("/user")
        else:
            messages.error(request, "Kindly login to view the page!")
            return HttpResponseRedirect("/user")



def rejectByAccounts(request):
    user = IsLoggedIn(request)
    if user is None: # not already logged in 
        messages.error(request, "Kindly login to view the page!")
        return HttpResponseRedirect("/user/logout")
    elif user.roles != "accounts": # already logged in but not as doctor 
        url = role_based_redirection(request)
        return HttpResponseRedirect(url)
    else:
        if request.method == "POST":
            t_no = request.POST.get("t_no")
            feedback = request.POST.get("feedback")
            if Transaction.objects.filter(transaction_id=t_no).exists():
                transaction = Transaction.objects.get(transaction_id=t_no)
                transaction.status = "Rejected by Accounts"
                transaction.feedback = feedback
                transaction.account_approve_date = timezone.now()
                transaction.save()
                return HttpResponseRedirect("/user/accounts_dashboard")
            else:
                messages.error(request, "Transaction ID does not exists!")
                return HttpResponseRedirect("/user")
        else:
            messages.error(request, "Kindly login to view the page!")
            return HttpResponseRedirect("/user")


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
    if user is None: # not already logged in 
        messages.error(request, "Kindly login to view the page!")
        return HttpResponseRedirect("/user/logout")
    elif user.roles != "hcadmin": # already logged in but not as hcadmin 
        url = role_based_redirection(request)
        return HttpResponseRedirect(url)
    else:
        if request.method == "POST":
            name = request.POST.get("name")
            username = request.POST.get("username")
            roll = request.POST.get("roll")
            email = request.POST.get("email")
            designation = request.POST.get("designation")
            department = request.POST.get("department")
            password1 = request.POST.get("password")
            password2 = request.POST.get("conf_password")
            if(password1 != password2):
                messages.error(request, "Password does not match!")
                return HttpResponseRedirect("/user/hcadmin_dashboard/signup_admin")   
            else:
                password = MAKE_PASSWORD(request.POST.get("password"))
                role = request.POST.get("role")
                if User.objects.filter(username=username).exists():
                    messages.error(request, "Username already in use!")
                    return HttpResponseRedirect("/user/hcadmin_dashboard/signup_admin")
                elif User.objects.filter(roll=roll).exists():
                    messages.error(request, "Roll Number already in use!")
                    return HttpResponseRedirect("/user/hcadmin_dashboard/signup_admin")
                elif User.objects.filter(email=email).exists():
                    messages.error(request, "User with this email already exits!")
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
                    if role == "patient":
                        patient = Patient(user=user, department=department)
                        patient.save()
                    elif role == "doctor":
                        doctor = Doctor(user=user)
                        doctor.save()
                    elif role == "hcadmin":
                        hcadmin = HCAdmin(user=user)
                        hcadmin.save()
                    elif role == "accounts":
                        accounts = Accounts(user=user)
                        accounts.save()
                    else:
                        messages.error(request, "Invalid User!")
                        return HttpResponseRedirect("/user/hcadmin_dashboard/signup_admin")

                    messages.success(request, "User account created successfully!")
                    return HttpResponseRedirect("/user/hcadmin_dashboard/signup_admin")
        else:
            messages.error(request, "Kindly login to view the page!")
            return HttpResponseRedirect("/user")


def patient_profile(request):
    user = IsLoggedIn(request)
    if user is None:
        return HttpResponseRedirect("/user")
    else:
        if user.roles == "patient":
            data = {"patient": None}
            for p in Patient.objects.all():
                if p.user == user:
                    data["patient"] = p
                    break
            return render(request, "patient_profile.html", data)
        else:
            messages.error(request, "Kindly login to view the page!")
            return HttpResponseRedirect("/user")


def update_patient_profile(request):
    user = IsLoggedIn(request)
    if user is None: # not already logged in 
        messages.error(request, "Kindly login to view the page!")
        return HttpResponseRedirect("/user/logout")
    elif user.roles != "patient": # already logged in but not as patient 
        url = role_based_redirection(request)
        return HttpResponseRedirect(url)
    else:
        if request.method == "POST":
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
            patient.bank_name = bank_name
            patient.bank_IFSC = bank_IFSC
            patient.bank_AC = bank_AC
            patient.save()
            messages.success(request, "Profile Succesfully Updated!")
            return HttpResponseRedirect("/user/patient_dashboard/patient_profile")
        else:
            messages.error(request, "Kindly login to view the page!")
            return HttpResponseRedirect("/user")



def doctor_profile(request):
    user = IsLoggedIn(request)
    if user is None: # not already logged in 
        messages.error(request, "Kindly login to view the page!")
        return HttpResponseRedirect("/user/logout")
    elif user.roles != "doctor": # already logged in but not as doctor 
        url = role_based_redirection(request)
        return HttpResponseRedirect(url)
    else:
        data = {"doctor": None}
        for p in Doctor.objects.all():
            if p.user == user:
                data["doctor"] = p
                break
        return render(request, "doctor_profile.html", data)


def update_doctor_profile(request):
    user = IsLoggedIn(request)
    if user is None: # not already logged in 
        messages.error(request, "Kindly login to view the page!")
        return HttpResponseRedirect("/user/logout")
    elif user.roles != "doctor": # already logged in but not as doctor 
        url = role_based_redirection(request)
        return HttpResponseRedirect(url)
    else:
        if request.method == "POST":
            username = user.username
            contact = request.POST.get("contact")
            address = request.POST.get("address")
            specialization = request.POST.get("specialization")

            # return HttpResponse(str(username) + " " + str(contact))
            userp = User.objects.get(username=username)
            userp.contact = contact
            userp.address = address
            userp.save()

            doctor = Doctor.objects.get(user=user)
            doctor.specialization = specialization
            doctor.save()
            messages.success(request, "Profile Succesfully Updated!")
            return HttpResponseRedirect("/user/doctor_dashboard/doctor_profile")
        else:
            messages.error(request, "Kindly login to view the page!")
            return HttpResponseRedirect("/user")



def hcadmin_profile(request):
    user = IsLoggedIn(request)
    if user is None: # not already logged in 
        messages.error(request, "Kindly login to view the page!")
        return HttpResponseRedirect("/user/logout")
    elif user.roles != "hcadmin": # already logged in but not as hcadmin 
        url = role_based_redirection(request)
        return HttpResponseRedirect(url)
    else:
        data = {"hcadmin": None}
        for p in HCAdmin.objects.all():
            if p.user == user:
                data["hcadmin"] = p
                break
        return render(request, "hcadmin_profile.html", data)

def med_and_test(request):
    user = IsLoggedIn(request)
    if user is None: # not already logged in 
        messages.error(request, "Kindly login to view the page!")
        return HttpResponseRedirect("/user/logout")
    elif user.roles != "hcadmin": # already logged in but not as hcadmin 
        url = role_based_redirection(request)
        return HttpResponseRedirect(url)
    else:
        data = {"hcadmin": None, "med_items": [], "test_items":[]}
        for p in HCAdmin.objects.all():
            if p.user == user:
                data["hcadmin"] = p
                break
        for med in Medicine.objects.all():
            data["med_items"].append(
                {
                    "medicine_name": med.medicine_name,
                    "brand": med.brand,
                    "price": med.price,
                }
            )
        for test in Test.objects.all():
            data["test_items"].append(
                {
                    "test_name": test.test_name,
                }
            )
        return render(request, "med_and_test.html", data)

def add_medicine(request):
    user = IsLoggedIn(request)
    if user is None: # not already logged in 
        messages.error(request, "Kindly login to view the page!")
        return HttpResponseRedirect("/user/logout")
    elif user.roles != "hcadmin": # already logged in but not as hcadmin 
        url = role_based_redirection(request)
        return HttpResponseRedirect(url)
    else:
        if request.method == "POST":
            if Medicine.objects.filter(medicine_name=request.POST.get("med_name"), brand=request.POST.get("med_brand"), price = request.POST.get("med_price")).exists():
                messages.error(request, "Medicine already exists!")
                return HttpResponseRedirect("/user/hcadmin_dashboard/med_and_test")
            else:
                med = Medicine()
                med.medicine_name = request.POST.get("med_name")
                med.brand = request.POST.get("med_brand")
                med.price = request.POST.get("med_price")
                med.save()

                messages.success(request, "Medicine added successfully")
                return HttpResponseRedirect("/user/hcadmin_dashboard/med_and_test")
        else:
            messages.error(request, "Kindly login to view the page!")
            return HttpResponseRedirect("/user")

def delete_medicine(request):
    user = IsLoggedIn(request)
    if user is None: # not already logged in 
        messages.error(request, "Kindly login to view the page!")
        return HttpResponseRedirect("/user/logout")
    elif user.roles != "hcadmin": # already logged in but not as hcadmin 
        url = role_based_redirection(request)
        return HttpResponseRedirect(url)
    else:
        if request.method == "POST":
            Medicine.objects.filter(medicine_name=request.POST.get("med_name"), brand=request.POST.get("med_brand"), price = request.POST.get("med_price")).delete()
            messages.success(request, "Medicine deleted successfully")
            return HttpResponseRedirect("/user/hcadmin_dashboard/med_and_test")
        else:
            messages.error(request, "Kindly login to view the page!")
            return HttpResponseRedirect("/user")

def add_test(request):
    user = IsLoggedIn(request)
    if user is None: # not already logged in 
        messages.error(request, "Kindly login to view the page!")
        return HttpResponseRedirect("/user/logout")
    elif user.roles != "hcadmin": # already logged in but not as hcadmin 
        url = role_based_redirection(request)
        return HttpResponseRedirect(url)
    else:
        if request.method == "POST":
            if Test.objects.filter(test_name=request.POST.get("test_name")).exists():
                messages.error(request, "Test already exists!")
                return HttpResponseRedirect("/user/hcadmin_dashboard/med_and_test")
            else:
                test = Test()
                test.test_name = request.POST.get("test_name")
                test.save()

                messages.success(request, "Test added successfully")
                return HttpResponseRedirect("/user/hcadmin_dashboard/med_and_test")
        else:
            messages.error(request, "Kindly login to view the page!")
            return HttpResponseRedirect("/user")


def delete_test(request):
    user = IsLoggedIn(request)
    if user is None: # not already logged in 
        messages.error(request, "Kindly login to view the page!")
        return HttpResponseRedirect("/user/logout")
    elif user.roles != "hcadmin": # already logged in but not as hcadmin 
        url = role_based_redirection(request)
        return HttpResponseRedirect(url)
    else:
        if request.method == "POST":
            Test.objects.filter(test_name=request.POST.get("test_name")).delete()
            messages.success(request, "Test deleted successfully")
            return HttpResponseRedirect("/user/hcadmin_dashboard/med_and_test")
        else:
            messages.error(request, "Kindly login to view the page!")
            return HttpResponseRedirect("/user")

def update_hcadmin_profile(request):
    user = IsLoggedIn(request)
    if user is None: # not already logged in 
        messages.error(request, "Kindly login to view the page!")
        return HttpResponseRedirect("/user/logout")
    elif user.roles != "hcadmin": # already logged in but not as hcadmin 
        url = role_based_redirection(request)
        return HttpResponseRedirect(url)
    else:
        if request.method == "POST":
            username = user.username
            contact = request.POST.get("contact")
            address = request.POST.get("address")

            # return HttpResponse(str(username) + " " + str(contact))
            userp = User.objects.get(username=username)
            userp.contact = contact
            userp.address = address
            userp.save()
            messages.success(request, "Profile Succesfully Updated!")
            return HttpResponseRedirect("/user/hcadmin_dashboard/hcadmin_profile")
        else:
            messages.error(request, "Kindly login to view the page!")
            return HttpResponseRedirect("/user")



def accounts_profile(request):
    user = IsLoggedIn(request)
    if user is None: # not already logged in 
        messages.error(request, "Kindly login to view the page!")
        return HttpResponseRedirect("/user/logout")
    elif user.roles != "accounts": # already logged in but not as accounts 
        url = role_based_redirection(request)
        return HttpResponseRedirect(url)
    else:
        data = {"accounts": None}
        for p in Accounts.objects.all():
            if p.user == user:
                data["accounts"] = p
                break
        return render(request, "accounts_profile.html", data)


def update_accounts_profile(request):
    user = IsLoggedIn(request)
    if user is None: # not already logged in 
        messages.error(request, "Kindly login to view the page!")
        return HttpResponseRedirect("/user/logout")
    elif user.roles != "accounts": # already logged in but not as accounts 
        url = role_based_redirection(request)
        return HttpResponseRedirect(url)
    else:
        if request.method == "POST":
            username = user.username
            contact = request.POST.get("contact")
            address = request.POST.get("address")

            # return HttpResponse(str(username) + " " + str(contact))
            userp = User.objects.get(username=username)
            userp.contact = contact
            userp.address = address
            userp.save()

            messages.success(request, "Profile Succesfully Updated!")
            return HttpResponseRedirect("/user/accounts_dashboard/accounts_profile")
        else:
            messages.error(request, "Kindly login to view the page!")
            return HttpResponseRedirect("/user")


class UploadView(CreateView):
    model = Form
    fields = ['file', ]
    success_url = reverse_lazy('fileupload')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['documents'] = Form.objects.all()
        return context
