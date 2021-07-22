from django.contrib import admin
from .models import Profile


# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'public_key')
    search_fields = ['user__username', 'public_key']


admin.site.register(Profile, CustomUserAdmin)


