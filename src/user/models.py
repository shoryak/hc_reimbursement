from django.db import models
from django.utils import timezone

# Create your models here.
# Database initilization
class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=120)
    username = models.CharField(max_length=40, unique=True)
    roll = models.CharField(max_length=6, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100, blank=False)
    contact = models.CharField(max_length=10, blank=False)
    address = models.CharField(max_length=400)
    designation = models.CharField(max_length=120)
    roles = models.CharField(max_length=10)  # patient doctor hcadmin accounts

    def __str__(self):
        return str(self.user_id)


class Patient(models.Model):
    patient_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bank_name = models.CharField(max_length=40)
    department = models.CharField(max_length=20)
    bank_IFSC = models.CharField(max_length=11)
    bank_AC = models.CharField(max_length=18)

    def __str__(self):
        return str(self.patient_id)


class Doctor(models.Model):
    doctor_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=20)

    def __str__(self):
        return str(self.doctor_id)


class HCAdmin(models.Model):
    admin_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.admin_id)


class Accounts(models.Model):
    acc_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.admin_id)


class Form(models.Model):
    form_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    patient_name = models.CharField(max_length=120)
    hc_medical_advisor = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    consultation_date = models.DateTimeField(null=True)
    referral_advisor = models.CharField(max_length=120)
    consultation_fees = models.IntegerField(default=0)
    consultation_visits = models.IntegerField(default=0)
    created_date = models.DateTimeField(default=timezone.now)

    def publish(self):
        self.created_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.form_id)


class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    reimbursement_amount = models.IntegerField()
    # Form submitted, Waiting Doctor approval, Waiting HC Admin approval, Sent to Accounts,  Approved by Accounts, Rejected
    feedback = models.CharField(max_length=400)
    created_date = models.DateTimeField(default=timezone.now)
    admin_update_date = models.DateTimeField()
    doctor_update_date = models.DateTimeField()
    account_sent_date = models.DateTimeField()
    account_approve_date = models.DateTimeField()

    def __str__(self):
        return str(self.transaction_id)


class Medicine(models.Model):
    medicine_id = models.AutoField(primary_key=True)
    medicine_name = models.CharField(max_length=50)
    brand = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return str(self.medicine_id)


class FormMedicine(models.Model):
    fm_id = models.AutoField(primary_key=True)
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return str(self.fm_id)


class Test(models.Model):
    test_id = models.AutoField(primary_key=True)
    test_name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.test_id)


class FormTest(models.Model):
    ft_id = models.AutoField(primary_key=True)
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    cost = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return str(self.ft_id)