from django.db import models


class User(models.Model):
    name = models.CharField(max_length=255)


class SOSDevice(models.Model):
    device_id = models.CharField(unique=True, max_length=255)
    user = models.OneToOneField(User, null=True,
                                on_delete=models.SET_NULL,
                                related_name="device")
    # Nulls for initially added devices that haven't sent anything yet.
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    timestamp = models.DateTimeField(null=True)
