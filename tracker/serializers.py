from tracker.models import User, SOSDevice
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name']


class SOSDeviceSerializer(serializers.ModelSerializer):
    # For reads
    user = UserSerializer(read_only=True)
    # For writes by pk
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),
                                                 read_only=False,
                                                 source='user',
                                                 allow_null=True,
                                                 required=False)
    # Some endpoints use that name as an alias
    ping_time = serializers.DateTimeField(source="timestamp", write_only=True)

    class Meta:
        model = SOSDevice
        fields = ['device_id', 'user', 'user_id', 'latitude', 'longitude',
                  'timestamp', 'ping_time']


class SOSDeviceLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SOSDevice
        fields = ['latitude', 'longitude', 'timestamp']
