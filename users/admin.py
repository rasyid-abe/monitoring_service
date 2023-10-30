from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from users.models import User


@admin.action(description='Activate selected users')
def activate_user(modeladmin, request, queryset):
    queryset.update(is_active=True)

@admin.action(description='Deactivate selected users')
def deactivate_user(modeladmin, request, queryset):
    queryset.update(is_active=False)

@admin.action(description='Readonly = True')
def readonly_user(modeladmin, request, queryset):
    queryset.update(is_readonly=True)

@admin.action(description='Readonly = False')
def nonreadonly_user(modeladmin, request, queryset):
    queryset.update(is_readonly=False)

@admin.action(description='TAC = True')
def activate_tac(modeladmin, request, queryset):
    queryset.update(is_tac=True)

@admin.action(description='TAC = False')
def deactivate_tac(modeladmin, request, queryset):
    queryset.update(is_tac=False)

class MyUserAdmin(UserAdmin):
    model = User
    fieldsets = UserAdmin.fieldsets
    list_display = ('email', 'username', 'is_active', 'is_readonly', 'is_tac', 'is_staff', 'is_superuser')
    actions = [activate_user, deactivate_user, readonly_user, nonreadonly_user, activate_tac, deactivate_tac]

admin.site.register(User, MyUserAdmin)