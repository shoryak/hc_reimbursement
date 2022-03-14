from django.contrib import admin

# Register your models here.
from user.models import User, Form

admin.site.register(User)
admin.site.register(Form)
