# Generated by Django 4.2.20 on 2025-05-27 14:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('App2', '0002_remove_surveillance_location_delete_plantlocation'),
    ]

    operations = [
        migrations.CreateModel(
            name='EntryExitLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=100)),
                ('person_name', models.CharField(max_length=100)),
                ('purpose', models.CharField(max_length=255)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('remarks', models.TextField(blank=True, null=True)),
                ('farm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App2.farm')),
            ],
        ),
    ]
