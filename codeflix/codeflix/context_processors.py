from django.contrib.sites.shortcuts import get_current_site


from . import settings


def site_name(request):
    """
    Define the site name in the context.
    """
    site = get_current_site(request)
    return {
        "sitename": settings.SITE_NAME or site.name,
    }
