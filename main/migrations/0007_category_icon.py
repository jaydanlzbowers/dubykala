# Generated by Django 4.2.3 on 2023-10-31 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_alter_category_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='icon',
            field=models.ImageField(default=1, upload_to='img_category'),
            preserve_default=False,
        ),
    ]