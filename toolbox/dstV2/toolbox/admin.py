from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyUser, AdminUser
from django.utils.translation import gettext_lazy as _

class MyUserAdmin(UserAdmin):
    model = MyUser
    list_display = ['student_id', 'level', 'is_active', 'is_staff']
    fieldsets = (
        (None, {'fields': ('student_id', 'password')}),
        (_('Personal info'), {'fields': ('level',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('student_id', 'level', 'password1', 'password2'),
        }),
    )
    search_fields = ('student_id',)
    ordering = ('student_id',)

class AdminUserAdmin(UserAdmin):
    model = AdminUser
    list_display = ['email', 'is_active', 'is_staff', 'is_superuser']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)

# Register your models here.
admin.site.register(MyUser, MyUserAdmin)
admin.site.register(AdminUser, AdminUserAdmin)
