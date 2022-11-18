from django.db import models
from authorization.models import CustomUser

# Create your models here.

class Tasks(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length = 30, default = 'My task')
    description = models.CharField(max_length = 300)
    date_created = models.DateTimeField(auto_now_add = True)
    date_modefied = models.DateTimeField(auto_now = True)
    appointment_date = models.DateTimeField()

    class Meta:
        verbose_name = 'task'
        verbose_name_plural = 'tasks'
        order_with_respect_to = 'user_id'
        get_latest_by = ['date_created']
