from deployments.models import deployment
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import SensorSerializer
from .models import sensor
from rest_framework import status, generics, mixins
from django.http import JsonResponse

class Sensors(mixins.CreateModelMixin, generics.GenericAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class = SensorSerializer

    def post(self, request, *args, **kwargs):
        filters={}
        filters['FLOAT_SERIAL_NO'] = request.GET.get("FLOAT_SERIAL_NO", None)
        filters['PLATFORM_TYPE'] = request.GET.get("PLATFORM_TYPE", None)
        dep_id = deployment.objects.get(**filters).pk
        request.data["DEPLOYMENT"]=dep_id
        return self.create(request, *args, **kwargs)

    def get_object(self, filters):
        return sensor.objects.get(**filters)

    def patch(self, request):
        filters={}
        filters['DEPLOYMENT__FLOAT_SERIAL_NO'] = request.GET.get("FLOAT_SERIAL_NO", None)
        filters['DEPLOYMENT__PLATFORM_TYPE'] = request.GET.get("PLATFORM_TYPE", None)
        filters['SENSOR'] = request.GET.get("SENSOR", None)
        if not filters['DEPLOYMENT__PLATFORM_TYPE'] or not filters['DEPLOYMENT__FLOAT_SERIAL_NO'] or not filters['SENSOR']:
            return JsonResponse({'details':'Error: FLOAT_SERIAL_NO, PLATFORM_TYPE, or SENSOR not provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            sensor = self.get_object(filters)
            serializer = SensorSerializer(sensor, data=request.data, partial=True) # set partial=True to update a data partially
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(data=serializer.data)
            return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data="wrong parameters")
        except Exception as e:
            return JsonResponse({'details':str(e)}, status=status.HTTP_400_BAD_REQUEST)
