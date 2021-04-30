# Generated by Django 3.2 on 2021-04-29 12:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('deployments', '0024_alter_deployment_platform_number'),
        ('env_data', '0003_auto_20210429_0818'),
    ]

    operations = [


        migrations.AlterField(
            model_name='park',
            name='OTV',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='cycle_metadata',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DATE_ADD', models.DateTimeField()),
                ('PROFILE_ID', models.CharField(blank=True, default=0, max_length=20, null=True, unique=True)),
                ('ActiveBallastAdjustments', models.IntegerField(blank=True, null=True)),
                ('AirBladderPressure', models.IntegerField(blank=True, null=True)),
                ('AirPumpAmps', models.IntegerField(blank=True, null=True)),
                ('AirPumpVolts', models.IntegerField(blank=True, null=True)),
                ('BatteryCounts', models.IntegerField(blank=True, null=True)),
                ('BuoyancyPumpOnTime', models.IntegerField(blank=True, null=True)),
                ('BuoyancyPumpAmps', models.IntegerField(blank=True, null=True)),
                ('BuoyancyPumpVolts', models.IntegerField(blank=True, null=True)),
                ('CurrentBuoyancyPosition', models.IntegerField(blank=True, null=True)),
                ('DeepProfileBuoyancyPosition', models.IntegerField(blank=True, null=True)),
                ('FlashErrorsCorrectable', models.IntegerField(blank=True, null=True)),
                ('FlashErrorsUncorrectable', models.IntegerField(blank=True, null=True)),
                ('FloatId', models.IntegerField(blank=True, null=True)),
                ('GpsFixTime', models.IntegerField(blank=True, null=True)),
                ('IceMLSample', models.IntegerField(blank=True, null=True)),
                ('McomsAmps', models.IntegerField(blank=True, null=True)),
                ('McomsVolts', models.IntegerField(blank=True, null=True)),
                ('Ocr504Amps', models.IntegerField(blank=True, null=True)),
                ('Ocr504Volts', models.IntegerField(blank=True, null=True)),
                ('ParkDescentPCnt', models.IntegerField(blank=True, null=True)),
                ('ParkBuoyancyPosition', models.IntegerField(blank=True, null=True)),
                ('ProfileId', models.IntegerField(blank=True, null=True)),
                ('ObsIndex', models.IntegerField(blank=True, null=True)),
                ('QuiescentAmps', models.IntegerField(blank=True, null=True)),
                ('QuiescentVolts', models.IntegerField(blank=True, null=True)),
                ('Sbe41cpAmps', models.IntegerField(blank=True, null=True)),
                ('Sbe41cpVolts', models.IntegerField(blank=True, null=True)),
                ('Sbe63Amps', models.IntegerField(blank=True, null=True)),
                ('Sbe63Volts', models.IntegerField(blank=True, null=True)),
                ('SurfaceBuoyancyPosition', models.IntegerField(blank=True, null=True)),
                ('Vacuum', models.IntegerField(blank=True, null=True)),
                ('NpfFwRev', models.CharField(blank=True, max_length=50, null=True)),
                ('IceEvasionRecord', models.CharField(blank=True, max_length=50, null=True)),
                ('IceMLMedianT', models.CharField(blank=True, max_length=50, null=True)),
                ('Sbe41cpStatus', models.CharField(blank=True, max_length=50, null=True)),
                ('status', models.CharField(blank=True, max_length=50, null=True)),
                ('gps_lon', models.FloatField(blank=True, null=True)),
                ('gps_lat', models.FloatField(blank=True, null=True)),
                ('Sbe41cpHumidity', models.FloatField(blank=True, null=True)),
                ('Sbe41cpHumidityTemp', models.FloatField(blank=True, null=True)),
                ('SurfacePressure', models.FloatField(blank=True, null=True)),
                ('TimeStartDescent', models.DateTimeField(blank=True, null=True)),
                ('TimeStartPark', models.DateTimeField(blank=True, null=True)),
                ('TimeStartProfileDescent', models.DateTimeField(blank=True, null=True)),
                ('TimeStartProfile', models.DateTimeField(blank=True, null=True)),
                ('TimeStopProfile', models.DateTimeField(blank=True, null=True)),
                ('TimeStartTelemetry', models.DateTimeField(blank=True, null=True)),
                ('DEPLOYMENT', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='cycle_metadata', to='deployments.deployment')),
            ],
            options={
                'verbose_name_plural': 'Cycle Metadata',
            },
        ),
        migrations.AlterField(
            model_name='continuous_profile',
            name='PROFILE_METADATA',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='env_data.cycle_metadata', to_field='PROFILE_ID'),
        ),
        migrations.AlterField(
            model_name='discrete_profile',
            name='PROFILE_METADATA',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='env_data.cycle_metadata', to_field='PROFILE_ID'),
        ),
        migrations.DeleteModel(
            name='profile_metadata',
        ),
    ]