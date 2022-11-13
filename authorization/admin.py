from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    readonly_fields = ('date_joined', 'last_login')
    fields = [field.name for field in CustomUser._meta.fields if field.name != 'id']
    list_display = ('email', 'username', 'date_joined')
    date_hierarchy = 'date_joined'


admin.site.register(CustomUser, CustomUserAdmin)