from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import RegisterForm
from .models import Profile


# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'public_key')


admin.site.register(Profile, CustomUserAdmin)


