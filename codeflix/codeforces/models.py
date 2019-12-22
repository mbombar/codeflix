from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class CodeforcesUser(models.Model):
    """
    A Codeforces User object. May be linked to a database user.
    """

    handle = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_("Handle"),
    )
    email = models.EmailField(
        verbose_name=_("Email address"),
        blank=True,
    )
    vkid = models.CharField(
        max_length=255,
        blank=True,
    )
    openid = models.CharField(
        max_length=255,
        blank=True,
    )
    first_name = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("First name"),
    )
    last_name = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Last name"),
    )
    country = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Country"),
    )
    city = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("City"),
    )
    organization = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Organization"),
    )
    contribution = models.IntegerField(
        verbose_name=_("User contribution"),
    )
    rank = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Rank"),
    )
    max_rating = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Max Rating"),
    )
    last_online_time_seconds = models.BigIntegerField(
        verbose_name=_("Time, when user was last seen online, in UNIX format."),
    )
    registration_time_seconds = models.BigIntegerField(
        verbose_name=_("Time, when user was registered, in UNIX format."),
    )
    friend_of_count = models.IntegerField(
        verbose_name=_("Amount of users who have this user in friends."),
    )
    avatar = models.CharField(
        max_length=255,
        verbose_name=_("User's avatar URL."),
    )
    title_photo = models.CharField(
        max_length=255,
        verbose_name=_("User's title photo URL."),
    )
    database_user = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
