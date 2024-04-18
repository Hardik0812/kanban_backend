from django.contrib import admin
from user.models import User, OtpModel

# Register your models here.
admin.site.register(User)
admin.site.register(OtpModel)
