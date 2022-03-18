from django.contrib import admin

# Register your models here.
from user.models import (
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

admin.site.register(User)
admin.site.register(Form)
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(HCAdmin)
admin.site.register(Accounts)
admin.site.register(Transaction)
admin.site.register(Medicine)
admin.site.register(FormMedicine)
admin.site.register(Test)
admin.site.register(FormTest)