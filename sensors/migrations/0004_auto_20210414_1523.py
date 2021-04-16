# Generated by Django 3.2 on 2021-04-14 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sensors', '0003_auto_20210414_1507'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensor',
            name='PREDEPLOYMENT_CALIB_COEFFICIENT',
            field=models.JSONField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='sensor',
            name='PREDEPLOYMENT_CALIB_EQUATION',
            field=models.JSONField(blank=True, max_length=100, null=True),
        ),
    ]