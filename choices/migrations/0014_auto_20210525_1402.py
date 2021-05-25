# Generated by Django 3.2 on 2021-05-25 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('choices', '0013_deployment_platforms'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='battery_manufacturers',
            name='DESCRIPTION',
        ),
        migrations.RemoveField(
            model_name='battery_manufacturers',
            name='SOURCE',
        ),
        migrations.RemoveField(
            model_name='battery_types',
            name='DESCRIPTION',
        ),
        migrations.RemoveField(
            model_name='battery_types',
            name='SOURCE',
        ),
        migrations.RemoveField(
            model_name='deployment_platforms',
            name='SOURCE',
        ),
        migrations.RemoveField(
            model_name='origin_countries',
            name='DESCRIPTION',
        ),
        migrations.RemoveField(
            model_name='origin_countries',
            name='SOURCE',
        ),
        migrations.AlterField(
            model_name='deployment_platforms',
            name='DESCRIPTION',
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='platform_makers',
            name='DESCRIPTION',
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='platform_types',
            name='DESCRIPTION',
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='transmission_systems',
            name='DESCRIPTION',
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
    ]
