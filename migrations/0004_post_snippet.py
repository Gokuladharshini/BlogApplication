# Generated by Django 3.2.3 on 2021-05-25 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Sblogs', '0003_post_header_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='snippet',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
