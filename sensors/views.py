from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import SensorSerializer
from .models import sensor
from django.shortcuts import get_object_or_404
from rest_framework import status
import json
from django.http import JsonResponse

class GetSensors(generics.ListAPIView):
    permission_classes=[permissions.IsAuthenticated]
    serializer_class = SensorSerializer
    queryset=sensor.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['ADD_DATE','SENSOR','SENSOR_MAKER','SENSOR_MODEL','SENSOR_SERIAL_NO','SENSOR_CALIB_DATE']

class UpdateSensors(generics.UpdateAPIView):
    permission_classes=[permissions.IsAuthenticated]
    serializer_class = SensorSerializer
    lookup_field='SENSOR_SERIAL_NO'
    queryset=sensor.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['ADD_DATE','SENSOR','SENSOR_MAKER','SENSOR_MODEL','SENSOR_SERIAL_NO','SENSOR_CALIB_DATE']
