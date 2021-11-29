# Generated by Django 3.2.9 on 2021-11-27 16:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0002_auto_20211125_2054'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place', models.CharField(max_length=50)),
                ('number', models.CharField(max_length=10)),
                ('neighborhood', models.CharField(max_length=50)),
                ('complements', models.CharField(blank=True, max_length=255, null=True)),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
                ('cep', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ResidenceType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ServiceType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hours', models.IntegerField()),
                ('date', models.DateField()),
                ('bathrooms', models.IntegerField()),
                ('bedrooms', models.IntegerField()),
                ('value', models.FloatField()),
                ('completed', models.BooleanField()),
                ('opened', models.BooleanField()),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.address')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.customer')),
                ('partner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.partner')),
                ('residence', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.residencetype')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.servicetype')),
            ],
        ),
    ]