# Generated by Django 3.2 on 2021-06-10 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0008_alter_deployment_tracking_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file_processing',
            name='STATUS',
            field=models.CharField(choices=[('Success', 'Success'), ('Fail', 'Fail'), ('Warning', 'Warning'), ('Skip', 'Skip'), ('Reprocess', 'Reprocess')], max_length=200),
        ),
    ]
