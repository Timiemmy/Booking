# Generated by Django 5.2 on 2025-04-14 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('driver', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driver',
            name='rating',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
