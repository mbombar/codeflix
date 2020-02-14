from codeforces.models import CodeforcesUser
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class Profile(models.Model):
    """
    The Profile of a user. Adds new fields.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars', default='avatars/unknown.png')
    email_confirmed = models.BooleanField(default=False)
    cfuser = models.ForeignKey(
        CodeforcesUser,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
