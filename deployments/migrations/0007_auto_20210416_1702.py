# Generated by Django 3.2 on 2021-04-16 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deployments', '0006_rename_internal_id_no_deployment_aoml_id'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='deployment',
            name='deployments_deployment_CHECKS',
        ),
        migrations.AlterField(
            model_name='deployment',
            name='DEPLOYMENT_TYPE',
            field=models.CharField(blank=True, choices=[('RV', 'RV'), ('VOS', 'VOS'), ('RRS', 'RRS')], max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='deployment',
            name='LAUNCH_DATE_QC',
            field=models.CharField(blank=True, choices=[('estimated', 'estimated'), ('as recorded', 'as recorded')], default='estimated', max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='deployment',
            name='LAUNCH_POSITION_QC',
            field=models.CharField(blank=True, choices=[('estimated', 'estimated'), ('as recorded', 'as recorded')], default='estimated', max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='deployment',
            name='START_DATE_QC',
            field=models.CharField(blank=True, choices=[('estimated', 'estimated'), ('as recorded', 'as recorded')], default='estimated', max_length=25, null=True),
        ),
        migrations.AddConstraint(
            model_name='deployment',
            constraint=models.CheckConstraint(check=models.Q(('TRANS_SYSTEM__in', ['IRIDIUM', 'ARGOS', 'ORBCOMM']), ('START_DATE_QC__in', ['estimated', 'as recorded']), ('LAUNCH_DATE_QC__in', ['estimated', 'as recorded']), ('LAUNCH_POSITION_QC__in', ['estimated', 'as recorded']), ('DEPLOYMENT_TYPE__in', ['RV', 'VOS', 'RRS']), ('LAUNCH_LATITUDE__lte', 90), ('LAUNCH_LATITUDE__gte', -90), ('LAUNCH_LONGITUDE__lte', 180), ('LAUNCH_LONGITUDE__gte', -180)), name='deployments_deployment_CHECKS'),
        ),
    ]
