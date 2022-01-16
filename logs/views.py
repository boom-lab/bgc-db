from cmath import log
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http.response import JsonResponse
from django.core.mail import send_mail
from .models import file_processing
import json
from rest_framework import status
from django.db.models import Q

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_file_status(request):

    sfiles = file_processing.objects.filter(Q(STATUS='Success') | Q(STATUS='Skip') | Q(STATUS='Warning')).all()
    rfiles = file_processing.objects.filter(Q(STATUS='Reprocess')).all()
    ffiles = file_processing.objects.filter(Q(STATUS='Fail')).all()
    result = {'ignore_files': [s.DIRECTORY for s in sfiles], 'reprocess':[r.DIRECTORY for r in rfiles], 'fail':[r.DIRECTORY for r in ffiles]}

    return JsonResponse(result)

def send_email(payload, log_item):
    #Sends warning/error or recieved first cycle/prelude email messages

    try:
        if log_item:
            #print(log_item)
            #if log_item['STATUS'] != 'Success' and payload['STATUS'] == 'Success': #Success email after failed attempts
             #   send_mail(
              #      'BGC Processing '+payload['STATUS'] + ' - SN: ' + payload['FLOAT_SERIAL_NO'] + ' Cycle: ' + payload['CYCLE'],
               #     payload.get('DETAILS'),
                #    'from@example.com',
                 #   ['randerson@whoi.edu', 'dnicholson@whoi.edu'],
                  #  fail_silently=False,
                #)
            if payload['STATUS'] != 'Success': #Any failed files after initial files
                send_mail(
                    'BGC Processing '+payload['STATUS'] + ' - SN: ' + payload['FLOAT_SERIAL_NO'] + ' Cycle: ' + payload['CYCLE'],
                    payload.get('DETAILS'),
                    'from@example.com',
                    ['randerson@whoi.edu'],
                    fail_silently=False,
                )

        else: #First files
            #Error processing or warning
            if payload['STATUS'] != 'Success' and payload['CYCLE'] != '000':
                send_mail(
                    'BGC Processing '+payload['STATUS'] + ' - SN: ' + payload['FLOAT_SERIAL_NO'] + ' Cycle: ' + payload['CYCLE'],
                    payload.get('DETAILS'),
                    'from@example.com',
                    ['randerson@whoi.edu'],
                    fail_silently=False,
                )

            #Mision Prelude
            if payload['CYCLE'] == '000':
                if payload['DETAILS']:
                    details = payload['DETAILS']
                else:
                    details = ""
                send_mail(
                    payload['FLOAT_SERIAL_NO'] + ": "+"Mission prelude recieved",
                    payload['STATUS'] +" - "+ details,
                    'from@example.com',
                    ['randerson@whoi.edu','dnicholson@whoi.edu'],
                    fail_silently=False,
                )

            #first cycle
            if payload['CYCLE'] == '001':
                if payload['DETAILS']:
                    details = payload['DETAILS']
                else:
                    details = ""
                send_mail(
                    payload['FLOAT_SERIAL_NO'] + ": "+"First cycle recieved",
                    payload['STATUS'] +" - "+ details,
                    'from@example.com',
                    ['randerson@whoi.edu','dnicholson@whoi.edu'],
                    fail_silently=False,
                )
    except Exception:
        pass

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def put_process_log(request):
    #Updates or adds process log entries

    directory = request.GET['DIRECTORY']
    payload = json.loads(request.body)
    
    try:
        log_item = file_processing.objects.filter(DIRECTORY=directory)
        send_email(payload, log_item) #only send email if new record
        if log_item: #Log entry already exists
            log_item.update(**payload)
            return JsonResponse({'status': 'updated'}, safe=False, status=status.HTTP_200_OK)
        else: #Create new entry
            file_processing.objects.create(DIRECTORY=directory, **payload)
            return JsonResponse({'status': 'added'}, safe=False, status=status.HTTP_200_OK)
    except Exception:
        return JsonResponse({'error': 'Something terrible went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)