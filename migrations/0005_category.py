# Generated by Django 3.2.3 on 2021-05-27 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Sblogs', '0004_post_snippet'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
    ]
