# Generated by Django 2.0.5 on 2018-07-02 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('temp_app', '0005_tempusers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tempusers',
            name='user_locality',
            field=models.TextField(blank=True, null=True),
        ),
    ]
