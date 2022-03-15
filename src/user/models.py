from django.db import models
from django.utils import timezone

# Create your models here.
# Database initilization
class User(models.Model):
    user_id = models.AutoField(primary_key = True)
    name = models.CharField(max_length=120)
    username = models.CharField(max_length=40, unique=True)
    roll = models.CharField(max_length=10, unique=True)
    email = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100, null=True, blank=True)
    roles = models.CharField(max_length=10)  # patient doctor hcadmin accounts

    def __str__(self):
        return str(self.user_id)

class Form(models.Model):
    form_id = models.AutoField(primary_key = True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null = True)
    name = models.CharField(max_length=120)
    designation = models.CharField(max_length=120)
    department = models.CharField(max_length=120)
    # residence = models.CharField(max_length=120)
    # hc_medical_advisor = models.CharField(max_length=120)
    # referral_medical_advisor = models.CharField(max_length=120)
    # consultation_number = models.IntegerField()
    # consulation_fees = models.IntegerField()
    created_date = models.DateTimeField(default=timezone.now)

    def publish(self):
        self.created_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.form_id)


class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    # Form submitted, Waiting Doctor approval, Waiting HC Admin approval, Sent to Accounts,  Approved by Accounts
    feedback = models.CharField(max_length=400)

    def __str__(self):
        return str(self.transaction_id)

    
