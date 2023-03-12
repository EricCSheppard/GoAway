# Generated by Django 4.1.7 on 2023-03-12 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_alter_day_options_day_flight_alter_day_city_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='inout',
            field=models.CharField(choices=[('I', 'Inside'), ('O', 'Outside')], default='I', max_length=1),
        ),
        migrations.AlterField(
            model_name='activity',
            name='description',
            field=models.CharField(max_length=125),
        ),
        migrations.AlterField(
            model_name='activity',
            name='time',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='day',
            name='flight',
            field=models.CharField(blank=True, default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='day',
            name='state',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='day',
            name='transport',
            field=models.CharField(blank=True, choices=[('W', 'Walk'), ('B', 'Bike'), ('D', 'Drive'), ('T', 'Train'), ('F', 'Fly')], default='D', max_length=1),
        ),
    ]
