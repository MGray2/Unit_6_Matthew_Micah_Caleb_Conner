# Generated by Django 4.2.6 on 2024-01-11 01:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_alter_customuser_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='profile_picture',
            field=models.ImageField(blank=True, default="{% static 'images/dinosaur_profile_default.jpg' %}", null=True, upload_to='profile_pictures/'),
        ),
    ]
