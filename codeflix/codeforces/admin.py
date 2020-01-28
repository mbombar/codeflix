# Register your models here.

from django.contrib import admin
from DjangoTools import tools
from .models import CodeforcesUser

tools.autoregister(app_list=['codeforces'], ignored_models=[CodeforcesUser])

@admin.register(CodeforcesUser)
class CodeforcesUserAdmin(admin.ModelAdmin):
    search_fields = ['handle', 'first_name', 'last_name']
