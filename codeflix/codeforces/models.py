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
    rating = models.IntegerField(
        verbose_name=_("Rating"),
        default=0
    )
    max_rank = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("User's max rank."),
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
        blank=True,
    )
    title_photo = models.CharField(
        max_length=255,
        verbose_name=_("User's title photo URL."),
        blank=True,
    )
    database_user = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )


class Contest(models.Model):
    """
    A Codeforces Contest object.
    """
    id = models.IntegerField(
        verbose_name=_("Id of the contest."),
        primary_key=True
    )
    name = models.CharField(
        max_length=255,
        verbose_name=_("Name of the contest.")
    )
    type = models.CharField(
        max_length=255,
        choices=[("CF", "CF"),
                 ("IOI", "IOI"),
                 ("ICPC", "ICPC")],
        verbose_name=_("Scoring system used for the contest.")
    )
    phase = models.CharField(
        max_length=255,
        choices=[("BEFORE", "BEFORE"),
                 ("CODING", "CODING"),
                 ("PENDING_SYSTEM_TEST", "PENDING_SYSTEM_TEST"),
                 ("SYSTEM_TEST", "SYSTEM_TEST"),
                 ("FINISHED", "FINISHED")],
        verbose_name=_("Current phase of the contest.")
    )
    frozen = models.BooleanField()
    duration_seconds = models.IntegerField(
        verbose_name=_("Duration of the contest in seconds.")
    )
    start_time_seconds = models.BigIntegerField(
        null=True,
        verbose_name=_("Contest start time in unix format.")
    )
    relative_time_seconds = models.BigIntegerField(
        null=True,
        verbose_name=_("Number of seconds, passed after the start of the contest.")
    )
    difficulty = models.IntegerField(
        null=True,
        verbose_name=_("Larger number means more difficult problems")
    )
    useful = models.BooleanField(
        default=False,
        verbose_name=_("Is this contest useful for codeflix ?")
    )
