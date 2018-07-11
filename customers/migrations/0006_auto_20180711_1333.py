# Generated by Django 2.0.5 on 2018-07-11 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0005_auto_20180710_1655'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customers',
            name='contact_no',
            field=models.CharField(blank=True, default=None, max_length=15, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='customers',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True),
        ),
    ]