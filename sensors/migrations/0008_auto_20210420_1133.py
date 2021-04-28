# Generated by Django 3.2 on 2021-04-20 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sensors', '0007_auto_20210420_1126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensor',
            name='SENSOR',
            field=models.CharField(choices=[('FLUOROMETER_CHLA', 'Fluorometer measuring chlorophyll-a'), ('TRANSISTOR_PH', 'Transistor measuring pH'), ('CTD_CNDC', 'Conductivity Temperature Depth (CTD) sensors package measuring conductivity'), ('CTD_PRES', 'Conductivity Temperature Depth (CTD) sensors package measuring pressure'), ('CTD_TEMP', 'Conductivity Temperature Depth (CTD) sensors package measuring temperature'), ('OPTODE_DOXY', 'Optode measuring dissolved oxygen'), ('SPECTROPHOTOMETER_NITRATE', 'Spectrophotometer measuring nitrate'), ('FLUOROMETER_CDOM', 'Fluorometer measuring Colored Dissolved Organic Matter (CDOM)'), ('RADIOMETER_PAR', 'Radiometer measuring Photosynthetically Active Radiation (PAR)'), ('BACKSCATTERINGMETER_BBP700', 'Backscattering meter measuring backscattering at 700 nanometers'), ('PUMP_VOLTAGE', 'PUMP_VOLTAGE'), ('CPU_VOLTAGE', 'CPU_VOLTAGE')], max_length=50),
        ),
        migrations.AlterField(
            model_name='sensor',
            name='SENSOR_MAKER',
            field=models.CharField(blank=True, choices=[('JAC', 'JFE Advantech Co., Ltd'), ('WETLABS', 'Wetlabs Inc.'), ('SBE', 'Sea-Bird Scientific'), ('MBARI', 'Monterey Bay Aquarium Research Institute'), ('DRUCK', 'Druck Inc.'), ('SATLANTIC', 'Satlantic Inc.')], max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='sensor',
            name='SENSOR_MODEL',
            field=models.CharField(blank=True, choices=[('DRUCK_2900PSIA', 'Druck pressure sensor with 2900 PSIA rating'), ('SBE41CP_V3.0c', 'Sea-Bird Scientific SBE 41CP CTD V3.0c'), ('DURAFET', 'DURAFET'), ('MCOMS', 'MCOMS'), ('SBE63_V3.2.2', 'SBE63_V3.2.2'), ('SUNA_V2', 'SUNA_V2'), ('SBE41CP_V5.3.4', 'SBE41CP_V5.3.4')], max_length=25, null=True),
        ),
    ]