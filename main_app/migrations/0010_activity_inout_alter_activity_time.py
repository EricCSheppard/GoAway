# Generated by Django 4.1.7 on 2023-03-12 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0009_remove_activity_inout'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='inout',
            field=models.CharField(choices=[('I', 'Inside'), ('O', 'Outside')], default='I', max_length=1),
        ),
        migrations.AlterField(
            model_name='activity',
            name='time',
            field=models.CharField(choices=[('M', 'Morning'), ('A', 'Afternoon'), ('E', 'Evening')], default='M', max_length=1),
        ),
    ]
