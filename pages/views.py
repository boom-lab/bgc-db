from django.shortcuts import redirect
from django.http import JsonResponse
from django.db.models import Sum, Max
from django.forms.models import model_to_dict
from deployments.models import deployment
from deployments.serializers import TrackingSerializer
from sensor_qc.serializers import SensorQCdataSerializer, SensorQCserializer
from rest_framework import generics
from env_data.models import continuous_profile, cycle_metadata, discrete_profile, nitrate_continuous_profile, park
from sensor_qc.models import sensor_qc

import pandas as pd
from datetime import datetime, timedelta
import pytz

#----------------Redirect--------------------#
def newsite(request):
    page = request.META['PATH_INFO']
    return redirect("http://argo.whoifloatgroup.org"+page)

#---------Front End - Data for Plots and Maps -------#

# Sensor QC page
class GetSensorQCdata(generics.ListAPIView): #Read only
    serializer_class = SensorQCdataSerializer
    queryset = sensor_qc.objects.all()

#Float tracking
class GetTrackingData(generics.ListAPIView):
    serializer_class = TrackingSerializer
    queryset = deployment.objects.filter(PLATFORM_TYPE='NAVIS_EBR').order_by('FLOAT_SERIAL_NO')

# Serial numnbers page
def serial_number_data(request):
    if request.method=="GET":
        query = deployment.objects.filter(PLATFORM_TYPE='NAVIS_EBR').order_by('FLOAT_SERIAL_NO').prefetch_related("sensors")

        res = []
        for dep in query:
            record = {}
            record["FLOAT_SERIAL_NO"] = dep.FLOAT_SERIAL_NO
            record["PLATFORM_NUMBER"] = dep.PLATFORM_NUMBER
            record["DEPLOYMENT_CRUISE_ID"] = dep.DEPLOYMENT_CRUISE_ID
            record["LAST_EVENT"] = dep.last_event["EVENT"].VALUE
            for sensor in dep.sensors.prefetch_related("SENSOR").all():
                record[sensor.SENSOR.VALUE] = sensor.SENSOR_SERIAL_NO
            res.append(record)
        return JsonResponse(res, status = 200, safe=False)

    return JsonResponse({}, status = 400)

def float_detail(request):
    FLOAT_SERIAL_NO = request.GET.get('FLOAT_SERIAL_NO', None)
    PLATFORM_TYPE = request.GET.get('PLATFORM_TYPE', None)
    PLATFORM_NUMBER = request.GET.get('PLATFORM_NUMBER', None)

    #Filters
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


    qcfilters = {}
    if PLATFORM_NUMBER:
        qcfilters['SENSOR__DEPLOYMENT__PLATFORM_NUMBER'] = PLATFORM_NUMBER
    else:
        qcfilters['SENSOR__DEPLOYMENT__FLOAT_SERIAL_NO'] = FLOAT_SERIAL_NO
        qcfilters['SENSOR__DEPLOYMENT__PLATFORM_TYPE'] = PLATFORM_TYPE



    n_reports = cycle_metadata.objects.filter(**filters).count()

    #If deployed
    if n_reports > 0:

        latest_cycle_meta = cycle_metadata.objects.filter(**filters).order_by("-GpsFixDate").first()

        #Cycle metadata timseries data
        cols = [f.name for f in cycle_metadata._meta.get_fields()]
        query = cycle_metadata.objects.filter(**filters).order_by("ProfileId").values_list(*cols)
        data = pd.DataFrame(query, columns=cols)
        

        #Duration
        #Substract start of cycle time from all other values
        data["TimeStartDescent_py_delta"] = (data["TimeStartDescent"] - data["TimeStartDescent"])
        data["GpsFixDate_py_delta"] = (data["GpsFixDate"] - data["TimeStartDescent"])
        data["TimeStartPark_py_delta"] = (data["TimeStartPark"] - data["TimeStartDescent"])
        data["TimeStartProfileDescent_py_delta"] = (data["TimeStartProfileDescent"] - data["TimeStartDescent"])
        data["TimeStartProfile_py_delta"] = (data["TimeStartProfile"] - data["TimeStartDescent"])
        data["TimeStopProfile_py_delta"] = (data["TimeStopProfile"] - data["TimeStartDescent"]) 
        data["TimeStartTelemetry_py_delta"] = (data["TimeStartTelemetry"] - data["TimeStartDescent"])

        data["TimeStartDescent_delta"] = (data["TimeStartDescent_py_delta"] + pd.to_datetime('1970/01/01')).dt.strftime("%Y-%m-%d %H:%M:%S")
        data["GpsFixDate_delta"] = (data["GpsFixDate_py_delta"] + pd.to_datetime('1970/01/01')).dt.strftime("%Y-%m-%d %H:%M:%S")
        data["TimeStartPark_delta"] = (data["TimeStartPark_py_delta"] +pd .to_datetime('1970/01/01')).dt.strftime("%Y-%m-%d %H:%M:%S")
        data["TimeStartProfileDescent_delta"] = (data["TimeStartProfileDescent_py_delta"] + pd.to_datetime('1970/01/01')).dt.strftime("%Y-%m-%d %H:%M:%S")
        data["TimeStartProfile_delta"] = (data["TimeStartProfile_py_delta"] + pd.to_datetime('1970/01/01')).dt.strftime("%Y-%m-%d %H:%M:%S")
        data["TimeStopProfile_delta"] = (data["TimeStopProfile_py_delta"] + pd.to_datetime('1970/01/01')).dt.strftime("%Y-%m-%d %H:%M:%S")
        data["TimeStartTelemetry_delta"] = (data["TimeStartTelemetry_py_delta"] + pd.to_datetime('1970/01/01')).dt.strftime("%Y-%m-%d %H:%M:%S")

        #Surface duration
        data["GPS_DURATION_plotly"] = data["GPS_DURATION"] + pd.to_datetime('1970/01/01')
        data["TRANS_DURATION_plotly"] = data["TRANS_DURATION"] + pd.to_datetime('1970/01/01')

        #Hover data
        duration_hov_data = data.loc[:,["TimeStartDescent_py_delta",
            "GpsFixDate_py_delta",
            "TimeStartPark_py_delta",
            "TimeStartProfileDescent_py_delta",
            "TimeStartProfile_py_delta",
            "TimeStopProfile_py_delta",
            "TimeStartTelemetry_py_delta"]].astype(str).values.tolist()

        surface_duration_hov_data = data.loc[:,["GPS_DURATION",
        "TRANS_DURATION"]].astype(str).values.tolist()

        hov = pd.DataFrame()
        hov["GpsFixDate"] = data["GpsFixDate"]
        hov["GpsFixDate"] = hov.GpsFixDate.dt.strftime('%Y-%m-%d')
        general_hov_data = hov.values.tolist()


        data = data.where(pd.notnull(data), None) #Convert NaN to None (which turns into null in API)

        cycle_meta_data = {}
        for col in data.columns:
            cycle_meta_data[col]=data[col].to_list()

        #Sensor QC data
        sensor_qcs = sensor_qc.objects.filter(**qcfilters)
        sensor_qcs_ser = SensorQCserializer(sensor_qcs, many=True)

        #Monthly upload
        now = datetime.utcnow()
        now = now.replace(tzinfo=pytz.utc)
        last_month = now - timedelta(days=30)
        if dep.LAUNCH_DATE < last_month:
            query = cycle_metadata.objects.filter(TimeStartProfile__gte=last_month).aggregate(msg=Sum('MSG_BYTES'),log=Sum('LOG_BYTES'),isus=Sum('ISUS_BYTES'))
            monthly_upload = round((query['msg'] + query['log'] + query['isus'])/1000,1)
        else:
            monthly_upload = ""

        #Park Pressure data
        query = park.objects.filter(**filters).order_by("PROFILE_ID","DATE_MEASURED").values_list("PROFILE_ID","PRES")
        park_data = pd.DataFrame(query, columns=["PROFILE_ID","PRES"])
        park_data['PROFILE_ID'] = park_data.PROFILE_ID.str.split('.').str[1]
        park_data['cycle'] = park_data.groupby("PROFILE_ID").cumcount()
        park_data = park_data.pivot(index='PROFILE_ID',columns='cycle',values='PRES').reset_index()
        park_data = park_data.where(pd.notnull(park_data), None)
        park_json = {}
        for col in park_data.columns:
            park_json[col]=park_data[col].to_list()

        #Profile start pressure data
        query = discrete_profile.objects.filter(**filters).values('PROFILE_ID').annotate(max=Max('PRES')).values_list("PROFILE_ID","max")
        start_pres_data = pd.DataFrame(query, columns=["PROFILE_ID","PRES"])
        start_pres_data = start_pres_data.where(pd.notnull(start_pres_data), None)
        start_pres_data['PROFILE_ID'] = start_pres_data.PROFILE_ID.str.split('.').str[1]
        start_pres_json = {}
        start_pres_json['PROFILE_ID'] = start_pres_data['PROFILE_ID'].to_list()
        start_pres_json['PRES']= start_pres_data['PRES'].to_list()

        context = {
            'latest_cycle_metadata': model_to_dict(latest_cycle_meta),
            'monthly_upload':monthly_upload,
            'sensor_qcs':sensor_qcs_ser.data,
            'cycle_metadata':cycle_meta_data,
            'park_pres_data':park_json,
            'profile_start_pres_data':start_pres_json,
            'duration_hov_data':duration_hov_data,
            'surface_duration_hov_data':surface_duration_hov_data,
            'general_hov_data':general_hov_data
        }
        return JsonResponse(context, status = 200, safe=False)
    else: #Pre deployment
        context = {
            'cycle_metadata': None,
            'calc':None,
            'deployment':dep,
            'sensor_qcs':None
        }
        JsonResponse(context, status = 200, safe=False)

def map_data(request):
    
    if request.is_ajax and request.method == "GET":
        # get the selections
        deployments = request.GET.get("deployments", None).split(",")

        results = []
        for d in deployments:
            crt = {}
            #info 
            deployment_entry = deployment.objects.get(PLATFORM_NUMBER=d)
            crt['sn'] = deployment_entry.FLOAT_SERIAL_NO
            crt['wmo'] = deployment_entry.PLATFORM_NUMBER

            #Positions for traces
            hist_lat = list(cycle_metadata.objects.filter(DEPLOYMENT__PLATFORM_NUMBER=d).order_by('-GpsFixDate').all().values_list('GpsLat', flat=True))
            hist_lon = list(cycle_metadata.objects.filter(DEPLOYMENT__PLATFORM_NUMBER=d).order_by('-GpsFixDate').all().values_list('GpsLong', flat=True))

            combined = [None]*(len(hist_lon)+len(hist_lat))
            combined[::2] = hist_lon
            combined[1::2] = hist_lat
            crt['hist_positions'] = combined

            # profile_id = list(cycle_metadata.objects.filter(DEPLOYMENT__PLATFORM_NUMBER=d).order_by('-GpsFixDate').all().values_list('PROFILE_ID', flat=True))
            # profile_id = [x.split('.')[1] for x in profile_id] #Remove wmo number
            # time_start_p = pd.Series(cycle_metadata.objects.filter(DEPLOYMENT__PLATFORM_NUMBER=d).order_by(
            #     '-GpsFixDate').all().values_list('TimeStartTelemetry', flat=True))
            # time_start_p_human = time_start_p.dt.strftime('%Y-%m-%d %H:%M')
            # time_start_p_human = time_start_p_human.replace(np.nan, '')
            # #Hover data
            # hov_data = np.stack((profile_id, time_start_p_human, lat, lon),axis = -1)

            #Data for current location points
            crt['lat'] = cycle_metadata.objects.filter(DEPLOYMENT__PLATFORM_NUMBER=d).order_by('-GpsFixDate').first().GpsLat
            crt['long'] = cycle_metadata.objects.filter(DEPLOYMENT__PLATFORM_NUMBER=d).order_by('-GpsFixDate').first().GpsLong

            results.append(crt)

        return JsonResponse(results, status = 200, safe=False)

    return JsonResponse({}, status = 400)

def profile_explorer_query(prof, selected_var):
    prof_data = {}

    #Get profile metadata record
    profile = cycle_metadata.objects.get(PROFILE_ID=prof)
    prof_data["SN"]=profile.DEPLOYMENT.FLOAT_SERIAL_NO
    prof_data["WMO"]=profile.DEPLOYMENT.PLATFORM_NUMBER
    prof_data["PROFILE_ID"]=prof

    #Get continuous data
    if selected_var not in ["NITRATE","VK_PH","IB_PH","IK_PH"]:
        con_query = continuous_profile.objects.filter(PROFILE_ID=prof).order_by(
            "PRES").values_list("PRES", selected_var)
        con_data = pd.DataFrame(con_query, columns=["PRES",selected_var])
        con_data = con_data.dropna()
        prof_data["CON_PRES"]=con_data.PRES.to_list()
        prof_data["CON_"+selected_var]=con_data[selected_var].to_list()

    elif selected_var == "NITRATE":
        con_query = nitrate_continuous_profile.objects.filter(PROFILE_ID=prof).order_by(
            "PRES").values_list("PRES", "NO3")
        
        con_data = pd.DataFrame(con_query, columns=["PRES",selected_var])
        con_data = con_data.dropna()
        prof_data["CON_PRES"]=con_data.PRES.to_list()
        prof_data["CON_"+selected_var]=con_data[selected_var].to_list()


    #Get discrete data
    dis_query = discrete_profile.objects.filter(PROFILE_ID=prof).order_by(
        "PRES").values_list("PRES", selected_var)
    dis_data = pd.DataFrame(dis_query, columns=["PRES",selected_var])
    dis_data = dis_data.dropna()
    prof_data["DIS_PRES"]=dis_data.PRES.to_list()
    prof_data["DIS_"+selected_var]=dis_data[selected_var].to_list()

    return prof_data

def profile_explorer_data(request):
    if request.method == "GET":
        # get the selections from parameters
        profiles = request.GET.get("profiles", None).split(",")
        top_var = request.GET.get("top_var", None)
        bot_var = request.GET.get("bot_var", None)

        #No profiles selected
        if profiles == ['']:
            return JsonResponse({}, status=200)

        plot_data = {}
        #Bottom axis data
        if bot_var not in ["null","undefined"]:
            bottom_data = []
            for prof in profiles:
                prof_data = profile_explorer_query(prof, bot_var)
                bottom_data.append(prof_data)
            plot_data["BOTTOM_DATA"] = bottom_data

        #top axis data
        if top_var not in ["null","undefined"]:
            top_data = []
            for prof in profiles:
                prof_data = profile_explorer_query(prof, top_var)
                top_data.append(prof_data)
            plot_data["TOP_DATA"] = top_data
    
        return JsonResponse(plot_data, status = 200)
    return JsonResponse({}, status = 400)

def compare_latest_profiles_data(request):
    if request.method == "GET":
        # get the selections from parameters
        deployments = request.GET.get("deployments", None).split(",")
        var_selected = request.GET.get("var_selected", None)

        plot_data = []

        if var_selected not in ["NITRATE","VK_PH","IB_PH","IK_PH"]:
            for dep in deployments:
                #Get most recent cycle metadata record
                profile = cycle_metadata.objects.filter(DEPLOYMENT__PLATFORM_NUMBER=dep).order_by(
                    '-PROFILE_ID').first()

                #Get continuous data
                con_query = continuous_profile.objects.filter(PROFILE_ID=profile).order_by(
                    "PRES").values_list("PRES", var_selected)

                con_data = pd.DataFrame(con_query, columns=["PRES",var_selected])
                con_data = con_data.dropna()

                #Get discrete data
                dis_query = discrete_profile.objects.filter(PROFILE_ID=profile).order_by(
                    "PRES").values_list("PRES", var_selected)

                dis_data = pd.DataFrame(dis_query, columns=["PRES",var_selected])
                dis_data = dis_data.dropna()

                plot_data.append({
                    "SN":profile.DEPLOYMENT.FLOAT_SERIAL_NO,
                    "WMO":dep,
                    "CON_PRES":con_data.PRES.to_list(),
                    "CON_"+var_selected: con_data[var_selected].to_list(),
                    "DIS_PRES":dis_data.PRES.to_list(),
                    "DIS_"+var_selected: dis_data[var_selected].to_list()
                })
        
        elif var_selected == "NITRATE":
            for dep in deployments:
                #Get most recent cycle metadata record
                profile = cycle_metadata.objects.filter(DEPLOYMENT__PLATFORM_NUMBER=dep).order_by(
                    '-PROFILE_ID').first()

                #Get continuous data
                con_query = nitrate_continuous_profile.objects.filter(PROFILE_ID=profile).order_by(
                    "PRES").values_list("PRES", "NO3")

                con_data = pd.DataFrame(con_query, columns=["PRES",var_selected])
                con_data = con_data.dropna()

                #Get discrete data
                dis_query = discrete_profile.objects.filter(PROFILE_ID=profile).order_by(
                    "PRES").values_list("PRES", var_selected)

                dis_data = pd.DataFrame(dis_query, columns=["PRES",var_selected])
                dis_data = dis_data.dropna()

                plot_data.append({
                    "SN":profile.DEPLOYMENT.FLOAT_SERIAL_NO,
                    "WMO":dep,
                    "CON_PRES":con_data.PRES.to_list(),
                    "CON_"+var_selected: con_data[var_selected].to_list(),
                    "DIS_PRES":dis_data.PRES.to_list(),
                    "DIS_"+var_selected: dis_data[var_selected].to_list()
                })

        elif var_selected  in ["VK_PH","IB_PH","IK_PH"]:
            for dep in deployments:
                #Get most recent cycle metadata record
                profile = cycle_metadata.objects.filter(DEPLOYMENT__PLATFORM_NUMBER=dep).order_by(
                    '-PROFILE_ID').first()

                #Get discrete data
                dis_query = discrete_profile.objects.filter(PROFILE_ID=profile).order_by(
                    "PRES").values_list("PRES", var_selected)

                dis_data = pd.DataFrame(dis_query, columns=["PRES",var_selected])
                dis_data = dis_data.dropna()

                plot_data.append({
                    "SN":profile.DEPLOYMENT.FLOAT_SERIAL_NO,
                    "WMO":dep,
                    "CON_PRES":[],
                    "CON_"+var_selected: [],
                    "DIS_PRES":dis_data.PRES.to_list(),
                    "DIS_"+var_selected: dis_data[var_selected].to_list()
                })

    
        return JsonResponse(plot_data, status = 200, safe=False)
    return JsonResponse({}, status = 400)

def latest_profiles_data(request):
    if request.method == "GET":

        year = request.GET.get("year", None)


        #Cycle metadata query
        cycle_meta_query = cycle_metadata.objects.filter(DEPLOYMENT__LAUNCH_DATE__year=year).order_by(
            '-DEPLOYMENT__id','-PROFILE_ID').distinct('DEPLOYMENT__id')
        
        #latest continuous data query
        con_query = continuous_profile.objects.filter(PROFILE_ID__in=cycle_meta_query.values_list("PROFILE_ID")).order_by(
            "PROFILE_ID", "PRES").values_list("DEPLOYMENT__PLATFORM_NUMBER", 
            "PRES", "PSAL","TEMP","DOXY","CHLA","BBP700","CDOM","PH_IN_SITU_TOTAL")

        #latest nitrate continuous data
        nitrate_query = nitrate_continuous_profile.objects.filter(PROFILE_ID__in=cycle_meta_query.values_list("PROFILE_ID")).order_by(
            "PROFILE_ID", "PRES").values_list("DEPLOYMENT__PLATFORM_NUMBER", "PRES", "NO3")

        #Latest discrete data query
        dis_query = discrete_profile.objects.filter(PROFILE_ID__in=cycle_meta_query.values_list("PROFILE_ID")).order_by(
            "PROFILE_ID", "PRES").values_list("DEPLOYMENT__PLATFORM_NUMBER", 
            "PRES", "PSAL","TEMP","DOXY","CHLA","BBP700","CDOM","PH_IN_SITU_TOTAL","NITRATE")
        
        #Get data and convert to dataframes
        con_data = pd.DataFrame(con_query, columns=["PLATFORM_NUMBER", "PRES", "PSAL",
            "TEMP","DOXY","CHLA","BBP700","CDOM","PH_IN_SITU_TOTAL"])
        con_data = con_data.where(pd.notnull(con_data), None)

        nitrate_data = pd.DataFrame(nitrate_query, columns=["PLATFORM_NUMBER", 
            "PRES", "NITRATE"])
        nitrate_data = nitrate_data.where(pd.notnull(nitrate_data), None)

        dis_data = pd.DataFrame(dis_query, columns=["PLATFORM_NUMBER", 
            "PRES", "PSAL","TEMP","DOXY","CHLA","BBP700","CDOM","PH_IN_SITU_TOTAL","NITRATE"])
        dis_data = dis_data.where(pd.notnull(dis_data), None)
        
        plot_data =[]
        for cycle in cycle_meta_query:
            wmo = cycle.DEPLOYMENT.PLATFORM_NUMBER
            deployment_data = {
                "FLOAT_SERIAL_NO": cycle.DEPLOYMENT.FLOAT_SERIAL_NO,
                "PLATFORM_NUMBER":wmo,
                "PROFILE_ID":cycle.PROFILE_ID,
                "TIMESTARTPROFILE":cycle.TimeStartProfile,
                "CONTINUOUS_DATA":{
                    "PRES":con_data.loc[con_data.PLATFORM_NUMBER==wmo,"PRES"].to_list(),
                    "PSAL":con_data.loc[con_data.PLATFORM_NUMBER==wmo,"PSAL"].to_list(),
                    "TEMP":con_data.loc[con_data.PLATFORM_NUMBER==wmo,"TEMP"].to_list(),
                    "DOXY":con_data.loc[con_data.PLATFORM_NUMBER==wmo,"DOXY"].to_list(),
                    "CHLA":con_data.loc[con_data.PLATFORM_NUMBER==wmo,"CHLA"].to_list(),
                    "BBP700":con_data.loc[con_data.PLATFORM_NUMBER==wmo,"BBP700"].to_list(),
                    "CDOM":con_data.loc[con_data.PLATFORM_NUMBER==wmo,"CDOM"].to_list(),
                    "PH_IN_SITU_TOTAL":con_data.loc[con_data.PLATFORM_NUMBER==wmo,"PH_IN_SITU_TOTAL"].to_list(),
                },
                "CONTINUOUS_NITRATE_DATA":{
                    "NITRATE":nitrate_data.loc[nitrate_data.PLATFORM_NUMBER==wmo,"NITRATE"].to_list()
                },
                "DISCRETE_DATA":{
                    "PRES":dis_data.loc[dis_data.PLATFORM_NUMBER==wmo,"PRES"].to_list(),
                    "PSAL":dis_data.loc[dis_data.PLATFORM_NUMBER==wmo,"PSAL"].to_list(),
                    "TEMP":dis_data.loc[dis_data.PLATFORM_NUMBER==wmo,"TEMP"].to_list(),
                    "DOXY":dis_data.loc[dis_data.PLATFORM_NUMBER==wmo,"DOXY"].to_list(),
                    "CHLA":dis_data.loc[dis_data.PLATFORM_NUMBER==wmo,"CHLA"].to_list(),
                    "BBP700":dis_data.loc[dis_data.PLATFORM_NUMBER==wmo,"BBP700"].to_list(),
                    "CDOM":dis_data.loc[dis_data.PLATFORM_NUMBER==wmo,"CDOM"].to_list(),
                    "PH_IN_SITU_TOTAL":dis_data.loc[dis_data.PLATFORM_NUMBER==wmo,"PH_IN_SITU_TOTAL"].to_list(),
                    "NITRATE":dis_data.loc[dis_data.PLATFORM_NUMBER==wmo,"NITRATE"].to_list()
                }
            }
            plot_data.append(deployment_data)

        return JsonResponse(plot_data, status = 200, safe=False)
    return JsonResponse({}, status = 400)


def all_profiles_data(request):
    if request.method == "GET":

        year = request.GET.get("year", None)
        var_selected = request.GET.get("var_selected")

        #Get list of profiles
        cycle_meta_q = cycle_metadata.objects.filter(DEPLOYMENT__LAUNCH_DATE__year=year).order_by("PROFILE_ID").values_list(
            "PROFILE_ID","ProfileId","DEPLOYMENT__FLOAT_SERIAL_NO","DEPLOYMENT__PLATFORM_NUMBER","TimeStartProfile")
        cycle_meta = pd.DataFrame(cycle_meta_q, columns=["PROFILE_ID","CYCLE_ID","FLOAT_SERIAL_NO","PLATFORM_NUMBER","TimeStartProfile"])

        #Continuous data
        if var_selected not in ["NITRATE","VK_PH","IB_PH","IK_PH"]:
            query = continuous_profile.objects.filter(PROFILE_ID__in=cycle_meta.PROFILE_ID).order_by("PROFILE_ID", "PRES").values_list(
                "DEPLOYMENT__PLATFORM_NUMBER","PROFILE_ID", "PRES", var_selected)
            data = pd.DataFrame(query, columns=["PLATFORM_NUMBER","PROFILE_ID", "PRES", var_selected])
            data = data.fillna("")

        #Discrete data
        query = discrete_profile.objects.filter(PROFILE_ID__in=cycle_meta.PROFILE_ID).order_by("PROFILE_ID", "PRES").values_list(
            "DEPLOYMENT__PLATFORM_NUMBER","PROFILE_ID", "PRES", var_selected)
        dis_data = pd.DataFrame(query, columns=["PLATFORM_NUMBER","PROFILE_ID", "PRES", var_selected])
        dis_data = dis_data.fillna("")

        if var_selected == "NITRATE":
            query = nitrate_continuous_profile.objects.filter(PROFILE_ID__in=cycle_meta.PROFILE_ID).order_by("PROFILE_ID", "PRES").values_list(
                "DEPLOYMENT__PLATFORM_NUMBER","PROFILE_ID", "PRES", "NO3")
            data = pd.DataFrame(query, columns=["PLATFORM_NUMBER","PROFILE_ID", "PRES", "NITRATE"])
            data = data.fillna("")

        #Remove cycle metadata that does not have continuous data (failed profile cycle)
        keep_profiles = dis_data.PROFILE_ID.unique()
        cycle_meta = cycle_meta.loc[cycle_meta.PROFILE_ID.isin(keep_profiles),:]

        #Remove discrete data that does not hve continuous data (failed profile cycle)
        dis_data = dis_data.loc[dis_data.PROFILE_ID.isin(keep_profiles),:]

        plot_data = []
        #Loop through each float
        for wmo in cycle_meta.PLATFORM_NUMBER.unique():
            #continuous
            if var_selected not in ["VK_PH","IB_PH","IK_PH"]:
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
            single_plot = {"x":var_flat,
                "y":pres_flat,
                "dis_x":dis_var_flat,
                "dis_y":dis_pres_flat,
                "TIME_START_PROFILE":time_start,
                "DAY":day,
                "CYCLE_ID":cycle_id,
                "sn":sn,
                "wmo":wmo,
            }
            plot_data.append(single_plot)

        return JsonResponse(plot_data, status=200, safe=False)

    return JsonResponse({}, status = 400)

#---------------------Selector Lists ------------------------------#

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
        platform_number = deployment.objects.filter(HISTORICAL=False).exclude(cycle_metadata=None).all().values_list('PLATFORM_NUMBER', flat=True)
        float_serial_no = deployment.objects.filter(HISTORICAL=False).exclude(cycle_metadata=None).all().values_list('FLOAT_SERIAL_NO', flat=True)

        res = []
        for i, item in enumerate(platform_number):
            res.append({'PLATFORM_NUMBER':item, "LABEL":"WMO: " + str(item) + " SN:" + str(float_serial_no[i])})

        return JsonResponse({"deployments":res}, status = 200)

    return JsonResponse({}, status = 400)
