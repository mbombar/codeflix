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

def cfuser(request):
    """
    Define cfuser in the context
    """
    try:
        cfuser = request.user.profile.cfuser
    except AttributeError:
        cfuser = None
    return {
        "cfuser": cfuser,
    }
