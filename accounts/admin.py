"""
Accounts admin
Mostafa Rasouli
mostafarasooli54@gmail.com
feb 2024
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from accounts import models
from accounts.forms import UserCreationForm, UserChangeForm


@admin.register(models.User)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('phone', 'email', 'first_name', 'last_name', 'gender', 'age', 'marital', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (
            None,
            {'fields': ('email', 'phone', 'first_name', 'last_name', 'gender', 'age', 'marital', 'password')}
        ),
        (
            'permissions',
            {'fields': ('is_superuser', 'is_admin', 'is_active', 'groups', 'user_permissions', 'last_login',
                        'date_joined')}
        ),
    )
    add_fieldsets = (
        (
            None,
            {'fields':
                 ('phone', 'email', 'first_name', 'last_name', 'gender', 'age', 'marital', 'password1', 'password2')}
        ),
    )
    search_fields = ('phone', 'email')
    ordering = ('first_name',)
    filter_horizontal = ('groups', 'user_permissions')
    readonly_fields = ('last_login', 'date_joined')

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        if not is_superuser:
            form.base_fields['is_superuser'].disabled = True
        return form


@admin.register(models.UserOtp)
class UserOtpAdmin(admin.ModelAdmin):
    list_display = ('phone', 'otp', 'date', 'expire', 'used_date')


