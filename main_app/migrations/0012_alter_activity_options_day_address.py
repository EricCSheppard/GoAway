# Generated by Django 4.1.7 on 2023-03-14 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0011_alter_activity_time'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='activity',
            options={'ordering': ['time']},
        ),
        migrations.AddField(
            model_name='day',
            name='address',
            field=models.CharField(default='', max_length=70),
        ),
    ]
