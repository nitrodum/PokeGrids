# Generated by Django 4.2.7 on 2023-11-14 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grid', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pokemon',
            name='lengendary',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='pokemon',
            name='type2',
            field=models.CharField(default='None', max_length=50),
        ),
    ]
