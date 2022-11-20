from django.db import models
from django.contrib.auth import get_user_model
from authorization.models import CustomUser

# Create your models here.

class Tasks(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
    title = models.CharField(max_length = 30, default = 'My task')
    description = models.CharField(max_length = 300, blank = True)
    date_created = models.DateTimeField(auto_now_add = True)
    date_modefied = models.DateTimeField(auto_now = True)
    appointment_date = models.DateTimeField()

    class Meta:
        verbose_name = 'task'
        verbose_name_plural = 'tasks'
        order_with_respect_to = 'user_id'
        get_latest_by = ['date_created']

class FriendsRequests(models.Model):
    from_user = models.ForeignKey(get_user_model(), related_name = 'from_user',on_delete = models.CASCADE)
    to_user = models.ForeignKey(get_user_model(), related_name = 'to_user', on_delete = models.CASCADE)
    relationship = models.SmallIntegerField(null = False, blank = False)
