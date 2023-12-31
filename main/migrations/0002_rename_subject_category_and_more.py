# Generated by Django 4.2.3 on 2023-10-31 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Subject',
            new_name='Category',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='subject',
            new_name='category',
        ),
        migrations.AddField(
            model_name='product',
            name='detail',
            field=models.JSONField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='flag',
            field=models.JSONField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='saleamount',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='picture',
            name='img',
            field=models.ImageField(upload_to=''),
        ),
        migrations.DeleteModel(
            name='Detail',
        ),
    ]
