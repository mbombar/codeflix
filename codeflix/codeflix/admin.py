# Register your models here.

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    autocomplete_fields = ["cfuser"]


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = ["username", "first_name", "last_name", "email", "_cfuser"]

    def _cfuser(self, obj):
        return obj.profile.cfuser


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
