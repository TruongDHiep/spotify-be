# Generated by Django 5.2 on 2025-04-18 09:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('songs', '0002_song_play_count'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ListeningHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('listened_at', models.DateTimeField(auto_now_add=True)),
                ('song', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listened_by', to='songs.song')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listening_histories', to='users.user')),
            ],
            options={
                'ordering': ['-listened_at'],
            },
        ),
    ]
