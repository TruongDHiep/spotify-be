# Generated by Django 5.2 on 2025-04-22 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('songs', '0004_alter_song_file_upload_alter_song_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='mv',
            field=models.TextField(blank=True),
        ),
    ]
