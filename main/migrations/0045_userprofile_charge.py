# Generated by Django 4.2.3 on 2023-11-06 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0044_remove_address_user_address_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='charge',
            field=models.FloatField(default=0),
        ),
    ]
