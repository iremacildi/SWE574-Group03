# Generated by Django 2.2.1 on 2022-05-22 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventify', '0048_servicechart_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicechart',
            name='range',
            field=models.IntegerField(default=1),
        ),
    ]
