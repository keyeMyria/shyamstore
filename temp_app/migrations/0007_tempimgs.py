# Generated by Django 2.0.5 on 2018-07-02 10:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('temp_app', '0006_auto_20180702_1303'),
    ]

    operations = [
        migrations.CreateModel(
            name='TempImgs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('src', models.CharField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('app', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='temp_app.TempAppMasters')),
            ],
        ),
    ]
