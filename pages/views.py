from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Sum
from deployments.models import deployment
from env_data.models import continuous_profile, cycle_metadata, discrete_profile
import pandas as pd
import cmocean
import numpy as np
from datetime import datetime, timedelta
import pytz

import pages.engineering_plots as ep



def index(request):
    deployments = deployment.objects.filter(LAUNCH_DATE__isnull=False).filter(HISTORICAL=False)

    context = {
        'deployments': deployments,
    }
    return render(request, 'pages/index.html', context)

def floats_predeployment(request):
    deployments = deployment.objects.filter(LAUNCH_DATE__isnull=True).filter(HISTORICAL=False)

    context = {
        'deployments': deployments,
    }
    return render(request, 'pages/floats_predeployment.html', context)

def profile_explorer(request):
    return render(request, 'pages/profile_explorer.html')

def cohort(request):
    return render(request, 'pages/cohort.html')

def cohort(request):
    return render(request, 'pages/cohort.html')

def cohort_latest(request):
    return render(request, 'pages/cohort_latest.html')

def display_map(request):
    return render(request, 'pages/map.html')

def float_tracking(request):
    deps = deployment.objects.filter(PLATFORM_TYPE='NAVIS_EBR').order_by('FLOAT_SERIAL_NO')
    context = {'deployments':deps}
    return render(request, 'pages/float_tracking.html', context)

def float_detail(request):
    FLOAT_SERIAL_NO = request.GET.get('FLOAT_SERIAL_NO', None)
    PLATFORM_TYPE = request.GET.get('PLATFORM_TYPE', None)
    PLATFORM_NUMBER = request.GET.get('PLATFORM_NUMBER', None)

    filters={}
    if PLATFORM_NUMBER:
        filters['DEPLOYMENT__PLATFORM_NUMBER'] = PLATFORM_NUMBER
    else:
        filters['DEPLOYMENT__FLOAT_SERIAL_NO'] = FLOAT_SERIAL_NO
        filters['DEPLOYMENT__PLATFORM_TYPE'] = PLATFORM_TYPE

    dfilters = {}
    if PLATFORM_NUMBER:
        dfilters['PLATFORM_NUMBER'] = PLATFORM_NUMBER
    else:
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
        vacuum_plot = ep.single_var_plot(filters, "Vacuum", y_label="Pressure", legend_label="Internal Vacuum")

        #Monthly upload
        now = datetime.utcnow()
        now = now.replace(tzinfo=pytz.utc)
        last_month = now - timedelta(days=30)
        if dep.LAUNCH_DATE < last_month:
            query = cycle_metadata.objects.filter(TimeStartProfile__gte=last_month).aggregate(msg=Sum('MSG_BYTES'),log=Sum('LOG_BYTES'),isus=Sum('ISUS_BYTES'))
            monthly_upload = round((query['msg'] + query['log'] + query['isus'])/1000,1)
        else:
            monthly_upload = ""

        context = {
            'cycle_metadata': latest_cycle_meta,
            'deployment':dep,
            'monthly_upload':monthly_upload,
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
            'profile_start_pres_plot':ep.profile_start_pres_plot(filters),
            'vacuum_plot':vacuum_plot
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
        query = cycle_metadata.objects.all().values_list('PROFILE_ID', flat=True)
        profile_ids = list(query)
        profile_ids.sort()
        return JsonResponse({'profiles': profile_ids }, status = 200)

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

def cmocean_to_plotly(cmap, pl_entries):
    """Function to sample cmocean colors and output list of rgb values for plotly
    cmap = color map from cmocean
    pl_entries = number of samples to take"""
    
    #Sample 40 colors from cmap
    colors_n = 40
    h = 1.0/(colors_n-1)
    pl_colorscale = []
    for k in range(colors_n):
        C = list(map(np.uint8, np.array(cmap(k*h)[:3])*255))
        pl_colorscale.append('rgb'+str((C[0], C[1], C[2])))
    
    #Add light blue colors if older than 40 profiles
    solid_add = pl_entries - colors_n
    i = 0
    while i < solid_add:
        pl_colorscale.insert(0, 'rgb(207, 230, 233)')
        i+=1

    #chop scale if younger than 40 profiles
    if pl_entries < colors_n:
        final_scale = pl_colorscale[pl_entries*-1:]
    else:
        final_scale = pl_colorscale

    
    return final_scale

def cohort_data(request):
    # provides flat data to plotly cohort plot

    if request.is_ajax and request.method == "GET":
        year_selected = request.GET.get('year_selected', None)
        var_selected = request.GET.get('var_selected', None)

        #Get list of profiles
        cycle_meta_q = cycle_metadata.objects.filter(DEPLOYMENT__LAUNCH_DATE__year=year_selected).order_by("PROFILE_ID").values_list(
            "PROFILE_ID","ProfileId","DEPLOYMENT__FLOAT_SERIAL_NO","DEPLOYMENT__PLATFORM_NUMBER","TimeStartProfile")
        cycle_meta = pd.DataFrame(cycle_meta_q, columns=["PROFILE_ID","CYCLE_ID","FLOAT_SERIAL_NO","PLATFORM_NUMBER","TimeStartProfile"])

        #Continuous data
        if var_selected != "NITRATE":
            query = continuous_profile.objects.filter(PROFILE_ID__in=cycle_meta.PROFILE_ID).order_by("PROFILE_ID", "PRES").values_list(
                "DEPLOYMENT__PLATFORM_NUMBER","PROFILE_ID", "PRES", var_selected)
            data = pd.DataFrame(query, columns=["PLATFORM_NUMBER","PROFILE_ID", "PRES", var_selected])
            data = data.fillna("")

        #Discrete data
        query = discrete_profile.objects.filter(PROFILE_ID__in=cycle_meta.PROFILE_ID).order_by("PROFILE_ID", "PRES").values_list(
            "DEPLOYMENT__PLATFORM_NUMBER","PROFILE_ID", "PRES", var_selected)
        dis_data = pd.DataFrame(query, columns=["PLATFORM_NUMBER","PROFILE_ID", "PRES", var_selected])
        dis_data = dis_data.fillna("")

        #Remove cycle metadata that does not have continuous data (failed profile cycle)
        keep_profiles = dis_data.PROFILE_ID.unique()
        cycle_meta = cycle_meta.loc[cycle_meta.PROFILE_ID.isin(keep_profiles),:]

        #Remove discrete data that does not hve continuous data (failed profile cycle)
        dis_data = dis_data.loc[dis_data.PROFILE_ID.isin(keep_profiles),:]

        plot_data = {}
        #Loop through each float
        for wmo in cycle_meta.PLATFORM_NUMBER.unique():
            #continuous
            if var_selected != "NITRATE":
                grouped_data = data.loc[data.PLATFORM_NUMBER==wmo,:].groupby("PROFILE_ID")
                var_flat = grouped_data[var_selected].apply(list).tolist()
                pres_flat = grouped_data["PRES"].apply(list).tolist()
            else:
                var_flat = None
                pres_flat = None

            #discrete
            dis_grouped_data = dis_data.loc[dis_data.PLATFORM_NUMBER==wmo,:].groupby("PROFILE_ID")
            dis_var_flat = dis_grouped_data[var_selected].apply(list).tolist()
            dis_pres_flat = dis_grouped_data["PRES"].apply(list).tolist()

            #Aux data
            sn = cycle_meta.loc[cycle_meta.PLATFORM_NUMBER==wmo,"FLOAT_SERIAL_NO"].iloc[0]
            time_start = cycle_meta.loc[cycle_meta.PLATFORM_NUMBER==wmo,"TimeStartProfile"].dt.strftime('%Y-%m-%d').tolist()
            day = cycle_meta.loc[cycle_meta.PLATFORM_NUMBER==wmo,"TimeStartProfile"].dt.dayofyear.tolist()
            cycle_id = cycle_meta.loc[cycle_meta.PLATFORM_NUMBER==wmo,"CYCLE_ID"].tolist()

            #continuous colormaps
            n_colors = len(cycle_id)
            cont_colors = cmocean_to_plotly(cmocean.cm.dense, n_colors)
            #print(cont_colors)
            plot_data[wmo] = {"x":var_flat,
                "y":pres_flat,
                "dis_x":dis_var_flat,
                "dis_y":dis_pres_flat,
                "TIME_START_PROFILE":time_start,
                "DAY":day,
                "CYCLE_ID":cycle_id,
                "sn":sn,
                "wmo":wmo,
                "continuous_colors":cont_colors
            }

        return JsonResponse(plot_data, status=200)

    return JsonResponse({}, status = 400)