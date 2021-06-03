from django.http import HttpResponse
from django.shortcuts import get_object_or_404
import zipfile
from .models import mission
from django.core import serializers

def navis_crc(command_string):
    #Author: Ben Greenwood
    crc = 0x1D0F; # start value
    for c in command_string:
        crc = crc ^ (ord(c) * 256)
        for i in range(8,0,-1):
            if (crc & 0x8000):
                crc = (crc*2) ^ 0x1021
            else:
                crc = (crc*2)
        return crc & 0xffff

def gen_commands(data):
    #Create mission configuration command string
    output = ""
    for key, value in data.items():
        if key not in ['DEPLOYMENT','ADD_DATE','COMMENTS', 'ActivateRecoveryMode']: #Ignore these fields
            if value: #Ignore blank entries
                command = key + "(" + str(value) + ")" #command
                white_space = (32 - len(command)) * " "
                crc = '%04X' % navis_crc(command) #checksum
                output = output + command + white_space + "[0x" + str(crc).lower() + "]" + "\n" #add to output as new line

        if key == "ActivateRecoveryMode" and value: #Recovery mode command
            command = "ActivateRecoveryMode()          [0x9848]\n" + command

    return output

#Create NAVIS mission config file
def export_NAVIS_mission_config(request, entry_ids):
    """Tested with NAVIS_EBR float"""

    if len(entry_ids) == 1: #If only one record selected
        #Get data from mission
        m = get_object_or_404(mission, pk=entry_ids[0])
        data = serializers.serialize("python", [m])[0]['fields']
        output = gen_commands(data)
       
        #Return file
        response = HttpResponse(output, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="{}_{}.cfg"'.format(m.DEPLOYMENT.FLOAT_SERIAL_NO, m.ADD_DATE.strftime("%Y_%m_%d"))
        return response
    else:
        response = HttpResponse(content_type='application/zip')
        zf = zipfile.ZipFile(response, 'w')
        for entry in entry_ids: #loop through each mission record selected
            m = get_object_or_404(mission, pk=entry)
            data = serializers.serialize("python", [m])[0]['fields']
            output = gen_commands(data)
            filename="{}_{}.cfg".format(m.DEPLOYMENT.FLOAT_SERIAL_NO, m.ADD_DATE.strftime("%Y_%m_%d"))
            zf.writestr(filename, output)
        zf.close()
        response['Content-Disposition'] = 'attachment; filename={}'.format("configs.zip")
        return response