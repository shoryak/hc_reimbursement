from django.contrib import admin

# Register your models here.
from user.models import User, Form, Transaction, Patient, Doctor, HCAdmin

admin.site.register(User)
admin.site.register(Form)
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(HCAdmin)
admin.site.register(Transaction)
