# Generated by Django 3.0.6 on 2020-08-08 08:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_remove_raspberrypi_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='raspberrypi',
            name='user',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='accounts.Account'),
        ),
    ]