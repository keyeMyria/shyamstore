# Generated by Django 2.0.5 on 2018-07-26 13:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('temp_app', '0006_auto_20180726_1842'),
        ('users', '0002_auto_20180717_1656'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetails',
            name='designation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='designations.Designations'),
        ),
        migrations.DeleteModel(
            name='Designations',
        ),
    ]
