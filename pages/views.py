from django.shortcuts import render
from django.http import JsonResponse
from deployments.models import deployment
from env_data.models import cycle_metadata

import pages.engineering_plots as ep

def index(request):
    deployments = deployment.objects.filter(HISTORICAL=False)

    context = {
        'deployments': deployments,
    }
    return render(request, 'pages/index.html', context)

def profile_plot(request):
    return render(request, 'pages/profile_plot.html')

def cohort(request):
    return render(request, 'pages/cohort.html')

def cohort_latest(request):
    return render(request, 'pages/cohort_latest.html')

def display_map(request):
    return render(request, 'pages/map.html')

def float_detail(request):
    FLOAT_SERIAL_NO = request.GET.get('FLOAT_SERIAL_NO', None)
    PLATFORM_TYPE = request.GET.get('PLATFORM_TYPE', None)

    filters={}
    filters['DEPLOYMENT__FLOAT_SERIAL_NO'] = FLOAT_SERIAL_NO
    filters['DEPLOYMENT__PLATFORM_TYPE'] = PLATFORM_TYPE

    dfilters = {}
    dfilters['FLOAT_SERIAL_NO'] = FLOAT_SERIAL_NO
    dfilters['PLATFORM_TYPE'] = PLATFORM_TYPE
    dep = deployment.objects.get(**dfilters)

    n_reports = cycle_metadata.objects.filter(**filters).count()

    #If deployed
    if n_reports > 0:
        latest_cycle_meta = cycle_metadata.objects.filter(**filters).order_by("-GpsFixDate").first()

        abpres_plot = ep.single_var_plot(filters, "AirBladderPressure", y_label="Pressure", legend_label="Air Bladder Pressure")
        buoy_pump_time_plot = ep.single_var_plot(filters, "BuoyancyPumpOnTime", y_label="Time", 
            legend_label="Buoyancy Pump On Time")

        calc={}
        if latest_cycle_meta.MSG_BYTES:
            calc['MSG_KB'] = round(latest_cycle_meta.MSG_BYTES/1000,1)
        if latest_cycle_meta.ISUS_BYTES:
            calc['ISUS_KB'] = round(latest_cycle_meta.ISUS_BYTES/1000,1)
        if latest_cycle_meta.LOG_BYTES:
            calc['LOG_KB'] = round(latest_cycle_meta.LOG_BYTES/1000,1)
        if latest_cycle_meta.MSG_BYTES and latest_cycle_meta.ISUS_BYTES and latest_cycle_meta.LOG_BYTES:
            calc['TOTAL'] = calc['MSG_KB']+calc['ISUS_KB']+calc['LOG_KB']

        context = {
            'cycle_metadata': latest_cycle_meta,
            'calc':calc,
            'deployment':dep,
            'battery_plot':ep.volts_plot(filters),
            'amps_plot':ep.amps_plot(filters),
            'buoyancy_plot':ep.buoyancy_position_plot(filters),
            'air_bladder_pres_plot': abpres_plot,
            'buoy_pump_time_plot': buoy_pump_time_plot,
            'duration_plot':ep.duration_plot(filters),
            'con_attempt_plot':ep.con_attempt_plot(filters),
            'upload_attempt_plot':ep.upload_attempt_plot(filters),
            'surface_duration_plot':ep.surface_duration_plot(filters),
            'park_pres_plot':ep.park_pres_plot(filters),
            'profile_start_pres_plot':ep.profile_start_pres_plot(filters)
        }
        return render(request, 'pages/float_detail.html', context)
    else: #Pre deployment
        context = {
            'cycle_metadata': None,
            'calc':None,
            'deployment':dep,
        }
        return render(request, 'pages/float_detail.html', context)

def get_profiles_list(request):
    # for populating selector dropdown
    if request.is_ajax and request.method == "GET":
        profile_id = cycle_metadata.objects.all().values_list('PROFILE_ID', flat=True)

        return JsonResponse({'profiles': list(profile_id) }, status = 200)

    return JsonResponse({}, status = 400)


def get_deployments_list(request):
    # for populationg selector dropdown
    if request.is_ajax and request.method == "GET":
        platform_number = deployment.objects.filter(HISTORICAL=False).exclude(LAUNCH_DATE=None).all().values_list('PLATFORM_NUMBER', flat=True)
        float_serial_no = deployment.objects.filter(HISTORICAL=False).exclude(LAUNCH_DATE=None).all().values_list('FLOAT_SERIAL_NO', flat=True)

        res = []
        for i, item in enumerate(platform_number):
            res.append({'PLATFORM_NUMBER':item, "LABEL":"WMO: " + str(item) + " SN:" + str(float_serial_no[i])})

        return JsonResponse({"deployments":res}, status = 200)

    return JsonResponse({}, status = 400)