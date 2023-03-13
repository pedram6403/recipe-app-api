from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BasUserAdmin
from django.utils.translation import gettext as _
from . import models

class AdminUser(BasUserAdmin):
    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (
        (None, {"fields": ('email', 'password')}),
        (_('personal info'), {"fields":('name',)}),
        (_('permissions'),
        {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (_('important date'), {"fields": ('last_login',)})
    )
    add_fieldsets = (
        (None, {
            'classes':('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )
admin.site.register(models.User, AdminUser)
