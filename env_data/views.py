from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .models import continuous_profile, discrete_profile, park, cycle_metadata, mission_reported
from .serializers import ConProfileSerializer, DisProfileSerializer, ParkSerializer, CycleMetaSerializer, MissionReportedSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django.http.response import JsonResponse
from rest_framework import status

@api_view(['DELETE','GET'])
@permission_classes([IsAuthenticated])
def con_profile(request):
    if request.method == 'GET':
        return JsonResponse({'details':'Not Implemented Yet'}, status=status.HTTP_200_OK)

    if request.method == 'DELETE':
        profile_id = request.GET.get('PROFILE_ID', None)
        filters={"MISSION":profile_id}
        query = continuous_profile.objects.filter(**filters)
        res = query.delete()
        print(res[0])
        if res[0]==0: #If nothing was deleted
            return JsonResponse({'status': 'nothing deleted'}, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({'status': 'deleted '+str(res[0])+" entries"}, status=status.HTTP_200_OK)


class ConProfile(generics.ListCreateAPIView): #Read, write
    permission_classes=[IsAuthenticated]
    serializer_class = ConProfileSerializer
    queryset=continuous_profile.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_fields = [field.name for field in continuous_profile._meta.fields]


class ConProfileDelete(generics.DestroyAPIView): # delete
    permission_classes=[IsAuthenticated]
    serializer_class = ConProfileSerializer
    queryset=continuous_profile.objects.all()

    def destroy(self, request, *args, **kwargs):
        filters={"MISSION":kwargs['PROFILE_ID']}
        query = continuous_profile.objects.filter(**filters)
        res = query.delete()
        print(res[0])
        if res[0]==0:
            return JsonResponse({'status': 'nothing deleted'}, status=status.HTTP_200_OK)
        return JsonResponse({'status': 'deleted '+str(res[0])+" entries"}, status=status.HTTP_200_OK)


class DisProfile(generics.ListCreateAPIView): #Read, write
    permission_classes=[IsAuthenticated]
    serializer_class = DisProfileSerializer
    queryset=discrete_profile.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_fields = [field.name for field in discrete_profile._meta.fields]
    
class DisProfileDelete(generics.DestroyAPIView): # delete
    permission_classes=[IsAuthenticated]
    serializer_class = DisProfileSerializer
    queryset=discrete_profile.objects.all()

    def destroy(self, request, *args, **kwargs):
        filters={"MISSION":kwargs['PROFILE_ID']}
        query = discrete_profile.objects.filter(**filters)
        res = query.delete()
        print(res[0])
        if res[0]==0:
            return JsonResponse({'status': 'nothing deleted'}, status=status.HTTP_200_OK)
        return JsonResponse({'status': 'deleted '+str(res[0])+" entries"}, status=status.HTTP_200_OK)

class Park(generics.ListCreateAPIView): #Read, write
    permission_classes=[IsAuthenticated]
    serializer_class = ParkSerializer
    queryset=park.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_fields = [field.name for field in park._meta.fields]

class ParkDelete(generics.DestroyAPIView): # delete
    permission_classes=[IsAuthenticated]
    serializer_class = ParkSerializer
    queryset=park.objects.all()

    def destroy(self, request, *args, **kwargs):
        filters={"MISSION":kwargs['PROFILE_ID']}
        query = park.objects.filter(**filters)
        res = query.delete()
        print(res[0])
        if res[0]==0:
            return JsonResponse({'status': 'nothing deleted'}, status=status.HTTP_200_OK)
        return JsonResponse({'status': 'deleted '+str(res[0])+" entries"}, status=status.HTTP_200_OK)

class CycleMeta(generics.ListCreateAPIView): #Read, write
    permission_classes=[IsAuthenticated]
    serializer_class = CycleMetaSerializer
    queryset=cycle_metadata.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_fields = [field.name for field in cycle_metadata._meta.fields]

class CycleMetaDelete(generics.DestroyAPIView): # delete
    permission_classes=[IsAuthenticated]
    serializer_class = CycleMetaSerializer
    queryset=cycle_metadata.objects.all()

    def destroy(self, request, *args, **kwargs):
        filters={"PROFILE_ID":kwargs['PROFILE_ID']}
        query = cycle_metadata.objects.filter(**filters)
        res = query.delete()
        print(res[0])
        if res[0]==0:
            return JsonResponse({'status': 'nothing deleted'}, status=status.HTTP_200_OK)
        return JsonResponse({'status': 'deleted '+str(res[0])+" entries"}, status=status.HTTP_200_OK)

class MissionReported(generics.ListCreateAPIView): #Read, write
    permission_classes=[IsAuthenticated]
    serializer_class = MissionReportedSerializer
    queryset=mission_reported.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_fields = [field.name for field in mission_reported._meta.fields]

class MissionReportedDelete(generics.DestroyAPIView): # delete
    permission_classes=[IsAuthenticated]
    serializer_class = MissionReportedSerializer
    queryset=mission_reported.objects.all()

    def destroy(self, request, *args, **kwargs):
        filters={"PROFILE_ID":kwargs['PROFILE_ID']}
        query = mission_reported.objects.filter(**filters)
        res = query.delete()
        print(res[0])
        if res[0]==0:
            return JsonResponse({'status': 'nothing deleted'}, status=status.HTTP_200_OK)
        return JsonResponse({'status': 'deleted '+str(res[0])+" entries"}, status=status.HTTP_200_OK)