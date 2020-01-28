from django.apps import apps
from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered, NotRegistered


def autoregister(*args, **kwargs):
    """
    Automatically register all the models from a given list
    of apps to the admin site
    """
    app_list = kwargs.get('app_list', [])
    ignored_models = kwargs.get('ignored_models', [])
    for app in app_list:
        for model in apps.get_app_config(app).get_models():
            if model in ignored_models:
                try:
                    admin.site.unregister(model)
                except NotRegistered:
                    pass
            else:
                try:
                    admin.site.register(model)
                except AlreadyRegistered:
                    pass
