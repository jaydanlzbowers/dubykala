# Generated by Django 4.2.3 on 2023-11-03 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0030_product_category_product_rate'),
    ]

    operations = [
        migrations.AddField(
            model_name='brand',
            name='article',
            field=models.TextField(default=1, max_length=20000),
            preserve_default=False,
        ),
    ]
