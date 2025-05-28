from django.urls import path
import tracker.views as tviews
urlpatterns = [
    path('devices/<str:id>/assign', tviews.AssignDevice.as_view()),
    path('devices/<str:id>/location', tviews.DeviceLocation.as_view()),
    path('users/<int:id>/location', tviews.UserLocation.as_view()),
    path('map', tviews.Map.as_view()),
    path('devices', tviews.Devices.as_view()),
    path('devices/<str:id>/unassign', tviews.UnassignDevice.as_view())
    ]
