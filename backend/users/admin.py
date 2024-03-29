# Register your models here.
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin


from .models import PreRegister, ChangeEmailTicket, Following


User = get_user_model()


admin.site.register(User)
admin.site.register(PreRegister)
admin.site.register(ChangeEmailTicket)
admin.site.register(Following)
