# Generated by Django 4.2.3 on 2023-11-07 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0045_userprofile_charge'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='city',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
    ]
