from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http.response import JsonResponse
from .models import file_processing
import json
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status

@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_success_files(request):

    sfiles = file_processing.objects.filter(STATUS__exact='Success').all()

    result = {'sucess_files': [s.DIRECTORY for s in sfiles]}

    return JsonResponse(result)

#@csrf_exempt
@permission_classes([IsAuthenticated])
@api_view(['PUT'])
def update_log(request):
    directory = request.GET['DIRECTORY']
    payload = json.loads(request.body)
    try:
        log_item = file_processing.objects.filter(DIRECTORY=directory)
        # returns 1 or 0
        log_item.update(**payload)

        return JsonResponse({'status': 'updated'}, safe=False, status=status.HTTP_200_OK)
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return JsonResponse({'error': 'Something terrible went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)