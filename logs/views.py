from cmath import log
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http.response import JsonResponse
from django.core.mail import send_mail
from .models import file_processing
import json
from rest_framework import status
from django.db.models import Q
from datetime import datetime, timedelta

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_file_status(request):

    sfiles = file_processing.objects.filter(Q(STATUS='Success') | Q(STATUS='Skip') | Q(STATUS='Warning')).all()
    rfiles = file_processing.objects.filter(Q(STATUS='Reprocess')).all()
    ffiles = file_processing.objects.filter(Q(STATUS='Fail')).all()
    result = {'ignore_files': [s.DIRECTORY for s in sfiles], 'reprocess':[r.DIRECTORY for r in rfiles], 'fail':[r.DIRECTORY for r in ffiles]}

    return JsonResponse(result)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def put_process_log(request):
    #Updates or adds process log entries

    directory = request.GET['DIRECTORY']
    payload = json.loads(request.body)

    try:
        
        log_item = file_processing.objects.filter(DIRECTORY=directory)

        date_processed = datetime.strptime(payload["DATE_PROCESSED"],'%Y-%m-%dT%H:%M:%SZ')
        date_modified = datetime.strptime(payload["DATE_FILE_MODIFIED"],'%Y-%m-%dT%H:%M:%SZ')
        print(((date_modified + timedelta(days=1)) < date_processed))
        send_email(payload, log_item) #only send email if new record
        if log_item: #Log entry already exists
            log_item.update(**payload)
            return JsonResponse({'status': 'updated'}, safe=False, status=status.HTTP_200_OK)
        else: #Create new entry
            file_processing.objects.create(DIRECTORY=directory, **payload)
            return JsonResponse({'status': 'added'}, safe=False, status=status.HTTP_200_OK)
    except Exception:
        return JsonResponse({'error': 'Something terrible went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

def send_email(payload, log_item):
    #Sends warning/error or recieved first cycle/prelude email messages
    try:
        if log_item:
            date_processed = datetime.strptime(payload["DATE_PROCESSED"],'%Y-%m-%dT%H:%M:%SZ')
            date_modified = datetime.strptime(payload["DATE_FILE_MODIFIED"],'%Y-%m-%dT%H:%M:%SZ')

            if payload['CYCLE'] == '000' and payload['STATUS'] == 'Success': #Special for prelude
                send_mail(
                    payload['FLOAT_SERIAL_NO'] + ": "+"Prelude Proccessed",
                    payload['STATUS'],
                    'from@example.com',
                    ['randerson@whoi.edu','dnicholson@whoi.edu'],
                    fail_silently=False,
                )
            elif payload['CYCLE'] == '001' and payload['STATUS'] == 'Success': #Special for first profile
                send_mail(
                    payload['FLOAT_SERIAL_NO'] + ": "+"First cycle proccessed",
                    payload['STATUS'],
                    'from@example.com',
                    ['randerson@whoi.edu','dnicholson@whoi.edu'],
                    fail_silently=False,
                )
            elif payload['STATUS'] != 'Success' and ((date_modified + timedelta(days=1)) < date_processed): #New message, but error proccessing. Ignore <EOT> errors, don't send email if already sent one.
                send_mail(
                    'BGC Processing '+payload['STATUS'] + ' - SN: ' + payload['FLOAT_SERIAL_NO'] + ' Cycle: ' + payload['CYCLE'],
                    payload.get('DETAILS'),
                    'from@example.com',
                    ['randerson@whoi.edu',],
                    fail_silently=False,
                )

        else: #No process log record
            #Mission Prelude (incomplete or complete)
            if payload['CYCLE'] == '000':
                send_mail(
                    payload['FLOAT_SERIAL_NO'] + ": "+"Mission prelude recieved",
                    payload.get('DETAILS'),
                    'from@example.com',
                    ['randerson@whoi.edu','dnicholson@whoi.edu'],
                    fail_silently=False,
                )


    except Exception:
        pass

