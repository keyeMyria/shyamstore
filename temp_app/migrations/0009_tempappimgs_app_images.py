# Generated by Django 2.0.5 on 2018-07-02 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('temp_app', '0008_auto_20180702_1603'),
    ]

    operations = [
        migrations.AddField(
            model_name='tempappimgs',
            name='app_images',
            field=models.ImageField(default=None, upload_to='app_images'),
        ),
    ]
