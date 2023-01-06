from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Tasks(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete = models.CASCADE)
    title = models.CharField(max_length = 30, default = 'My task')
    description = models.CharField(max_length = 300, null = True, blank = True)
    date_created = models.DateTimeField(auto_now_add = True)
    date_modified = models.DateTimeField(auto_now = True)
    appointment_date = models.DateTimeField()
    is_private = models.BooleanField(default = False)

    class Meta:
        verbose_name = 'task'
        verbose_name_plural = 'tasks'
        order_with_respect_to = 'user_id'
        get_latest_by = ['date_created']


class AllowedFriendsToPrivateTask(models.Model):
    task = models.ForeignKey(Tasks, related_name = 'admitted_friends', on_delete = models.CASCADE)
    friend = models.ForeignKey(get_user_model(), related_name = 'admitted_tasks', on_delete = models.CASCADE)


class FriendsRequests(models.Model):
    from_user = models.ForeignKey(get_user_model(), related_name = 'from_user', on_delete = models.CASCADE)
    to_user = models.ForeignKey(get_user_model(), related_name = 'to_user', on_delete = models.CASCADE)
    relationship = models.SmallIntegerField(null = False, blank = False)
