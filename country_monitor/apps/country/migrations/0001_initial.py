# Generated by Django 4.2.17 on 2025-01-08 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flag_png', models.URLField()),
                ('flag_svg', models.URLField()),
                ('flag_alt', models.TextField(blank=True, null=True)),
                ('name_common', models.CharField(max_length=255)),
                ('name_official', models.CharField(max_length=255)),
                ('native_name_official', models.CharField(max_length=255)),
                ('native_name_common', models.CharField(max_length=255)),
                ('capital', models.CharField(max_length=255)),
                ('lat', models.FloatField()),
                ('lng', models.FloatField()),
                ('area', models.FloatField()),
                ('population', models.IntegerField()),
                ('timezone', models.CharField(max_length=50)),
                ('continent', models.CharField(max_length=100)),
            ],
        ),
    ]