# Generated by Django 4.2.3 on 2023-11-01 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_rename_number_userprofile_mobile'),
    ]

    operations = [
        migrations.AddField(
            model_name='faq',
            name='serialnumber',
            field=models.IntegerField(default=0),
        ),
    ]