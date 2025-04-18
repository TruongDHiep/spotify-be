# Generated by Django 5.2 on 2025-04-10 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100, unique=True)),
                ('pass_hash', models.CharField(max_length=256)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('dob', models.DateField()),
                ('avatar', models.TextField()),
                ('is_premium', models.BooleanField(default=False)),
                ('is_online', models.BooleanField(default=False)),
            ],
        ),
    ]
