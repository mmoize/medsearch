from django.db.models.signals import post_save
from django.dispatch import receiver
import os

from django.db import models
from django.contrib.auth.models import User

DEFAULT = 'default.jpg'

#Save's Admins Display Image.
def get_image_path(instance, filename):
    return os.path.join('DP', str(instance.user), filename)


class  Owner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True)
    company = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to= get_image_path, default=DEFAULT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


    # The Owner will be defined by username field.
    def __str__(self):
        return self.user.username


# Signaling logic for triggering Owner object creation after signing up.
def create_user_owner(sender, instance, created, **kwargs):
    if created:
        owner = Owner(user=instance)
        owner.save()
post_save.connect(create_user_owner, sender=User, dispatch_uid="users-ownercreation-signal")