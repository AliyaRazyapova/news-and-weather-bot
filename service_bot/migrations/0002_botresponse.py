# Generated by Django 3.2.20 on 2023-07-29 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service_bot', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BotResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('command', models.CharField(max_length=255)),
                ('response', models.TextField()),
            ],
        ),
    ]
