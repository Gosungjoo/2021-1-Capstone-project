from django.db import models

# Create your models here.


class ChannelList(models.Model):
    channel_info = models.CharField(max_length=500)
    img = models.CharField(max_length=500)
    title = models.CharField(max_length=500)
    subscribers = models.CharField(max_length=500)

    class Meta:
        db_table = "channel_link"
