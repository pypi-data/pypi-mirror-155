from django.contrib import admin

from . import models


@admin.register(models.UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    list_filter = ('role',)
