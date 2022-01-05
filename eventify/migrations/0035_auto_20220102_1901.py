# Generated by Django 2.2.1 on 2022-01-02 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventify', '0034_auto_20220102_1858'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.CharField(choices=[('Seminar', 'Seminar'), ('Conference', 'Conference'), ('Workshop', 'Workshop'), ('Themed party', 'Themed Party'), ('Webinar', 'Webinar'), ('Summit', 'Summit'), ('Music festival', 'Music estival')], default='Seminar', max_length=20),
        ),
        migrations.AlterField(
            model_name='post',
            name='eventtime',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='service',
            name='category',
            field=models.CharField(choices=[('Seminar', 'Seminar'), ('Conference', 'Conference'), ('Workshop', 'Workshop'), ('Themed party', 'Themed Party'), ('Webinar', 'Webinar'), ('Summit', 'Summit'), ('Music festival', 'Music estival')], default='Seminar', max_length=20),
        ),
        migrations.AlterField(
            model_name='service',
            name='eventtime',
            field=models.TimeField(),
        ),
    ]