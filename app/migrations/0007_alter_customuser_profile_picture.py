# Generated by Django 4.2.6 on 2024-01-11 00:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_channel_safe_mode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='profile_picture',
            field=models.ImageField(blank=True, default='app/static/dinosaur_profile_default.jpg', null=True, upload_to='profile_pictures/'),
        ),
    ]
