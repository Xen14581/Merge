from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.




    # username, repo_name, task, date, completed
class Todo(models.Model):
    title = models.CharField(max_length=120)
    completed = models.BooleanField(default=False)
    repo = models.CharField(max_length=120, default='')
    assigned_merge_user = models.CharField(max_length=120, default='')
    deadline = models.CharField(max_length=10, default='')

    def _str_(self):
        return self.title


class MergeProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    merge_username = models.CharField(max_length=500, blank=True, unique=True)
    merge_password = models.CharField(max_length=500, blank=True)

    USERNAME_FIELD = 'merge_username'
    PASSWORD_FIELD = 'merge_password'


# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         MergeProfile.objects.create(user=instance)
#
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()

@receiver(post_save, sender=User)
def update_password(sender, instance, **kwargs):
    if instance.password != instance.profile.merge_password:
        instance.password = instance.profile.merge_password
        instance.save()
