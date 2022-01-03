# Generated by Django 3.2 on 2021-12-14 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('choices', '0025_tracking_error_types'),
    ]

    operations = [
        migrations.CreateModel(
            name='deployment_platforms_C17',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('VALUE', models.CharField(max_length=100, unique=True)),
                ('ACTIVE', models.BooleanField()),
                ('TYPE', models.CharField(choices=[('R/V', 'R/V'), ('VOS', 'VOS'), ('M/V', 'M/V'), ('AIR', 'AIR')], max_length=25)),
                ('ICES', models.CharField(blank=True, max_length=25, null=True)),
                ('SOURCE', models.CharField(blank=True, max_length=25, null=True)),
                ('DESCRIPTION', models.CharField(blank=True, max_length=2000, null=True)),
            ],
            options={
                'verbose_name_plural': 'Deployment Platforms C17',
            },
        ),
    ]