# Generated by Django 5.2 on 2025-04-10 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('avatar', models.ImageField(upload_to='artists/')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('description', models.TextField(blank=True)),
            ],
        ),
    ]
