# Generated by Django 4.1.7 on 2023-03-14 16:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0012_alter_activity_options_day_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='day',
            name='address',
            field=models.CharField(blank=True, default='', max_length=70),
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=200)),
                ('trip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.trip')),
            ],
        ),
    ]