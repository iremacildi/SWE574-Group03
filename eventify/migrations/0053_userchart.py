# Generated by Django 2.2.1 on 2022-05-27 15:25

from django.db import migrations, models
import django.utils.timezone
import location_field.models.plain


class Migration(migrations.Migration):

    dependencies = [
        ('eventify', '0052_auto_20220523_2107'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserChart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(default=django.utils.timezone.now)),
                ('end_date', models.DateField(default=django.utils.timezone.now)),
                ('paid', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('credits', models.IntegerField(default=1)),
                ('location', location_field.models.plain.PlainLocationField(default='41.088165, 29.043431', max_length=63)),
                ('range', models.IntegerField(default=1)),
            ],
        ),
    ]