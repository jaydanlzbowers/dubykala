# Generated by Django 4.2.3 on 2023-11-04 19:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0037_alter_comment_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='faq',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='main.userprofile'),
            preserve_default=False,
        ),
    ]
