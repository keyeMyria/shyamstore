# Generated by Django 2.0.5 on 2018-07-10 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0003_auto_20180710_1559'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customers',
            name='contact_no',
            field=models.CharField(blank=True, default=None, max_length=255, null=True),
        ),
    ]
