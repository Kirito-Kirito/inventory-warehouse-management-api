from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = [
        'username',
        'email',
        'role',
        'phone_number',
        'is_staff',
    ]
    #for edit user not only original fields but also custom field 'role' and 'phone_number'
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields' : ('role', 'phone_number')}),
    )

admin.site.register(User, CustomUserAdmin)