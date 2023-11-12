# Generated by Django 4.2.7 on 2023-11-12 04:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Grid',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('selected', models.IntegerField()),
                ('type', models.CharField(max_length=50)),
                ('generation', models.IntegerField()),
                ('evolution_stage', models.IntegerField()),
                ('lengendary', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Pokemon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('type1', models.CharField(max_length=50)),
                ('type2', models.CharField(max_length=50)),
                ('generation', models.IntegerField()),
                ('evolution_stage', models.IntegerField()),
                ('lengendary', models.BooleanField()),
            ],
        ),
    ]