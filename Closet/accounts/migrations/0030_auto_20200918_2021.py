# Generated by Django 3.0.6 on 2020-09-18 11:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0029_auto_20200918_2021'),
    ]

    operations = [
        migrations.AddField(
            model_name='frequency_fashion',
            name='dress',
            field=models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, related_name='fre_dress', to='accounts.Clothes_category'),
        ),
        migrations.AddField(
            model_name='recommendation',
            name='dress',
            field=models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, related_name='rec_dress', to='accounts.Clothes_category'),
        ),
    ]