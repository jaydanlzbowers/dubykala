# Generated by Django 4.2.3 on 2023-11-12 14:49

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0053_payaddress_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='present',
            field=ckeditor_uploader.fields.RichTextUploadingField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='specialpresent',
            field=ckeditor_uploader.fields.RichTextUploadingField(default=1),
            preserve_default=False,
        ),
    ]