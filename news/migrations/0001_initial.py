# Generated by Django 4.2 on 2023-04-15 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.TextField()),
            ],
            options={
                'verbose_name': 'News-Link',
                'verbose_name_plural': 'News-Links',
                'db_table': 'news',
            },
        ),
    ]
