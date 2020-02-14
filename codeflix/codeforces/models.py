from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Attempt(models.Model):
    """
    A model representing an attempt to solve a problem
    """
    contest = models.ForeignKey(
        "Contest",
        verbose_name=_("Contest for which this attempt was made."),
        on_delete=models.CASCADE,
        null=True,
    )
    problem = models.ForeignKey(
        "Problem",
        verbose_name=_("The problem for which this is an attempt."),
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        "CodeforcesUser",
        verbose_name=_("Author of this attempt"),
        on_delete=models.CASCADE,
    )
    solved = models.BooleanField(
        default=False,
        verbose_name=_("Was this submission a success ?")
    )

    def __str__(self):
        return "Attempt of {} for {} {}--> {}".format(self.author.handle, self.problem.name, "in contest {} ".format(self.contest.id) * bool(self.contest), "Success" * self.solved + "Failure" * (1 - self.solved))


class CodeforcesUser(models.Model):
    """
    A Codeforces User object.
    """

    handle = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_("Handle"),
    )
    first_name = models.CharField(
        max_length=255,
        null=True,
        verbose_name=_("First name"),
    )
    last_name = models.CharField(
        max_length=255,
        null=True,
        verbose_name=_("Last name"),
    )

    def __str__(self):
        return "{} '{}' {}".format(self.first_name or "", self.handle, self.last_name or "")


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
    problems = models.ManyToManyField(
        'Problem',
        verbose_name=_("The list of problems of this contest.")
    )

    def __str__(self):
        return "{} - {}".format(self.id, self.name)


class Problem(models.Model):
    """
    A Codeforces Problem object.
    """
    contest_id = models.IntegerField(
        null=True,
        verbose_name=_("Id of the contest containing the problem.")
    )
    problemset_name = models.CharField(
        max_length=255,
        null=True,
        verbose_name=_("Short name of the problemset the problem belongs to.")
    )
    index = models.CharField(
        max_length=255,
        verbose_name=_("Problem index in the contest.")
    )
    name = models.CharField(
        max_length=255,
        verbose_name=_("Name of the problem.")
    )
    type = models.CharField(
        max_length=255,
        choices=[("PROGRAMMING", "PROGRAMMING"),
                 ("QUESTION", "QUESTION")],
        verbose_name=_("Type of the problem.")
    )
    points = models.FloatField(
        null=True,
        verbose_name=_("Maximum ammount of points for the problem.")
    )
    rating = models.IntegerField(
        null=True,
        verbose_name=_("Problem rating (difficulty).")
    )
    tags = models.ManyToManyField(
        'ProblemTag',
        verbose_name=_("List of tags for the problem.")
    )

    def __str__(self):
        return self.name


class ProblemTag(models.Model):
    """A Tag for a problem"""
    name = models.CharField(
        max_length=255,
        verbose_name=_("The name of the tag.")
    )

    def __str__(self):
        return self.name
