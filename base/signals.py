from django.db.models.signals import post_save
from django.dispatch import receiver

from django.utils.translation import gettext as _

from django.contrib.auth.models import User
from portal.models import Profile

@receiver(post_save, sender=User)
def createProfile(sender, instance, created, **kwargs):
    if created:
        profile = Profile(
            email = instance.email,
            user = instance,
        )
        try : profile.save()
        except Exception as xc : print('xxxxxxxxxxxxxxxxxxx Exception raised when creating Profile instance:', str(xc))
    