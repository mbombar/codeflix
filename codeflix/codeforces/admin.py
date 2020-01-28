# Register your models here.

from DjangoTools import tools
from .models import CodeforcesUser

tools.autoregister(app_list=['codeforces'], ignored_models=[CodeforcesUser])
