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

@permission_classes([IsAuthenticated])
@api_view(['PUT'])
def update_suna_cal(request):
    sn = request.GET['SENSOR_SERIAL_NO']
    payload = json.loads(request.body)
    
    try:
        obj = get_object_or_404(sensor, SENSOR_SERIAL_NO=sn)
        obj.PREDEPLOYMENT_CALIB_COEFFICIENT=payload
        obj.save()
        return JsonResponse({'status': 'updated'}, safe=False, status=status.HTTP_200_OK)
    except Exception:
        return JsonResponse({'status': 'failed'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)