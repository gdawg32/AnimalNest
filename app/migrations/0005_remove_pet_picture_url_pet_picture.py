# Generated by Django 4.2 on 2024-08-26 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_remove_pet_picture_pet_picture_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pet',
            name='picture_url',
        ),
        migrations.AddField(
            model_name='pet',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='pets/'),
        ),
    ]
