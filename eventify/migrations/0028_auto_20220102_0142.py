# Generated by Django 2.2.1 on 2022-01-01 22:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventify', '0027_auto_20220102_0012'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='address',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='service',
            name='address',
            field=models.TextField(blank=True),
        ),
    ]