# Generated by Django 3.2 on 2021-06-02 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deployments', '0039_auto_20210602_1607'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deployment',
            name='FLOAT_SERIAL_NO',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
    ]