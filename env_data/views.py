from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import continuous_profile, discrete_profile, park, cycle_metadata, mission_reported
from .serializers import ConProfileSerializer, DisProfileSerializer, ParkSerializer, CycleMetaSerializer, MissionReportedSerializer
from django_filters.rest_framework import DjangoFilterBackend

class GetConProfile(generics.ListAPIView): #Read only
    permission_classes=[IsAuthenticated]
    serializer_class = ConProfileSerializer
    queryset=continuous_profile.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_fields = [field.name for field in continuous_profile._meta.fields]

class GetDisProfile(generics.ListAPIView): #Read only
    permission_classes=[IsAuthenticated]
    serializer_class = DisProfileSerializer
    queryset=discrete_profile.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_fields = [field.name for field in discrete_profile._meta.fields]

class GetPark(generics.ListAPIView): #Read only
    permission_classes=[IsAuthenticated]
    serializer_class = ParkSerializer
    queryset=park.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_fields = [field.name for field in park._meta.fields]

class GetCycleMeta(generics.ListAPIView): #Read only
    permission_classes=[IsAuthenticated]
    serializer_class = CycleMetaSerializer
    queryset=cycle_metadata.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_fields = [field.name for field in cycle_metadata._meta.fields]

class GetMissionReported(generics.ListAPIView): #Read only
    permission_classes=[IsAuthenticated]
    serializer_class = MissionReportedSerializer
    queryset=mission_reported.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_fields = [field.name for field in mission_reported._meta.fields]