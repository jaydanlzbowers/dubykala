# Generated by Django 4.2.3 on 2023-11-03 15:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0034_product_nrate'),
    ]

    operations = [
        migrations.RenameField(
            model_name='detail',
            old_name='name',
            new_name='key',
        ),
        migrations.RenameField(
            model_name='detail',
            old_name='title',
            new_name='value',
        ),
    ]