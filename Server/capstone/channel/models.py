from django.db import models

# Create your models here.


class ChannelList(models.Model):
    channelLink = models.CharField(max_length=500)

    class Meta:
        db_table = "channel_link"


class HistoryList(models.Model):
    gi = 5
