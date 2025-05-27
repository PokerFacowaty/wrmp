from tracker.models import User, SOSDevice
from rest_framework.views import APIView
from tracker.serializers import SOSDeviceSerializer
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from rest_framework import generics


class AssignDevice(APIView):
    def get_device(self, id):
        try:
            return SOSDevice.objects.get(device_id=id)
        except SOSDevice.DoesNotExist:
            raise Http404

    def get_user(self, id):
        try:
            return User.objects.get(pk=id)
        except User.DoesNotExist:
            raise Http404

    def post(self, request, id, format=None):
        device = self.get_device(id)
        user_id = self.request.data["user_id"]
        serializer = SOSDeviceSerializer(device, data={'user_id': user_id},
                                         partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data="Wrong data", status=status.HTTP_400_BAD_REQUEST)


class DeviceLocation(APIView):
    # TODO: fix
    def get_device(self, id):
        try:
            return SOSDevice.objects.get(device_id=id)
        except SOSDevice.DoesNotExist:
            raise Http404

    def post(self, request, id, format=None):
        device = self.get_device(id)
        if not device.user:
            return Response(data="Device not assigned",
                            status=status.HTTP_400_BAD_REQUEST)
        latitude = request.data["latitude"]
        longitude = request.data["longitude"]
        try:
            tz = datetime.fromisoformat(request.data["ping_time"])
        except ValueError:
            return Response(data="Timestamp not in ISO format",
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = SOSDeviceSerializer(device,
                                         data={"latitude": latitude,
                                               "longitude": longitude,
                                               "timestamp": tz},
                                         partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data="Wrong data", status=status.HTTP_400_BAD_REQUEST)


class UserLocation(APIView):
    def get_user(self, id):
        try:
            return User.objects.get(pk=id)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        user = self.get_user(id)
        serializer = SOSDeviceSerializer(user.device)
        return Response({"latitude": serializer.data["latitude"],
                         "longitude": serializer.data["longitude"],
                         "timestamp": serializer.data["timestamp"]},
                        status=status.HTTP_200_OK)


class Map(generics.ListAPIView):
    queryset = SOSDevice.objects.filter(user__isnull=False)
    serializer_class = SOSDeviceSerializer


class Devices(generics.ListAPIView):
    queryset = SOSDevice.objects.all()
    serializer_class = SOSDeviceSerializer


class UnassignDevice(APIView):
    # TODO: fix
    def get_device(self, id):
        try:
            return SOSDevice.objects.get(device_id=id)
        except SOSDevice.DoesNotExist:
            raise Http404

    def post(self, request, id, format=None):
        device = self.get_device(id)
        if not device.user:
            return Response(data="Device already unassigned",
                            status=status.HTTP_200_OK)
        serializer = SOSDeviceSerializer(device, data={"user_id": None},
                                         partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data="Wrong data", status=status.HTTP_400_BAD_REQUEST)
