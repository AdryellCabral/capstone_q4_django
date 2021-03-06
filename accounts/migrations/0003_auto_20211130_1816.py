# Generated by Django 3.2.9 on 2021-11-30 18:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
        ('accounts', '0002_auto_20211125_2054'),
    ]

    operations = [
        migrations.AddField(
            model_name='partner',
            name='address',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='partners', to='orders.address'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='partner',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='partners', to='orders.servicetype'),
            preserve_default=False,
        ),
    ]
