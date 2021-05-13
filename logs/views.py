from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http.response import JsonResponse
from .models import file_processing
import json
from rest_framework import status
from django.db.models import Q

@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_file_status(request):

    sfiles = file_processing.objects.filter(Q(STATUS='Success') | Q(STATUS='Skip')).all()
    rfiles = file_processing.objects.filter(Q(STATUS='Reprocess')).all()
    result = {'ignore_files': [s.DIRECTORY for s in sfiles], 'reprocess':[r.DIRECTORY for r in rfiles]}

    return JsonResponse(result)

#@csrf_exempt
@permission_classes([IsAuthenticated])
@api_view(['PUT'])
def put_process_log(request):
    directory = request.GET['DIRECTORY']
    payload = json.loads(request.body)
    try:
        log_item = file_processing.objects.filter(DIRECTORY=directory)
        if log_item:
            log_item.update(**payload)
            return JsonResponse({'status': 'updated'}, safe=False, status=status.HTTP_200_OK)
        else:
            file_processing.objects.create(DIRECTORY=directory, **payload)
            return JsonResponse({'status': 'added'}, safe=False, status=status.HTTP_200_OK)
    except Exception:
        return JsonResponse({'error': 'Something terrible went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)