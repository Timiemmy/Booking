# Generated by Django 5.2 on 2025-04-08 11:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('vehicle', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('license_number', models.CharField(max_length=50, unique=True)),
                ('license_expiry_date', models.DateField()),
                ('rating', models.FloatField()),
                ('is_available', models.BooleanField(default=True)),
                ('total_trips', models.PositiveIntegerField(default=0)),
                ('driver_license_image', models.ImageField(blank=True, null=True, upload_to='drivers_licenses/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='driver_profile', to=settings.AUTH_USER_MODEL)),
                ('vehicle', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='drivers', to='vehicle.vehicle')),
            ],
            options={
                'verbose_name': 'Driver',
                'verbose_name_plural': 'Drivers',
            },
        ),
        migrations.CreateModel(
            name='DriverVerification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_document', models.FileField(upload_to='driver_verification/id/')),
                ('license_document', models.FileField(upload_to='driver_verification/license/')),
                ('address_proof', models.FileField(blank=True, null=True, upload_to='driver_verification/address/')),
                ('background_check_status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=20)),
                ('background_check_report', models.FileField(blank=True, null=True, upload_to='verification/background/')),
                ('verification_notes', models.TextField(blank=True)),
                ('verified_at', models.DateTimeField(blank=True, null=True)),
                ('rejection_reason', models.TextField(blank=True)),
                ('driver', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='verification', to='driver.driver')),
                ('verified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
