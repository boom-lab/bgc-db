from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from .serializers import MissionSerializer
from rest_framework import status
from rest_framework.decorators import api_view

#API for mission
@api_view(['GET', 'POST'])
def mission(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = MissionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #Todo: add get
    return None