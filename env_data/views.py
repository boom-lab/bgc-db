from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .models import continuous_profile, discrete_profile, park, cycle_metadata, mission_reported
from django.http.response import JsonResponse
from rest_framework import status

@api_view(['DELETE','GET'])
@permission_classes([IsAuthenticated])
def con_profile_view(request):
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


@api_view(['DELETE','GET'])
@permission_classes([IsAuthenticated])
def dis_profile_view(request):
    if request.method == 'GET':
        return JsonResponse({'details':'Not Implemented Yet'}, status=status.HTTP_200_OK)

    if request.method == 'DELETE':
        profile_id = request.GET.get('PROFILE_ID', None)
        filters={"MISSION":profile_id}
        query = discrete_profile.objects.filter(**filters)
        res = query.delete()
        print(res[0])
        if res[0]==0: #If nothing was deleted
            return JsonResponse({'status': 'nothing deleted'}, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({'status': 'deleted '+str(res[0])+" entries"}, status=status.HTTP_200_OK)


@api_view(['DELETE','GET'])
@permission_classes([IsAuthenticated])
def park_view(request):
    if request.method == 'GET':
        return JsonResponse({'details':'Not Implemented Yet'}, status=status.HTTP_200_OK)

    if request.method == 'DELETE':
        profile_id = request.GET.get('PROFILE_ID', None)
        filters={"MISSION":profile_id}
        query = park.objects.filter(**filters)
        res = query.delete()
        print(res[0])
        if res[0]==0: #If nothing was deleted
            return JsonResponse({'status': 'nothing deleted'}, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({'status': 'deleted '+str(res[0])+" entries"}, status=status.HTTP_200_OK)


@api_view(['DELETE','GET'])
@permission_classes([IsAuthenticated])
def cycle_metadata_view(request):
    if request.method == 'GET':
        return JsonResponse({'details':'Not Implemented Yet'}, status=status.HTTP_200_OK)

    if request.method == 'DELETE':
        profile_id = request.GET.get('PROFILE_ID', None)
        filters={"PROFILE_ID":profile_id}
        query = cycle_metadata.objects.filter(**filters)
        res = query.delete()
        print(res[0])
        if res[0]==0: #If nothing was deleted
            return JsonResponse({'status': 'nothing deleted'}, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({'status': 'deleted '+str(res[0])+" entries"}, status=status.HTTP_200_OK)


@api_view(['DELETE','GET'])
@permission_classes([IsAuthenticated])
def mission_reported_view(request):
    if request.method == 'GET':
        return JsonResponse({'details':'Not Implemented Yet'}, status=status.HTTP_200_OK)

    if request.method == 'DELETE':
        profile_id = request.GET.get('PROFILE_ID', None)
        filters={"PROFILE_ID":profile_id}
        query = mission_reported.objects.filter(**filters)
        res = query.delete()
        print(res[0])
        if res[0]==0: #If nothing was deleted
            return JsonResponse({'status': 'nothing deleted'}, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({'status': 'deleted '+str(res[0])+" entries"}, status=status.HTTP_200_OK)