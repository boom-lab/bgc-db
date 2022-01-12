from env_data.serializers import CycleMetaSerializer, DisProfileSerializer, ParkSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .models import continuous_profile, discrete_profile, park, cycle_metadata, mission_reported
from django.http.response import JsonResponse
from rest_framework import status, generics
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Max, Count

#----------------------GET Data APIs------------------------------#

class GetDisData(generics.ListAPIView): #Read only, currently only filters by pressure, date add, and platform number. output fields can be controlled.
    serializer_class = DisProfileSerializer
    queryset=discrete_profile.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_fields ={"PRES":['gt','lt','range','exact'],
        "DATE_ADD":['gt','lt','range','exact'],
        "DEPLOYMENT__PLATFORM_NUMBER":['exact']
    }

class GetParkData(generics.ListAPIView): #Read only, currently only filters by pressure, date add, date measured, and platform number. output fields can be controlled.
    serializer_class = ParkSerializer
    queryset=park.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_fields ={"DATE_ADD":['gt','lt','range','exact'],
        "DATE_MEASURED":['gt','lt','range','exact'],
        "DEPLOYMENT__PLATFORM_NUMBER":['exact'],
        "PROFILE_ID":['exact']
    }

class GetCycleMeta(generics.ListAPIView): #Read only
    serializer_class = CycleMetaSerializer
    queryset=cycle_metadata.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_fields ={"DEPLOYMENT__PLATFORM_NUMBER":['exact'],
        "PROFILE_ID":['exact'],
        "DATE_ADD":['gt','lt','range','exact'],
    }


#------------------DELETE APIs -------------------------#
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def con_profile_delete(request):
    if request.method == 'DELETE':
        profile_id = request.GET.get('PROFILE_ID', None)
        filters={"PROFILE_ID":profile_id}
        query = continuous_profile.objects.filter(**filters)
        res = query.delete()

        if res[0]==0: #If nothing was deleted
            return JsonResponse({'status': 'nothing deleted'}, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({'status': 'deleted '+str(res[0])+" entries"}, status=status.HTTP_200_OK)
        
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def park_delete(request):
    if request.method == 'DELETE':
        profile_id = request.GET.get('PROFILE_ID', None)
        filters={"PROFILE_ID":profile_id}
        query = park.objects.filter(**filters)
        res = query.delete()

        if res[0]==0: #If nothing was deleted
            return JsonResponse({'status': 'nothing deleted'}, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({'status': 'deleted '+str(res[0])+" entries"}, status=status.HTTP_200_OK)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def cycle_metadata_delete(request):
    if request.method == 'DELETE':
        profile_id = request.GET.get('PROFILE_ID', None)
        filters={"PROFILE_ID":profile_id}
        query = cycle_metadata.objects.filter(**filters)
        res = query.delete()
        if res[0]==0: #If nothing was deleted
            return JsonResponse({'status': 'nothing deleted'}, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({'status': 'deleted '+str(res[0])+" entries"}, status=status.HTTP_200_OK)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def mission_reported_delete(request):
    if request.method == 'DELETE':
        profile_id = request.GET.get('PROFILE_ID', None)
        filters={"PROFILE_ID":profile_id}
        query = mission_reported.objects.filter(**filters)
        res = query.delete()

        if res[0]==0: #If nothing was deleted
            return JsonResponse({'status': 'nothing deleted'}, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({'status': 'deleted '+str(res[0])+" entries"}, status=status.HTTP_200_OK)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def dis_profile_delete(request):
    if request.method == 'DELETE':
        profile_id = request.GET.get('PROFILE_ID', None)
        filters={"PROFILE_ID":profile_id}
        query = discrete_profile.objects.filter(**filters)
        res = query.delete()

        if res[0]==0: #If nothing was deleted
            return JsonResponse({'status': 'nothing deleted'}, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({'status': 'deleted '+str(res[0])+" entries"}, status=status.HTTP_200_OK)

#---------------------Update Cycle Metadata ------------------------------#
class CycleMetaUpdate(generics.UpdateAPIView, generics.CreateAPIView): #Post new metadata, Update (patch), token
    permission_classes=[IsAuthenticated]
    serializer_class=CycleMetaSerializer
    queryset=cycle_metadata.objects.all()

    def get_object(self):
        filters={}
        filters['PROFILE_ID'] = self.request.GET.get("PROFILE_ID", None)

        if not filters['PROFILE_ID']:
            return JsonResponse({'details':'Error: PROFILE_ID not provided'}, status=status.HTTP_400_BAD_REQUEST)

        return get_object_or_404(cycle_metadata, **filters)

#---------------------------Stats APIs ---------------------------#
@api_view(['GET'])
def continuous_profile_stats(request):
    filters = {}
    
    #Get parameters
    PLATFORM_NUMBER = request.GET.get('PLATFORM_NUMBER', None)
    if PLATFORM_NUMBER:
        filters['DEPLOYMENT__PLATFORM_NUMBER'] = PLATFORM_NUMBER
    else:
        return JsonResponse({'details':'Error: PLATFORM_NUMBER (WMO) must be specified'}, 
        status=status.HTTP_400_BAD_REQUEST) 

    query = continuous_profile.objects.filter(**filters).values('PROFILE_ID').annotate(max=Max('PRES'), n=Count('PRES'))

    results = {
        "PROFILE_ID":list(query.values_list('PROFILE_ID', flat=True)),
        "PRES_MAX":list(query.values_list('max', flat=True)),
        "N_SAMPLES":list(query.values_list('n', flat=True)),
    }

    return JsonResponse(results, status=status.HTTP_200_OK)

@api_view(['GET'])
def dis_profile_stats(request):
    filters = {}
    
    #Get parameters
    PLATFORM_NUMBER = request.GET.get('PLATFORM_NUMBER', None)
    if PLATFORM_NUMBER:
        filters['DEPLOYMENT__PLATFORM_NUMBER'] = PLATFORM_NUMBER
    else:
        return JsonResponse({'details':'Error: PLATFORM_NUMBER (WMO) must be specified'}, 
        status=status.HTTP_400_BAD_REQUEST) 


    query = discrete_profile.objects.filter(**filters).values('PROFILE_ID').annotate(max=Max('PRES'), n=Count('PRES'))

    results = {
        "PROFILE_ID":list(query.values_list('PROFILE_ID', flat=True)),
        "PRES_MAX":list(query.values_list('max', flat=True)),
        "N_SAMPLES":list(query.values_list('n', flat=True)),
    }

    return JsonResponse(results, status=status.HTTP_200_OK)