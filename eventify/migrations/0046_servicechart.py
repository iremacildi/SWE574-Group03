# Generated by Django 2.2.1 on 2022-05-18 21:09

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('eventify', '0045_auto_20220516_2043'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceChart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(default=django.utils.timezone.now)),
                ('end_date', models.DateField(default=django.utils.timezone.now)),
                ('min_attendee', models.IntegerField(default=0)),
                ('max_attendee', models.IntegerField(default=0)),
            ],
        ),
    ]