# Generated by Django 4.2.3 on 2023-11-10 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0052_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='payaddress',
            name='amount',
            field=models.FloatField(default=0),
        ),
    ]
