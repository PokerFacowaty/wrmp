from rest_framework import status, generics
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.response import Response
from tracker.models import SOSDevice, User
from tracker.serializers import (SOSDeviceSerializer,
                                 SOSDeviceLocationSerializer, UserSerializer)


class DeviceView(generics.GenericAPIView):
    queryset = SOSDevice.objects.all()
    serializer_class = SOSDeviceSerializer

    lookup_field = "device_id"
    lookup_url_kwarg = "id"

    def _partial_update(self, data, device=None,
                        status_code=status.HTTP_200_OK):
        if device is None:
            device = self.get_object()
        serializer = self.get_serializer(device, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status_code)


class UserView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    lookup_field = "id"
    lookup_url_kwarg = "id"


class AssignDevice(DeviceView):
    def post(self, request, id):
        device = self.get_object()
        # Unassigning user"s current device if they have one assigned
        try:
            user = User.objects.get(pk=request.data["user_id"])
            if user.device:
                self._partial_update(device=user.device,
                                     data={"user_id": None})
        except User.DoesNotExist and User.device.RelatedObjectDoesNotExist:
            pass
        return self._partial_update(data={"user_id": request.data["user_id"]},
                                    device=device)


class Devices(generics.ListAPIView, DeviceView):
    ...


class DeviceLocation(DeviceView):
    def post(self, request, id):
        device = self.get_object()
        if not device.user:
            raise ValidationError("Device not assigned")
        return self._partial_update(device=device, data=request.data)


class Map(generics.ListAPIView):
    serializer_class = SOSDeviceSerializer

    def get_queryset(self):
        queryset = SOSDevice.objects.filter(user__isnull=False)
        # Assuming "device_id" was meant by "device type" in the assignment
        device_type = self.request.query_params.get("device_type")
        if device_type is not None:
            queryset = queryset.filter(device_id=device_type)
        user_id = self.request.query_params.get("user_id")
        if user_id is not None:
            queryset = queryset.filter(user__id=user_id)
        return queryset


class UnassignDevice(DeviceView):
    def post(self, request, id):
        device = self.get_object()
        if not device.user:
            # Early return skips an unncessary DB write
            return Response(status=status.HTTP_204_NO_CONTENT)
        return self._partial_update(device=device, data={"user_id": None})


class UserLocation(UserView):
    def get(self, request, id):
        user = self.get_object()
        try:
            device = user.device
        except User.device.RelatedObjectDoesNotExist:
            raise NotFound("User has not device.")
        serializer = SOSDeviceLocationSerializer(device)
        return Response(serializer.data, status=status.HTTP_200_OK)
