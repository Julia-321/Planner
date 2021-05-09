from django.db import models
from django.contrib.auth.models import User
from accounts import consts


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    notification_option = models.IntegerField(choices=consts.NOTIFICATION_OPTIONS, default=1)  # default push
    home_view = models.IntegerField(choices=consts.HOME_PAGE, default=1)  # default list of all tasks
    theme = models.IntegerField(choices=consts.APPEARANCE, default=1)  # default Light
    date_view = models.IntegerField(choices=consts.DATA_VIEW, default=1)  # default dd-mm-yyyy
    push_time = models.IntegerField(choices=consts.PUSH_TIME, default=1)  # default = deadline

    def __str__(self):
        return f'Profile {self.user}'
