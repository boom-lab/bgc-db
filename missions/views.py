from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import MissionSerializer, AddMissionSerializer
from .models import mission

class GetMissions(generics.ListAPIView): #Read and write only
    permission_classes=[permissions.IsAuthenticated]
    serializer_class = MissionSerializer
    queryset=mission.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_fields = [field.name for field in mission._meta.fields]

class AddMissions(generics.ListCreateAPIView): #Read and write only
    permission_classes=[permissions.IsAuthenticated]
    serializer_class = AddMissionSerializer
    queryset=mission.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_fields = [field.name for field in mission._meta.fields]