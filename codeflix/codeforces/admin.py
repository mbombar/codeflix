# Register your models here.

from django.contrib import admin
from DjangoTools import tools
from .models import CodeforcesUser, Problem

tools.autoregister(app_list=['codeforces'], ignored_models=[CodeforcesUser, Problem])

@admin.register(CodeforcesUser)
class CodeforcesUserAdmin(admin.ModelAdmin):
    search_fields = ['handle', 'first_name', 'last_name']

@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    search_fields = ['name']
