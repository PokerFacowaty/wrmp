from django.db import models


class User(models.Model):
    name = models.TextField()
    device = models.OneToOneField("SOSDevice", null=True,
                                  on_delete=models.SET_NULL)


class SOSDevice(models.Model):
    device_id = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField()
