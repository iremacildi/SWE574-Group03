# Generated by Django 2.2.1 on 2022-05-23 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20220523_2137'),
    ]

    operations = [
        migrations.CreateModel(
            name='InterestSelection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interest_1', models.CharField(choices=[('sport', 'Sport'), ('art', 'Art'), ('music', 'Music'), ('cooking', 'Cooking'), ('agriculture', 'Agriculture'), ('handicraft', 'Handicraft'), ('dance', 'Dance'), ('music', 'Music'), ('cinema', 'Cinema'), ('fashion', 'Fashion')], max_length=120)),
                ('interest_2', models.CharField(choices=[('sport', 'Sport'), ('art', 'Art'), ('music', 'Music'), ('cooking', 'Cooking'), ('agriculture', 'Agriculture'), ('handicraft', 'Handicraft'), ('dance', 'Dance'), ('music', 'Music'), ('cinema', 'Cinema'), ('fashion', 'Fashion')], max_length=120)),
                ('interest_3', models.CharField(choices=[('sport', 'Sport'), ('art', 'Art'), ('music', 'Music'), ('cooking', 'Cooking'), ('agriculture', 'Agriculture'), ('handicraft', 'Handicraft'), ('dance', 'Dance'), ('music', 'Music'), ('cinema', 'Cinema'), ('fashion', 'Fashion')], max_length=120)),
            ],
        ),
    ]
