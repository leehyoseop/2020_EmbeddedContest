# Generated by Django 3.0.6 on 2020-08-21 08:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_clothes_category_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_closet',
            name='frequency',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='Recommendation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bottom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rec_bottom', to='accounts.Clothes_category')),
                ('outer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rec_outer', to='accounts.Clothes_category')),
                ('top', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rec_top', to='accounts.Clothes_category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Account')),
            ],
            options={
                'db_table': 'recommendation',
            },
        ),
        migrations.CreateModel(
            name='Frequency_Fashion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bottom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fre_bottom', to='accounts.Clothes_category')),
                ('outer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fre_outer', to='accounts.Clothes_category')),
                ('top', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fre_top', to='accounts.Clothes_category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Account')),
            ],
            options={
                'db_table': 'frequency_fashion',
            },
        ),
    ]